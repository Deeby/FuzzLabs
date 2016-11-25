from primitives.__primitive import __primitive__

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
        "values": 0,
        "default": 0,
        "error": "primitive is non-fuzzable"
    }
]

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class static(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent = None):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        value = super(static, self).render()
        return str(value)

