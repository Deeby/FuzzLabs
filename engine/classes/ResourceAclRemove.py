from flask import Flask
from flask import request
from flask_restful import reqparse, abort, Resource
from classes.Utils import Utils

parser = reqparse.RequestParser()
parser.add_argument('apikey',  type=str, required=True, location='args')
parser.add_argument("address", type=str, required=True, 
                    help="address to grant access to")

class ResourceAclRemove(Resource):

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

    def is_allowed(self, address):
        for allowed in self.config.get('data').get('security').get('allow'):
            if allowed.get('address') == address: return True
        return False

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def post(self):
        found = False
        self.check_access()
        args = parser.parse_args(strict=True)
        cnt = 0
        for allowed in self.config.get('data').get('security').get('allow'):
            if allowed.get('address') == args['address']:
                self.config.get('data').get('security').get('allow').pop(cnt)
                found = True
                break
            cnt += 1

        if not found:
            abort(404, message="address not found in ACL")

        Utils.save_file(self.root + "/config/config.json",
                        self.config.get('data'))
        return {"message": "success"}, 200

