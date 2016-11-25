import ssl
import json
import uuid
import importlib
import httplib

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
    def read_grammar(filename):
        return Utils.read_grammar(filename)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def from_json(data):
        try:
            data = json.loads(data)
        except Exception, ex:
            raise Exception("failed to parse packet grammar (%s)" % str(ex))
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
    def ssl_verify_callback(conn, x509obj, err_num, err_dep, ret_code):
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def engine_request(config, address, port, robject, engine_id = None):
        ssle = False
        ssl_ctx = None
        if engine_id:
            ssle = config.get('data').get('engines')[engine_id].get('ssl')
            if ssle and ssle == 1:
                ssle = True
                ciphers = [
                    "EECDH+ECDSA+AESGCM"
                    "EECDH+aRSA+AESGCM",
                    "EECDH+ECDSA+SHA384",
                    "EECDH+ECDSA+SHA256",
                    "EECDH+aRSA+SHA384",
                    "EECDH+aRSA+SHA256",
                    "EECDH",
                    "EDH+aRSA",
                    "!aNULL",
                    "!eNULL",
                    "!LOW",
                    "!3DES",
                    "!MD5",
                    "!EXP",
                    "!PSK",
                    "!SRP",
                    "!DSS",
                    "!RC4"
                ]
                ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                ssl_ctx.set_ciphers(":".join(ciphers))
                ssl_ctx.set_ecdh_curve("prime256v1")

        res = None
        headers = {}
        if robject.get('method') in ["PUT", "POST"]:
            headers = {
                "Content-Type": "application/json"
            }

        if not ssle:
            conn = httplib.HTTPConnection(address, port, True, 5)
        else:
            r = config.get('root') + "/config/certificates/"
            k = r + config.get('data').get('security').get('ssl').get('key_file')
            c = r + config.get('data').get('security').get('ssl').get('certificate_file')
            conn = httplib.HTTPSConnection(address, port, k, c, timeout=5, context=ssl_ctx)

        try:
            conn.request(robject.get('method'),
                         robject.get('uri'),
                         json.dumps(robject.get('data')),
                         headers)
            res = conn.getresponse()
        except Exception, ex:
            print "[e] failed to contact engine at %s:%d: %s" %\
                  (address, port, str(ex))
            return False
        callback = robject.get('callback')
        data = json.loads(res.read())
        if callback: callback(res.status, res.reason, data,
                              {"address": address, "port": port})
        return {
            "status": res.status,
            "data": data
        }

