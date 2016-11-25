import os
import json
import uuid
import inspect
import importlib

# =============================================================================
#
# =============================================================================

class Utils:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def read_file(filename):
        data = None
        try:
            with open(filename, 'r') as f:
                data = f.read()
        except Exception, ex:
            raise Exception("failed to load file (%s)" % str(ex))
        return data

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def read_json(filename):
        data = Utils.read_file(filename)
        return Utils.from_json(data)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def save_file(filename, content, tojson = True):
        try:
            with open(filename, 'w') as f:
                if tojson:
                    content = json.dumps(content)
                f.write(content)
        except Exception, ex:
            raise Exception("failed to write file: %s (%s)" %\
                           (filename, str(ex)))
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def from_json(data):
        try:
            data = json.loads(data)
        except Exception, ex:
            raise Exception("failed to parse data (%s)" % str(ex))
        return data

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def bin_to_dec(binary):
        '''
        Convert a binary string to a decimal number.
        @type  binary: String
        @param binary: Binary string
        @rtype:  Integer
        @return: Converted bit string
        '''

        return int(binary, 2)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def generate_name():
        return str(uuid.uuid4())

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def integer_boundaries(library, max_num, integer):
        '''
        Add the supplied integer and border cases to the integer fuzz
        heuristics library.
        @type  integer: Int
        @param integer: Integer to append to fuzz heuristics
        '''
        ilist = []
        for i in xrange(-10, 10):
            case = integer + i
            if 0 > case or case > max_num: continue
            if case in library: continue
            ilist.append(case)
        return ilist

    @staticmethod
    def getRoot():
        return os.path.dirname(
                os.path.abspath(
                    inspect.getfile(inspect.currentframe()
        ) + "/../../"))

