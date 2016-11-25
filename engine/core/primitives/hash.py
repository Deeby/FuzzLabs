import zlib
import hashlib
import binascii
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
        "name": "type",
        "type": "str",
        "default": "crc32",
        "mandatory": 0,
        "error": "primitive requires type to be of type str"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0],
        "default": 0,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
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
        "default": "little",
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

class hash(__primitive__):

    """
     NOTE: Hash always has to be outside of the target block.
    """

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent = None):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)
        self.ignore = True
        supported = [ "crc32", "md5", "sha1", "sha224", "sha256", "sh384",
                      "sha512" ]

        if self.get('type') not in supported:
            raise Exception('unsupported hash type requested')

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def swap_endian(self, value):
        return "".join(list(reversed(value)))

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        b = self.search(self.block)
        v = b.render()

        t = self.get('type')

        # Let's assume everything is little endian because who the hell knows
        # and why would any libs mention this?

        endian = "<"
        if self.get('endian') == 'big': endian = '>'

        value = None
        if t == "adler32":
            value = zlib.adler32(v) & 0xFFFFFFFFL
            value = struct.pack(endian+"L", value)
        elif t == "crc32":
            value = zlib.crc32(v) & 0xFFFFFFFFL
            value = struct.pack(endian+"L", value)
        elif t == "md5":
            value = hashlib.md5(v).digest()
        elif t == "sha1":
            value = hashlib.sha1(v).digest()
        elif t == "sha224":
            value = hashlib.sha224(v).digest()
        elif t == "sha256":
            value = hashlib.sha256(v).digest()
        elif t == "sha384":
            value = hashlib.sha384(v).digest()
        elif t == "sha512":
            value = hashlib.sha512(v).digest()
        else:
            raise Exception('unsupported hash type requested')

        # Let's assume everything is little endian above because who the hell 
        # knows, and why would any libs mention this?

        if t not in ['adler32', 'crc32']:
            if self.get('endian') == 'big': value = self.swap_endian(value)
        if self.get('format') == 'ascii': value = binascii.hexlify(value)
        self.value = value
        value = super(hash, self).render()
        return value

