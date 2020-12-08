#!/usr/bin/env python3
#
# <no description>
#
# TODO show registered environment vatiables in help message
# code does not indicate environment variables (use argoparse's epilog?)
# -------------------------------------------------------------------------
# # % ./update_new-relic-users.py3
# usage: update_new-relic-users.py3 [-h] account_dir
# update_new-relic-users.py3: error: the following arguments are required: account_dir
# -------------------------------------------------------------------------
#
# TODO document CliParser's methods

import argparse
import logging
import re

import cfgopts
import helpers

from typing import Dict, List, Optional


class CliParser:

    #def __init__(self, configoptions: cfgopts.ConfigOptions, description: str, version: Optional[str] = None):
    def __init__(self, configoptions, description: str, version: Optional[str] = None):
        """
        <no documentation>
        """
        self.cfgopts   = configoptions
        self.env_vars  = {}
        self.arguments = {}
        self.parser    = argparse.ArgumentParser(description=description, allow_abbrev=False)


    def define_environment_variable(self, cfgoption: str, name: str) -> bool:
        """
        <no documentation>
        """
        lh = logging.getLogger("jacket")
        is_registered = False
        if variable not in self.env_vars:
            self.env_vars[cfgoption] = name
            is_registered = True
        else:
            lh.warning("Environment variable '%s' was registered already! Ignoring.", variable)
        return is_registered


    def define_flag_argument(self, cfgoption: str, long_name: str, short_name: Optional[str] = None, repeatable: bool = False) -> bool:
        """
        <no documentation>
        """
        is_registered = False
        if cfgoption not in self.arguments:
            names = []
            if short_name is not None:
                names.append(short_name)
            names.append(long_name)
            description = self.cfgopts.get_description(cfgoption)
            if repeatable:
                self.parser.add_argument(*names, dest=cfgoption, action='count', default=0, help=description)
                self.arguments[cfgoption] = names
            else:
                self.parser.add_argument(*names, dest=cfgoption, action='store_const', const=1, default=0, help=description)
                self.arguments[cfgoption] = names
            is_registered = True
        else:
            lh.warning("Argument '%s' was registered already! Ignoring.", variable)
        return is_registered


    def define_named_argument(self, cfgoption: str, long_name: str, short_name: Optional[str] = None, delimiter: Optional[str] = None) -> bool:
        """
        <no documentation>
        """
        is_registered = False
        if cfgoption not in self.arguments:
            names = []
            if short_name is not None:
                names.append(short_name)
            names.append(long_name)
            description = self.cfgopts.get_description(cfgoption)
            if self.cfgopts.has_default(cfgoption):
                description += " (default: " + self.cfgopts.get_default(cfgoption) + ")"
            params = {
                "dest": cfgoption,
                "type": str,
                "help": description,
            }
            self.parser.add_argument(*names, **params)
            self.arguments[cfgoption] = names
            is_registered = True
        else:
            lh.warning("Argument '%s' was registered already! Ignoring.", variable)
        return is_registered


    def define_positional_argument(self, cfgoption: str) -> bool:
        """
        <no documentation>
        """
        is_registered = False
        if cfgoption not in self.arguments:
            description = self.cfgopts.get_description(cfgoption)
            if self.cfgopts.has_default(cfgoption):
                description += " (default: " + self.cfgopts.get_default(cfgoption) + ")"
            params = {
                "dest": cfgoption,
                "type": str,
                "help": description,
            }
            if self.cfgopts.is_optional(cfgoption):
                params["nargs"] = "?"
            self.parser.add_argument(**params)
            self.arguments[cfgoption] = cfgoption
            is_registered = True
        else:
            lh.warning("Argument '%s' was registered already! Ignoring.", variable)
        return is_registered


    def parse_and_verify(self, environment: Dict[str, str], arguments: List[str]) -> Optional[Dict[str, str]]:
        """
        parses the environment variables and command line arguments and verifies
        the provided values are correct and complete

        (returns 'None' if required variables are missing)
        """
        lh = logging.getLogger("jacket")
        # -----------------------------------------------------------------
        config = self.cfgopts.get_defaults()
        lh.warning("defaults: %s", config)
        config.update(helpers.parse_environment(self.cfgopts, self.env_vars, environment))
        lh.warning("with env: %s", config)
        config.update(helpers.parse_commandline(self.cfgopts, self.parser, arguments))
        lh.warning("final:    %s", config)
        # -----------------------------------------------------------------
        missing = helpers.find_missing(self.cfgopts, config)
        if not missing:
            return config
        else:
            for cfgoption in missing:
                cfgoption_names = []
                if cfgoption in self.env_vars:
                    cfgoption_names.extend(self.env_vars[cfgoption])
                if cfgoption in self.arguments:
                    cfgoption_names.extend(self.arguments[cfgoption])
                cfgoption_names_str = "/".join(cfgoption_names)
                lh.error("Required config option '%s' is missing! Please set %s.", cfgoption, cfgoption_names_str)
            return None
