import struct
from classes.Utils import Utils
from primitives.__primitive import __primitive__

all_properties = [
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    },
    {
        "name": "size",
        "type": ["int", "long"],
        "default": 4,
        "error": "primitive requires size to be of type int or long"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
    },
    {
        "name": "full_range",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires full_range to be of type bool (1 or 0)"
    },
    {
        "name": "inclusive",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive requires inclusive to be of type bool (1 or 0)"
    },
    {
        "name": "offset",
        "type": ["int", "long"],
        "default": 0,
        "value": 0,
        "mandatory": 0,
        "error": "primitive requires offset to be of type type int or long"
    },
    {
        "name": "value",
        "type": ["int", "long"],
        "default": 0,
        "value": 0,
        "mandatory": 0,
        "error": "primitive requires value to be of type type int or long"
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
        "name": "block",
        "type": "str",
        "mandatory": 0,
        "error": "primitive requires block name to be of type str"
    }
]

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class sizer(__primitive__):

    """
     NOTE: Sizer always has to be outside of the target block.
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
        max = Utils.bin_to_dec("1" + "0" * (self.get('size') * 8)) - 1

        if self.full_range:
            for i in xrange(0, max + 1):
                if i not in self.library: self.library.append(i)
        else:
            self.library += Utils.integer_boundaries(
                self.library,
                max,
                0)
            self.library += Utils.integer_boundaries(
                self.library,
                max,
                max)
            for v in [2, 3, 4, 8, 16, 32]:
                self.library += Utils.integer_boundaries(
                    self.library,
                    max,
                    max / v)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def format(self, value):
        if self.get('format') == "ascii":
            return str(value)
        else:
            endian = ">"
            if self.get('endian') == "little":
                endian = "<"

            format = "I"
            if self.get('size') == 1:
                format = "B"
            elif self.get('size') == 4:
                format = "I"
            elif self.get('size') == 8:
                format = "Q"

            try:
                return struct.pack(endian + format, value)
            except Exception, ex:
                raise Exception('failed to render sizer %s (%s)' %\
                (self.name,  str(ex)))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        if self.fuzzable and not self.completed:
            value = super(sizer, self).render()
            return self.format(value)

        b = self.search(self.block)
        length = len(b.render())
        if self.get('inclusive'): length += self.get('size')
        if self.get('offset'): length += self.get('offset')

        value = self.format(length)
        value = self.apply_transforms(value, True)
        return value

