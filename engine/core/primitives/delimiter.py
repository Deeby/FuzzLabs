from __primitive import __primitive__

all_properties = [
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    },
    {
        "name": "value",
        "type": "str",
        "mandatory": 1,
        "error": "primitive requires value to be of type str"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
    }
]

# =============================================================================
#
# =============================================================================

class delimiter(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent):
        global all_properties
        self.type = self.__class__.__name__
        __primitive__.__init__(self, properties, all_properties, parent)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):

        rounds = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
        delims = [" ", "\t", "\t\r\n", "!", "@", "#", "$", "%", "^", "&",
                  "*", "(", ")", "-", "_", "+", "=", ":", ";", "'", "\"",
                  "/", "\\", "?", "<", ">", ".", ",", "\r", "\n", "\r\n"]

        self.library.append(self.value)
        self.library.append("")
        for length in rounds:
            self.library.append(self.value * length)

        for delim in delims:
            for round in rounds:
                self.library.append(delim * round)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        value = super(delimiter, self).render()
        return str(value)

