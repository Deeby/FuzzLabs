from classes.Utils import Utils

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Config(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, root, filename):
        self.root = root
        self.data = Utils.read_json(root + filename)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def save(self):
        Utils.save_file(self.root + "/config/config.json",
                        self.data,
                        True)

