import base64
import socket
from flask import Flask
from flask import request
from flask_restful import reqparse, abort, Resource
from classes.Utils import Utils
from OpenSSL import crypto, SSL

parser = reqparse.RequestParser()
parser.add_argument('apikey', type=str, required=True, location='args')
parser.add_argument('enable', type=int, required=True, location='args')
parser.add_argument("client", type=str, required=False, help="client certificate")
parser.add_argument("id",     type=str, required=False, help="engine UUID")

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class ResourceSetupSsl(Resource):

    def __init__(self, **kwargs):
        self.root   = kwargs.get('root')
        self.config = kwargs

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def check_access(self):
        client = request.remote_addr
        args   = parser.parse_args(strict=True)
        allow  = self.config.get('data').get('security').get('allow')
        apikey = self.config.get('data').get('security').get('apikey')

        allow = self.config.get('data')['security'].get('allow')
        if not allow:
            abort(500, message="invalid configuration")
        allowed = False
        if allow:
            allowed = False
            for c in allow:
                if c.get('address') and c.get('address') == request.remote_addr:
                    allowed = True
        if not allowed:
            abort(403, message="access blocked due to ACL")

        if not args.get('apikey') or args.get('apikey') != apikey:
            abort(401, message="access denied")

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def write_cert(self, fpath, data):
        try:
            open(fpath, 'w').write(data)
        except Exception, ex:
            print "[e] failed to save certificate: %s" % str(ex)
            return False
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def save_certificate(self, client, ctype, data):
        cert_root = self.root + "/config/certificates/"
        fpath = None
        if ctype == "client": 
            fpath = cert_root + client + ".crt"
        elif ctype == "cert":
            fpath = cert_root + "engine.crt"
        elif ctype == "key":
            fpath = cert_root + "engine.key"
        else:
            return False

        if not self.write_cert(fpath, data): return False
        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def create_certificate(self, engine_id):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        c = crypto.X509()
        c.get_subject().C = "UK"
        c.get_subject().ST = "London"
        c.get_subject().L = "London"
        c.get_subject().O = "DCNWS"
        c.get_subject().OU = "DCNWS"
        c.get_subject().CN = engine_id
        c.set_serial_number(1000)
        c.gmtime_adj_notBefore(0)
        c.gmtime_adj_notAfter(10*365*24*60*60)
        c.set_issuer(c.get_subject())
        c.set_pubkey(k)
        c.sign(k, 'sha1')

        cert_root = self.root + "/config/certificates/"
        try:
            open(cert_root + "engine.crt", 'w').write(
                crypto.dump_certificate(crypto.FILETYPE_PEM, c))
            open(cert_root + "engine.key", 'w').write(
                crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        except Exception, ex:
            print "[e] failed to create certificate and key files: %s" % str(ex)
            return False

        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def post(self):
        self.check_access()
        args = parser.parse_args(strict=True)

        if args.get('enable') == 0:
            cert_root = self.root + "/config/certificates/"
            self.config.get('data').get('security').get('ssl')['enabled'] = 0
            Utils.save_file(self.root + "/config/config.json",
                            self.config.get('data'))
            open("/tmp/.flenginerestart", "w").write("restart")
            func = request.environ.get('werkzeug.server.shutdown')
            func()
        elif args.get('enable') == 1:
            client = None

            if not args.get('client') or not args.get('id'):
                abort(400, message="invalid payload")

            try:
                client = base64.b64decode(args.get('client'))
            except Exception, ex:
                abort(400, message="failed to decode payload: " % str(ex))

            rc = True
            try:
                rc = self.create_certificate(args.get('id'))
            except Exception, ex:
                abort(400, message="failed to create engine certificate: %s" %\
                           str(ex))

            if not rc:
                abort(400, message="failed to generate engine certificates")

            rc = True
            try:
                rc = self.save_certificate(request.remote_addr, "client", client)
            except Exception, ex:
                abort(400, message="failed to set up certificates: " % str(ex))

            if not rc:
                abort(400, message="failed to set up certificates")

            cert_root = self.root + "/config/certificates/"
            self.config.get('data').get('security')['ssl'] = {}
            self.config.get('data').get('security').get('ssl')['enabled'] = 1
            self.config.get('data').get('security').get('ssl')['certificate'] = cert_root + "engine.crt"
            self.config.get('data').get('security').get('ssl')['key'] = cert_root + "engine.key"
            for acle in self.config.get('data').get('security').get('allow'):
                if acle.get('address') and acle.get('address') == request.remote_addr:
                    acle['certificate'] = cert_root + request.remote_addr + ".crt"

            Utils.save_file(self.root + "/config/config.json",
                            self.config.get('data'))
        else:
            abort(400, message="invalid request")

        try:
            engine_certificate = Utils.read_file(self.config.get('data').get('security').get('ssl')['certificate'])
        except Exception, ex:
            abort(500, message="failed to read engine certificate")

        open("/tmp/.flenginerestart", "w").write("restart")
        func = request.environ.get('werkzeug.server.shutdown')
        func()
        return {"message": "success", 
                "certificate": base64.b64encode(engine_certificate)}, 200

