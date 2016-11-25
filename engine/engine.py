#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
import importlib
from OpenSSL import SSL
from flask import Flask
from flask_restful import Api
from classes.Utils import Utils
from classes.Config import Config

ROOT = os.path.dirname(
            os.path.abspath(
                inspect.getfile(inspect.currentframe()
            )))
config = Config(ROOT, "/config/config.json")
endpoints = None
app = Flask(__name__)
api = Api(app)

try:
    endpoints = Utils.read_json(ROOT + "/config/endpoints.json")
except Exception, ex:
    raise Exception('failed to load endpoints configuration: %s' %\
                    str(ex))

for endpoint in endpoints:
    ep_name  = endpoint.keys()[0]
    ep_cname = endpoint[ep_name]
    ep_mod   = importlib.import_module("classes." +\
                                       ep_cname)
    ep_class = getattr(ep_mod, ep_cname)
    api.add_resource(ep_class,
                     ep_name,
                     resource_class_kwargs=config)

def start_engine():
    context = None
    try:
        os.unlink("/tmp/.flenginerestart")
    except Exception, ex:
        pass

    try:
        if config.get('data').get('security').get('ssl').get('enabled') == 1:
            k = config.get('data').get('security').get('ssl').get('key')
            c = config.get('data').get('security').get('ssl').get('certificate')
            context = (c, k)
    except Exception, ex:
        print "[e] failed to set up SSL context"
        pass

    app.run(host=config.get('data').get('general').get('bind'),
            port=config.get('data').get('general').get('port'),
            debug=False,
            ssl_context=context)

    # Check if we have to restart. This custom restart is needed to
    # switch from HTTP to HTTPS once configured.

    r = None
    restart = False
    try:
        r = Utils.read_file("/tmp/.flenginerestart")
    except Exception, ex:
        pass
    if r and r == "restart": restart = True
    return restart

if __name__ == '__main__':
    rc = start_engine()
    while rc:
        rc = start_engine()

