from __driver__ import driver

import copy
import subprocess

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class commandline(driver):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, driver_config):
        driver.__init__(self, driver_config)
        self.command    = None
        try:
            self.command = self.driver_config.get('target')
        except Exception, ex:
            raise Exception('no target definition found: %s' % str(ex))
        try:
            self.command = self.command.get('command')
        except Exception, ex:
            raise Exception('no target command found: %s' % str(ex))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def connect(self):
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def send(self, data):

        params = [self.command] + data

        try:
            if subprocess.call(params, 
                               stdout=None,
                               stderr=subprocess.STDOUT) < 0:
                return False
        except Exception, ex:
            raise Exception('failed to execute command "%s": %s' %\
                            (params[0], str(ex)))
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def disconnect(self):
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def receive(self):
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def driver_socket(self):
        return None

