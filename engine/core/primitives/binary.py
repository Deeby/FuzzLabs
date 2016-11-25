import copy
from primitives.__primitive import __primitive__

all_properties = [
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    },
    {
        "name": "value",
        "type": "list",
        "mandatory": 1,
        "error": "primitive requires value to be of type list"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 0,
        "error": "primitive is non-fuzzable"
    }
]

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class binary(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent = None):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)
        if self.get('fuzzable'):
            self.original_value = copy.deepcopy(self.value)
            self.library_index  = 0

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):
        if self.get('fuzzable'):
            self.library = [0x00, 0x01, 0xFF, 0xFE, 0x7F]

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        if self.get('fuzzable'):
            if self.mutation_index == len(self.value) - 1:
                self.value = copy.deepcopy(self.original_value)
                self.complete = True

            if self.complete == True: return

            if self.library_index == len(self.library):
                self.value = copy.deepcopy(self.original_value)
                self.library_index = 0
                self.mutation_index += 1
            self.value[self.mutation_index] = self.library[self.library_index]
            self.library_index += 1

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        # This primitive does not support transforms
        value = "".join(map(chr, self.value))
        return str(value)

