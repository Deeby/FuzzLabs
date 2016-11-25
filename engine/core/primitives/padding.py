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
        "default": 0,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
    },
    {
        "name": "align",
        "type": ["int", "long"],
        "mandatory": 0,
        "default": 4096,
        "error": "primitive requires align to be of type int or long"
    },
    {
        "name": "expand",
        "type": "bool",
        "values": [0, 1],
        "mandatory": 0,
        "default": 0,
        "error": "primitive requires expand to be of type int or long"
    },
    {
        "name": "block",
        "type": "str",
        "mandatory": 1,
        "error": "primitive requires block name to be of type str"
    },
    {
        "name": "value",
        "type": "int",
        "mandatory": 1,
        "default": 0,
        "error": "primitive requires value to be of type int"
    }
]

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class padding(__primitive__):

    """
     NOTE: Padding always has to be outside of the target block.
    """

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent = None):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)
        self.ignore = True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        b = self.search(self.block)
        if not b:
            raise Exception('repater could not find target block: %s' %\
                            self.block)
        v = b.render()
        value = ""
        if self.align > len(v):
            value = chr(self.value) * (self.align - len(v))
        elif self.align < len(v) and self.get('expand'):
            # This is a mess, but I just want to sleep...
            d = self.align - (len(v) - (self.align * (len(v) / self.align)))
            d = (len(v) + d) / self.align
            d = (self.align * d) - len(v)
            value = chr(self.value) * d
        else:
            pass

        value = self.apply_transforms(value, True)
        return value

