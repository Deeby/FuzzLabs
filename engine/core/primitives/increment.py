from __primitive import __primitive__
from classes.Utils import Utils
import struct

all_properties = [
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    },
    {
        "name": "value",
        "type": ["int", "long"],
        "value": 0,
        "mandatory": 1,
        "error": "primitive requires value to be of type long or int"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [1],
        "default": 1,
        "error": "primitive requires fuzzable to be True (1)"
    }
]

# =============================================================================
#
# =============================================================================

class increment(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)
        self.value -= 2
        self.ignore = True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        self.value += 1
        super(increment, self).render()
        return str(self.value)

