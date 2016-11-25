import os
import time
import inspect
import threading
from classes.Utils import Utils
from classes.Config import Config
from logic.Linear import Linear
from primitives.block import block
from classes.MutationsExhaustedException import MutationsExhaustedException

STATE_DISCONNECTED = 0
STATE_CONNECTED = 1

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Scenario(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, config, scenario_id, job):
        scenario            = job.get('scenarios')[scenario_id]
        self.id             = scenario_id
        self.sleep_time     = 0
        self.job            = job
        self.config         = config
        self.name           = scenario.get('name')
        if not self.name:
            self.name       = str(scenario_id)
        self.units          = []
        self.current_unit   = None
        self.state          = STATE_CONNECTED

        if self.job.get('session'):
            if self.job.get('session').get('sleep_time'):
                self.sleep_time = self.job.get('session').get('sleep_time')

        if not scenario.get('units'):
            raise Exception("no unit specified for scenario")

        for unit in scenario.get('units'):
            self.units.append(self.load_unit(unit))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def stateConnected(self):
        self.state = STATE_CONNECTED

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def stateDisconnected(self):
        self.state = STATE_DISCONNECTED

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def load_unit(self, unit):
        data = None
        u_path = self.config.get('root') + "/units/" + unit + ".json"
        u_path = os.path.dirname(
            os.path.abspath(
                inspect.getfile(inspect.currentframe()
            ))) + "/../../units/" + unit + ".json"
        try:
            data = Utils.read_json(u_path)
        except Exception, ex:
            raise Exception("failed to read unit '%s': %s" % (unit, str(ex)))
        try:
            if not data.get('properties'):
                data['properties'] = {}
            if data.get('properties').get('name'):
                data['properties']['name'] = unit
            return block(data)
        except Exception, ex:
            raise Exception("failed to load unit '%s': %s" % (unit, str(ex)))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def unit_status(self, unit, s_object):
        for item in unit:
            primitives = item.get('primitives')
            if not primitives:
                s_object[item.name] = {
                    "total_mutations": item.total_mutations,
                    "mutation_index": item.mutation_index
                }
            else:
                self.unit_status(item, s_object)
        return s_object

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def status(self, include_units = False):
        s_info = {
            "name": self.name,
            "current_unit": self.current_unit
        }
        if include_units:
            s_info['units'] = []
            for item in self.units:
                s_object = {}
                s_info['units'].append({
                    "name": item.get('name'),
                    "status": self.unit_status(item, s_object)
                })
        return s_info

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def run(self):
        for unit in self.units:
            self.current_unit = unit.get('name')
            while not unit.completed:
                try:
                    unit.mutate()
                except Exception, ex:
                    raise Exception("failed to mutate unit '%s': %s" %\
                                   (unit.name, str(ex)))

                if self.state != STATE_CONNECTED:
                    yield {"state": "connect"}
                for r_unit in self.units:
                    data = None
                    try:
                        data = r_unit.render()
                    except Exception, ex:
                        raise Exception("failed to render unit '%s': %s" %\
                                       (unit.name, str(ex)))

                    yield {"state": "process", "data": r_unit.render()}

                    time.sleep(self.sleep_time)
                if self.state != STATE_DISCONNECTED:
                    yield {"state": "disconnect"}
        raise MutationsExhaustedException("all mutations exhausted")

