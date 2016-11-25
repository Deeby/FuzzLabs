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
        "mandatory": 1,
        "error": "primitive requires value to be of type long or int"
    },
    {
        "name": "max_num",
        "type": ["int", "long"],
        "default": 0xFFFFFFFF,
        "error": "primitive requires max_num to be of type int"
    },
    {
        "name": "endian",
        "type": "str",
        "values": ["big", "little"],
        "default": "big",
        "error": "primitive requires endian to be of type str ('big' or 'little')"
    },
    {
        "name": "format",
        "type": "str",
        "values": ["binary", "ascii"],
        "default": "binary",
        "error": "primitive requires format to be of type str"
    },
    {
        "name": "signed",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires signed to be of type bool (1 or 0)"
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

class dword(__primitive__):

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
        max = Utils.bin_to_dec("1" + "0" * 32)  - 1 # 32 bits
        if self.signed: max = max / 2

        if self.max_num and self.max_num > max:
            raise Exception("%s primitive maximum value is %d" % (self.type, max))
        if self.max_num == None or self.max_num == 0:
            self.max_num = max

        self.library += Utils.integer_boundaries(
            self.library, 
            self.max_num, 
            0)
        self.library += Utils.integer_boundaries(
            self.library,
            self.max_num,
            self.max_num)
        for v in [2, 3, 4, 8, 16, 32]:
            self.library += Utils.integer_boundaries(
                self.library,
                self.max_num,
                self.max_num / v)

        negatives = []
        if self.signed:
            for v in self.library:
                negatives.append(-v)
        self.library += negatives

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        endian = ">"
        if self.get('endian') == "little":
            endian = "<"
        if self.format == "binary":
            if self.signed:
                self.value = struct.pack(endian + "i", self.value)
            else:
                self.value = struct.pack(endian + "I", self.value)
        value = super(dword, self).render()
        return str(value)

