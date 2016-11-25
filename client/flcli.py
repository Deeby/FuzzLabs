#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cmd
import sys
import glob
import pprint
import inspect
import importlib

from Classes.Config import Config

__VERSION__ = "0.0.1"
INTRO="""
                                                                                 
 _|_|_|_|                                _|                  _|                  
 _|        _|    _|  _|_|_|_|  _|_|_|_|  _|          _|_|_|  _|_|_|      _|_|_|  
 _|_|_|    _|    _|      _|        _|    _|        _|    _|  _|    _|  _|_|      
 _|        _|    _|    _|        _|      _|        _|    _|  _|    _|      _|_|  
 _|          _|_|_|  _|_|_|_|  _|_|_|_|  _|_|_|_|    _|_|_|  _|_|_|    _|_|_|    
                                                                                 
"""

ROOT_DIR = os.path.dirname(
                os.path.abspath(
                    inspect.getfile(inspect.currentframe()
                )))

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Cli(cmd.Cmd):
    intro  = INTRO + 'FuzzLabs Fuzzing Framework ' + __VERSION__
    ruler = '-'
    prompt = 'fuzzlabs > '

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, completekey='tab', stdin = None, stdout = None):
        self.config = Config(ROOT_DIR, "/config/config.json")
        self.load_cli_modules()
        cmd.Cmd.__init__(self, completekey, stdin, stdout)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def load_cli_modules(self):
        for cmodule in glob.glob(ROOT_DIR + "/Cli/Module*"):
            m_parts    = cmodule.split("/")
            m_name     = m_parts[len(m_parts) - 1]
            m_cmdname  = m_name[6:].lower()
            m_path     = "/".join(m_parts[:-1]) + "/"
            m_mod      = None
            m_inst     = None
            try:
                m_mod = importlib.import_module("Cli." + m_name + "." + m_name)
            except Exception, ex:
                print "[e] CLI module '%s' is invalid: %s" % (m_name, str(ex))
                continue

            try:
                m_inst = getattr(m_mod, m_name)(self.config)
            except Exception, ex:
                print "[e] CLI module '%s' error: %s" % (m_name, str(ex))
                continue

            for m in inspect.getmembers(m_inst, predicate=inspect.ismethod):
                m_name = m[0].split("_")
                if m_name[0] != "export": continue
                if m_name[1] == "do":
                    setattr(self, m_name[1] + "_" + m_cmdname, m[1])
                if m_name[1] == "help":
                    setattr(self, m_name[1] + "_" + m_cmdname, m[1])

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def get_names(self):
        return dir(self)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_exit(self, arg):
        'Exit FuzzLabs.'
        sys.exit(0)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def do_quit(self, arg):
        'Exit FuzzLabs.'
        sys.exit(0)

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    Cli().cmdloop()

