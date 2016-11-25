class CliModuleBase:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, config):
        self.config = config

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def process_help(self, command):
        replaces = [
            ("[MODULE]", self.__class__.__name__.split("Module")[1].lower()),
            ("[NEWLINE]", "\n")
        ]
        help = {}
        help['module'] = self.__class__.__name__.split("Module")[1].lower()
        help['command'] = command
        try:
            command = getattr(self, "cmd_" + command).__doc__
        except Exception, ex:
            return None
        for entry in command.split("@"):
            s = entry.split(":")
            if len(s) < 2: continue
            key = s[0]
            value = ": ".join(s[1:])
            value = value.strip().replace("\r\n", "\n")
            value = value.replace("\n", "\\n")
            value = " ".join(value.split())
            value = value.replace("\\n", "\n")
            for r in replaces:
                value = value.replace(r[0], r[1])
            help[key] = value
        return help

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def cmd_help(self, args):
        """
        @shortdesc: Display information about a given command.
        """
        if type(args) != list: args = args.split()
        if len(args) == 0: return
        help = self.process_help(args[0])
        if not help or len(help) < 1: return
        
        command_help = getattr(self, "cmd_" + args[0]).__doc__

        print 
        print "%s / %s" % (help.get('module'), help.get('command'))
        print "-" * 80

        shortdesc = help.get('shortdesc')
        syntax    = help.get('syntax')
        longdesc  = help.get('longdesc')

        # Probably unformatted help, just try to print standard format
        if not shortdesc:
            if command_help:
                print command_help
                print
                return
        else:
            print help.get('shortdesc')
            print

        if syntax:
            print "Syntax: " + str(help.get('syntax'))
            print

        if longdesc:
            for line in help.get('longdesc').split("\n"):
                print line.strip()
            print 

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def export_do(self, args):
        args = args.split()
        if len(args) == 0: return
        try:
            func = getattr(self, "cmd_" + args[0])
        except Exception, ex:
            print "[e] command '%s' not supported" % args[0]
            return
        func(args[1:])

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def export_help(self):
        print
        print "%-15s\t%s" % ("Command", "Description")
        print "%s" % ("-" * 80)
        for attr in  dir(self):
            if attr.split("_")[0] == "cmd":
                name = attr.split("_")[1]
                doc  = self.process_help(name)
                if not doc: doc = ""
                print "%-15s\t%s" % (name, doc.get('shortdesc'))
        print

