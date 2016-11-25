import glob
import importlib
from logic.Linear import Linear
from primitives.__primitive import __primitive__

all_properties = [
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
    },
    {
        "name": "group",
        "type": "str",
        "default": "",
        "mandatory": 0,
        "error": "primitive requires group to be of type str"
    },
    {
        "name": "logic",
        "type": "str",
        "value": "linear",
        "default": "linear",
        "mandatory": 0,
        "error": "primitive requires logic to be of type str"
    },
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    }
]

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class block(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent = None):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)
        self.completed = False

        self.load_primitives(properties.get('primitives'))

        lmod = importlib.import_module("logic." + self.logic[0].upper() +\
                                       self.logic[1:])
        self.logic = getattr(lmod,
                             self.logic[0].upper() + self.logic[1:])(self)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def load_primitives(self, primitives):
        pmod = None
        for primitive in primitives:
            try:
                pmod = importlib.import_module("primitives." +\
                                               primitive.get('primitive'))
            except Exception, ex:
                raise Exception("failed to import primitive %s (%s)" % \
                      (primitive.get('primitive'), str(ex)))
            try:
                inst = getattr(pmod, primitive.get('primitive'))
                inst = inst(primitive, self)
            except Exception, ex:
                raise Exception("failed to instantiate primitive %s (%s)" % \
                      (primitive.get('primitive'), str(ex)))
            try:
                self.primitives.append(inst)
            except Exception, ex:
                raise Exception("failed to store primitive %s (%s)" % \
                      (primitive.get('primitive'), str(ex)))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        if self.logic.completed:
            self.completed = True
            return
        self.logic.mutate()

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        return self.logic.render()

