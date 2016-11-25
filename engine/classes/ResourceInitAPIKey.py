from flask import Flask
from flask import request
from flask_restful import reqparse, abort, Resource
from classes.Utils import Utils

parser = reqparse.RequestParser()

"""
 Either a users sets the API key via the configuration file locally, or
 it will be set the first time the client contacts the engine.

 Usage of this resource assumes that at the time of the engine setup and
 registration the environment is not hostile.
"""

class ResourceInitAPIKey(Resource):

    def __init__(self, **kwargs):
        self.root   = kwargs.get('root')
        self.config = kwargs

    def get(self):

        # If for whatever reason we do not have a security key
        # it will be created here.

        if not self.config.get('data').get('security'):
            abort(500, message="invalid configuration")

        # Check ACL

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

        # Check API key. If there is one set we return error here.

        apikey = self.config.get('data').get('security').get('apikey')
        if apikey and len(apikey) > 0:
            abort(403, message="api key already set")

        # If there was no API key set we generate a new one here.

        if not apikey or len(apikey) == 0:
            apikey = Utils.generate_name()
            self.config.get('data')['security']['apikey'] = apikey

        # Finally, we save the updated configuration

        Utils.save_file(self.root + "/config/config.json",
                        self.config.get('data'))

        # And return the API key to the client

        return {"message": "success", "apikey": apikey}, 200

