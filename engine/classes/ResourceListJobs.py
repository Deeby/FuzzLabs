from flask import Flask
from flask import request
from flask_restful import reqparse, abort, Resource
from classes.Utils import Utils

parser = reqparse.RequestParser()
parser.add_argument('apikey', type=str, required=True, location='args')

class ResourceListJobs(Resource):

    def __init__(self, **kwargs):
        self.root   = kwargs.get('root')
        self.config = kwargs

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
            abort(403, message="access blocked by ACL")

        if not args.get('apikey') or args.get('apikey') != apikey:
            abort(401, message="access denied")

    def get(self):
        self.check_access()
        jobs = []
        files = Utils.list_directory("./jobs")
        for file in files:
            f = file.split('.')
            if f[1] != "job": continue
            j_data = Utils.read_json("./jobs/" + file)
            if not j_data.get('id'): continue
            jobs.append(j_data.get('id'))
        return {"message": jobs}, 200

