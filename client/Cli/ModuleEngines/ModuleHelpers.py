import os
import cmd
import sys
import json
import copy
import pprint
import base64
import inspect
import httplib

from OpenSSL import crypto, SSL
from time import gmtime, mktime
from os.path import exists, join

class ModuleHelpers:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def getEngineById(config, engine_id):
        engines = config.get('data').get('engines')
        if not engines: return None
        engine = engines.get(engine_id)
        if not engine: return None
        return engine

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def checkLocalCertificates(config):
        has_certs = True
        if not config.get('data').get('security'):
            config.get('data')['security'] = {}
            has_certs = False

        if not config.get('data').get('security').get('ssl'):
            config.get('data').get('security')['ssl'] = {}
            has_certs = False

        if not config.get('data').get('security').get('ssl').get('certificate_file'):
            config.get('data').get('security').get('ssl')['certificate_file'] = "client.crt"
            has_certs = False

        if not config.get('data').get('security').get('ssl').get('key_file'):
            config.get('data').get('security').get('ssl')['key_file'] = "client.key"
            has_certs = False

        if not config.get('root'):
            print "[e] could not determine FuzzLabs client root path, aborting."
            return

        cf = config.get('root') + "/config/certificates/" +\
             config.get('data').get('security').get('ssl').get('certificate_file')

        kf = config.get('root') + "/config/certificates/" +\
             config.get('data').get('security').get('ssl').get('key_file')

        config.save()

        if not exists(cf) or not exists(kf):
            has_certs = False
        return has_certs

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def createCertificate(engine_id, cf, kf):
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

        try:
            open(cf, 'w').write(
                crypto.dump_certificate(crypto.FILETYPE_PEM, c))
            open(kf, 'w').write(
                crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        except Exception, ex:
            print "[e] failed to create local key file: %s" % str(ex)
            return False

        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def createLocalCertificate(config):
        cf = config.get('root') + "/config/certificates/" +\
             config.get('data').get('security').get('ssl').get('certificate_file')

        kf = config.get('root') + "/config/certificates/" +\
             config.get('data').get('security').get('ssl').get('key_file')

        eid = config.get('data').get('security').get('ssl').get('certificate_file')
        eid = eid.split(".")[0]
        return ModuleHelpers.createCertificate(eid, cf, kf)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    @staticmethod
    def enableEngineSSL(config, engine_id):
        try:
            engine = config.get('data').get('engines').get(engine_id)
            config.get('data').get('engines').get(engine_id)['ssl'] = 1
            config.save()
        except Exception, ex:
            print "[e] failed to enable SSL for engine '%s'" % engine_id
            return False
        return True


