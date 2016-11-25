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

class ResourceInitAcl(Resource):

    def __init__(self, **kwargs):
        self.root   = kwargs.get('root')
        self.config = kwargs

    def get(self):
        client = request.remote_addr

        # If for whatever reason we do not have a security key
        # it will be created here.

        if not self.config.get('data').get('security'):
            self.config.get('data')['security'] = {}

        # Check ACL. If there is not one, create one.

        allow = self.config.get('data').get('security').get('allow')
        if not allow:
            allow = self.config.get('data')['security']['allow'] = []

        if len(allow) > 0:
            abort(403, message="ACL already initialized")

        self.config.get('data')['security']['allow'].append({
            "address": client
        })

        # Save changes

        Utils.save_file(self.root + "/config/config.json",
                        self.config.get('data'))

        # And return the API key to the client

        return {"message": "success"}, 200

