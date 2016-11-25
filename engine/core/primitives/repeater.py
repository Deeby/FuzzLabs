import struct
from primitives.__primitive import __primitive__

all_properties = [
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
    },
    {
        "name": "min",
        "type": ["int", "long"],
        "mandatory": 0,
        "default": 0,
        "error": "primitive requires min to be of type int or long"
    },
    {
        "name": "max",
        "type": ["int", "long"],
        "mandatory": 0,
        "default": 0,
        "error": "primitive requires max to be of type int or long"
    },
    {
        "name": "step",
        "type": ["int", "long"],
        "mandatory": 0,
        "default": 0,
        "error": "primitive requires step to be of type str"
    },
    {
        "name": "block",
        "type": "str",
        "mandatory": 1,
        "error": "primitive requires block name to be of type str"
    },
    {
        "name": "value",
        "type": "str",
        "mandatory": 1,
        "default": "",
        "error": "primitive requires value to be of type str"
    }
]

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class repeater(__primitive__):

    """
     NOTE: Repeater always has to be outside of the target block.
    """

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent = None):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):
        b = self.search(self.block)
        if not b:
            raise Exception('repater could not find target block: %s' %\
                            self.block)
        v = b.render()
        for n in range(self.min, self.max + 1, self.step):
            self.library.append(v * n)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        value = super(repeater, self).render()
        return value

