__VERSION__ = "0.0.1"

import copy
import base64

from Classes.Utils import Utils
from Cli.CliModuleBase import CliModuleBase
from ModuleHelpers import ModuleHelpers

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class ModuleEngines(CliModuleBase):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def callbackAclInit(self, status, reason, data, engine):
        if (status != 200):
            print "[e] failed to add engine: %s" % data.get('message')

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def callbackGetApiKey(self, status, reason, data, engine):
        if (status != 200):
            print "[e] failed to add engine: %s" % data.get('message')
        else:
            apikey = data.get('apikey')
            if not apikey:
                print "[e] failed to add engine: %s" %\
                      "no API key in response"
                return

            if not self.config.get('data').get('engines'):
                self.config.get('data')['engines'] = {}
            id = Utils.generate_name()
            self.config.get('data').get('engines')[id] = {
                "address": engine.get('address'),
                "port": engine.get('port'),
                "apikey": apikey
            }
            self.config.save()

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def cmd_list(self, args):
        """
        @shortdesc: List registered engines.
        @longdesc: 
        Provides a list of engines that have been registered using the 'engines
        add' method. The output of the command shows the following details per
        registered engine:

        - engine ID: A unique ID that can be used to reference the engine.
        - Address:   The IP address or host name of the engine.
        - Port:      The port the engine is accepting connections on.
        - SSL:       Whether SSL is enabled or not.
        - API key:   The API key used as authentication secret.
        - Status:    Indicates whether the engine is active or offline.

        @syntax:    [MODULE] list
        """
        engines = self.config.get('data').get('engines')
        if not engines or len(list(engines)) == 0:
            print "[i] no engines registered"
            return

        print
        for engine in engines:
            status = "unknown"
            engine_data = self.config.get('data').get('engines')[engine]

            rc = Utils.engine_request(self.config,
                                     engine_data['address'],
                                     engine_data['port'],
            {
                "method": "GET",
                "uri": "/management/ping?apikey=" + engine_data['apikey'],
                "data": None
            }, engine)
            if rc:
                if rc.get('status') == 200 and \
                   rc.get('data').get('message') == "pong":
                    status = "active"

            ssls = "Yes" if engine_data.get('ssl') == 1 else "No"
            print "id: " + engine
            print "  %-10s: %-40s" % ("Address", engine_data['address'])
            print "  %-10s: %-40s" % ("Port", str(engine_data['port']))
            print "  %-10s: %-40s" % ("SSL", ssls)
            print "  %-10s: %-40s" % ("Api key", str(engine_data['apikey']))
            print "  %-10s: %-40s" % ("Status", status)
            print

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def cmd_add(self, args):
        """
        @shortdesc: Add a new engine.
        @longdesc: 
        To be able to manage engines, engines have to be registered using the
        'add' command. Once an engine is registered it receives a unique ID
        that can be used to reference the engine when using the other engine
        management commands. To register an engine, the following details have
        to be provided:

        - Address:   The IP address or host name of the engine.
        - Port:      The port the engine is listening on. (default: 26000)

        @syntax:    [MODULE] add <address> <port>
        """
        initialization = [
            {"method": "GET", "uri": "/setup/acl",
             "callback": self.callbackAclInit},
            {"method": "GET", "uri": "/setup/apikey",
             "callback": self.callbackGetApiKey}
        ]

        if type(args) != list: args = args.split(" ")
        if len(args) < 1:
            print "[e] invalid syntax"
            return
        address = args[0]
        port = 26000
        if len(args) == 2:
            try:
                port = int(args[1])
            except:
                print "[e] invalid port number"
                return

        error = False
        for robject in initialization:
            rc = Utils.engine_request(self.config,
                                     address,
                                     port,
                                     robject,
                                     None)
            if rc:
                rc = rc.get('status')
                if rc != 200:
                    error = True
                    break
            else:
                error = True
                break

        if not error:
            print "[e] engine '%s:%d' added successfully" %\
                  (address, port)
        else:
            print "[e] failed to add engine '%s:%d'" %\
                  (address, port)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def cmd_shutdown(self, args):
        """
        @shortdesc: Shut down an engine.
        @longdesc:
        The 'shutdown' command can be used to send a shutdown message resulting
        in the termination of the engine. The function accepts the following
        parameters:

        - engine ID: A unique ID that can be used to reference the engine.

        @syntax:    [MODULE] shutdown <engine ID>
        """
        engine = ModuleHelpers.getEngineById(self.config, args[0])
        if not engine:
            print "[e] engine not found"
            return

        rc = Utils.engine_request(self.config,
                                 engine.get('address'),
                                 engine.get('port'),
        {
            "method": "GET",
            "uri": "/management/shutdown?apikey=" + engine['apikey'],
            "data": None
        }, args[0])
        if rc:
            if rc.get('status') == 200:
                print "[i] engine shut down"

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def cmd_remove(self, args):
        """
        @shortdesc: Remove an engine.
        @longdesc:
        The 'remove' command can be used to remove an engine from the client's
        database. The function accepts the following parameters:

        - abandon:   Clear the engine configuration and remove from database.
        - terminate: Clear configuration, remove from datbase and shut down.
        - engine ID: A unique ID that can be used to reference the engine.

        @syntax:    [MODULE] remove < abandon | terminate >  <engine ID>
        """
        if type(args) != list: args = args.split(" ")
        if len(args) != 2:
            print "[e] syntax error"
            return

        engine = ModileHelpers.getEngineById(self.config, args[1])
        if not engine:
            print "[e] engine not found"
            return

        uri = None
        if args[0] == "abandon":
            uri = "/management/remove?terminate=false&apikey=" + engine['apikey']
        elif args[0] == "terminate":
            uri = "/management/remove?terminate=true&apikey=" + engine['apikey']
        else:
            print "[e] invalid option '%s'" % args[0]
            print "[e] valid options are 'abandon' or 'terminate'"
            return

        rc = Utils.engine_request(self.config,
                                 engine.get('address'),
                                 engine.get('port'),
        {
            "method": "GET",
            "uri": uri,
            "data": None
        }, args[1])
        if rc:
            if rc.get('status') == 200:
                engines_list = copy.deepcopy(self.config.get('data').get('engines'))
                for engine in engines_list:
                    if engine == args[1]:
                        self.config.get('data').get('engines').pop(engine)
                self.config.save()
                print "[i] engine removed"
            else:
                print "[i] failed to remove engine: %s" %\
                      rc.get('data').get('message')

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def cmd_ssl(self, args):
        """
        @shortdesc: Manage engine SSL settings.
        @longdesc:
        The 'ssl' command can be used to manage the SSL configuration of the
        registered engines. Enabling or disabling SSL has an immediate effect
        and does not require restart or the engine or the client.
        The function accepts the following parameters:

        - enable:    Enable SSL support for the engine.
        - disable:   Disable SSL support for the engine.
        - engine ID: A unique ID that can be used to reference the engine.

        @syntax:    [MODULE] ssl < enable | disable >  <engine ID>
        """
        if type(args) != list: args = args.split(" ")
        if len(args) != 2:
            print "[e] syntax error"
            return

        engine = ModuleHelpers.getEngineById(self.config, args[1])
        if not engine: return

        uri = None
        if args[0] == "enable":
            # Make sure we got our local cert and key
            if not ModuleHelpers.checkLocalCertificates(self.config):
                if not ModuleHelpers.createLocalCertificate(self.config):
                    print "[e] failed to create certificates"
                    return
            # Not sure if I want to have CA cert and sign each cert with
            # that. Probably would make things simpler, but... will see.
            cert_root = self.config.get('root') + "/config/certificates/"
            ccf = cert_root + self.config.get('data').get('security').get('ssl').get('certificate_file')

            try:
                client = Utils.read_file(ccf)
            except Exception, ex:
                print "[e] failed to read certificates: %s" % str(ex)
                return

            # read in certs, base64 and include
            r_object_data = {
                "client": base64.b64encode(client),
                "id": args[1]
            }

            r_object = {
                "method": "POST",
                "uri": "/setup/ssl?enable=1&apikey=" + engine.get('apikey'),
                "data": r_object_data
            }

            rc = Utils.engine_request(self.config,
                                     engine.get('address'),
                                     engine.get('port'),
                                     r_object,
                                     args[1])
            if not rc:
                print "[e] certificate distribution failed"
                return
            sc = rc.get('status')
            if sc != 200:
                print "[e] certificate distribution failed: %s" % rc.get('data').get('message')
                return

            engine_cert = rc.get('data').get('certificate')
            if not engine_cert:
                print "[e] certificate distribution failed: no certificate received from engine"
                return

            try:
                engine_cert = base64.b64decode(engine_cert)
            except Exception, ex:
                print "[e] invalid engine certificate received: %s" % str(ex)
                return

            try:
                Utils.save_file(cert_root + args[1] + ".crt", engine_cert, False)
            except Exception, ex:
                print "[e] failed to save engine certificate: %s" % str(ex)
                return

            ModuleHelpers.enableEngineSSL(self.config, args[1])

        elif args[0] == "disable":
            r_object = {
                "method": "POST",
                "uri": "/setup/ssl?enable=0&apikey=" + engine.get('apikey'),
                "data": None
            }

            rc = Utils.engine_request(self.config,
                                     engine.get('address'),
                                     engine.get('port'),
                                     r_object,
                                     args[1])
            if not rc:
                print "[e] failed to disable SSL on engine '%s'" % args[1]
                return
            sc = rc.get('status')
            if sc != 200:
                print "[e] failed to disable SSL on engine '%s': %s" %\
                      (args[1], rc.get('data').get('message'))
                return

            self.config.get('data').get('engines').get(args[1])['ssl'] = 0
            self.config.save()
        else:
            print "[e] invalid option '%s'" % args[0]
            return

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def cmd_acl(self, args):
        """
        @shortdesc: Manage engine ACL settings.
        @longdesc:
        The 'acl' command can be used to manage the Access Control List (ACL)
        settings of registered engines. The ACL is a list maintained by each
        engine and consist of one or more IP addresses that are allowed to
        communicate with the engine.
        The function accepts the following parameters:

        - list:      List the ACL entries for a given engine.
        - add:       Add a new item to the ACL list.
        - remove:    Remove an item from the ACL list.
        - engine ID: A unique ID that can be used to reference the engine.

        @syntax:    [MODULE] acl [ list | <add | remove >  <engine ID> ]
        """

        """
        @shortdesc: Manage engine ACL settings.
        """
        engine_id = None
        command   = None
        address   = None
        if type(args) != list: args = args.split(" ")
        if args < 2:
            print "[e] syntax error"
            self.help_acl()
            return

        try:
            engine_id = args[0]
            command   = args[1]
            if command in ["add", "remove"]:
                address = args[2]
        except Exception, ex:
            print "[e] syntax error"
            self.help_acl()
            return

        engine = ModuleHelpers.getEngineById(self.config, engine_id)
        if not engine: return

        if command == "list":
            r_object = {
                "method": "GET",
                "uri": "/management/acl/list?apikey=" + engine.get('apikey'),
                "data": None
            }

            rc = Utils.engine_request(self.config,
                                      engine.get('address'),
                                      engine.get('port'),
                                      r_object,
                                      engine_id)
            if not rc:
                print "[e] failed to retrieve ACL"
                return
            if rc.get('status') != 200:
                print "[e] failed to retrieve ACL: %s" % rc.get('data').get('message')
                return

            allowed_list = rc.get('data').get('message')
            if len(allowed_list) == 0:
                print "ACL empty for engine '%s'" % engine_id
                return

            print
            print "%-15s\t%s" % ("Client", "Certificate")
            print "-" * 80
            for allowed in allowed_list:
                cp = allowed.get('certificate')
                if not cp:
                    cp = "Not set"
                else:
                    cp = "/config/" + "".join(cp.split("config/")[1])
                print "%-15s\t%s" % (allowed.get('address'), cp)
            print
        elif command == "add":
            r_object = {
                "method": "POST",
                "uri": "/management/acl/add?apikey=" + engine.get('apikey'),
                "data": {"address": address}
            }

            rc = Utils.engine_request(self.config,
                                      engine.get('address'),
                                      engine.get('port'),
                                      r_object,
                                      engine_id)
            if not rc:
                print "[e] failed to update ACL"
                return
            if rc.get('status') != 200:
                print "[e] failed to update ACL: %s" % rc.get('data').get('message')
                return
        elif command == "remove":
            r_object = {
                "method": "POST",
                "uri": "/management/acl/remove?apikey=" + engine.get('apikey'),
                "data": {"address": address}
            }

            rc = Utils.engine_request(self.config,
                                      engine.get('address'),
                                      engine.get('port'),
                                      r_object,
                                      engine_id)
            if not rc:
                print "[e] failed to update ACL"
                return
            if rc.get('status') != 200:
                print "[e] failed to update ACL: %s" % rc.get('data').get('message')
                return
        else:
            print "[e] invalid action requested"
            return

