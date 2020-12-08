#!/usr/bin/env python3
"""
<no documentation>
"""

# TODO document ConfigOptions' methods

import logging
import re

from typing import Dict, List, Optional

# ensure the dictionary key has a suitable name
# (this name does not need to match the user-visible name)
RX_CFGOPTIONNAME = re.compile(r"^[\w][\w-]+$")


class ConfigOptions:
    """
    <no documentation>
    """

    def __init__(self):
        """
        <no documentation>
        """
        self.cfgoptions = {}


    def register_cfgoption(self, cfgoption: str, description: str, pattern: str = r".*", default: Optional[str] = None, is_optional: bool = False) -> bool:
        """
        <no documentation>
        """
        lh = logging.getLogger("jacket")
        is_valid = True
        rx_pattern = re.compile(pattern)
        # -- sanity checks -----------------------------------------------
        if not RX_CFGOPTIONNAME.match(cfgoption):
            lh.error("The value '%s' is not a suitable config option name! (must match '%s')", cfgoption, RX_CFGOPTIONNAME)
            is_valid = False
        if not str(description):
            lh.warning("Config option '%s' has no description!", cfgoption)
        if default is not None:
            if not rx_pattern.match(default):
                lh.error("Default value '%s' for config option '%s' fails to match pattern '%s'!", default, cfgoption, pattern)
                is_valid = False
            else:
                lh.debug("Stored default value '%s' for config option '%s'.", default, cfgoption)
        if cfgoption in self.cfgoptions:
            lh.error("Config option '%s' was defined already! Ignoring.", cfgoption)
            is_valid = False
        # -----------------------------------------------------------------
        if is_valid:
            lh.debug("Register config option '%s'.", cfgoption)
            spec = {
                "description": str(description),
                "pattern":     rx_pattern,
                "is_optional": bool(is_optional),
            }
            if default is not None:
                spec["default"] = str(default)
            self.cfgoptions[cfgoption] = spec
            lh.debug("Registered config option '%s': %s", cfgoption, spec)
        else:
            lh.warning("Failed to register config option '%s'!", cfgoption)
        return is_valid


    def get_description(self, cfgoption: str) -> str:
        """
        <no documentation>
        """
        lh = logging.getLogger("jacket")
        try:
            return self.cfgoptions[cfgoption]["description"]
        except KeyError:
            lh.error("Unknown config option '%s'!", cfgoption)
            lh.error("known config options are: %s", ", ".join(self.cfgoptions.keys()))
            raise


    def get_pattern(self, cfgoption: str) -> str:
        """
        <no documentation>
        """
        lh = logging.getLogger("jacket")
        try:
            return self.cfgoptions[cfgoption]["pattern"]
        except KeyError:
            lh.error("Unknown config option '%s'!", cfgoption)
            lh.error("known config options are: %s", ", ".join(self.cfgoptions.keys()))
            raise


    def has_default(self, cfgoption: str) -> bool:
        """
        <no documentation>
        """
        lh = logging.getLogger("jacket")
        try:
            return "default" in self.cfgoptions[cfgoption]
        except KeyError:
            lh.error("Unknown config option '%s'!", cfgoption)
            lh.error("known config options are: %s", ", ".join(self.cfgoptions.keys()))
            raise


    def get_default(self, cfgoption: str) -> str:
        """
        <no documentation>
        """
        lh = logging.getLogger("jacket")
        try:
            return self.cfgoptions[cfgoption]["default"]
        except KeyError:
            lh.error("Unknown config option '%s'!", cfgoption)
            lh.error("known config options are: %s", ", ".join(self.cfgoptions.keys()))
            raise


    def get_defaults(self) -> Dict[str, str]:
        """
        <no documentation>
        """
        defaults = {}
        for cfgoption, record in self.cfgoptions.items():
            if "default" in self.cfgoptions[cfgoption]:
                defaults[cfgoption] = record["default"]
        return defaults


    def get_required_options(self) -> List[str]:
        """
        <no documentation>
        """
        required = []
        for key, record in self.cfgoptions.items():
            if not record["is_optional"]:
                required.append(key)
        return required


    def is_optional(self, cfgoption: str) -> bool:
        """
        <no documentation>
        """
        lh = logging.getLogger("jacket")
        try:
            return self.cfgoptions[cfgoption]["is_optional"]
        except KeyError:
            lh.error("Unknown config option '%s'", cfgoption)
            lh.error("known config options are: %s", ", ".join(self.cfgoptions.keys()))
            raise
