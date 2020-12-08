#!/usr/bin/env python3
#
# <no description>
#
# TODO document functions

import argparse
import logging
import re

import cfgopts

from typing import Dict, List, Optional


def parse_environment(cfg_opts: cfgopts.ConfigOptions, map_cfg2env: Dict[str, str], environment: Dict[str, str]) -> Dict[str, str]:
    """
    <no documentation>
    """
    lh = logging.getLogger("jacket")
    config = {}
    for cfgoption, env_var in map_cfg2env.items():
        if env_var in environment:
            rx_valid_value = cfg_opts.get_pattern(cfgoption)
            if rx_valid_value.match(environment[env_var]):
                config[cfgoption] = environment[env_var]
            else:
                lh.warning("Found an invalid value in environment variable '%s'! Ignoring.", env_var)
        else:
            lh.debug("Found no value for environment variable '%s' (%s).", env_var, cfgoption)
    return config


def parse_commandline(cfg_opts: cfgopts.ConfigOptions, parser: argparse.ArgumentParser, arguments: List[str]) -> Dict[str, str]:
    """
    <no documentation>
    """
    lh = logging.getLogger("jacket")
    config = {}
    parsed = vars(parser.parse_args(args=arguments[1:]))
    lh.warning("parse_commandline(): parsed = %s", parsed)
    for cfgoption, value in parsed.items():
        lh.warning("parse_commandline(): %s = %s", cfgoption, value)
        if value is not None:
            rx_valid_value = cfg_opts.get_pattern(cfgoption)
            if rx_valid_value.match(str(value)):
                config[cfgoption] = value
            else:
                lh.warning("Found an invalid value for command line argument '%s'! Ignoring.", cfgoption)
        else:
            lh.debug("Found no value for command line argument '%s'.", cfgoption)
    lh.warning("parse_commandline(): %s", config)
    return config


def find_missing(cfg_opts: cfgopts.ConfigOptions, config: Dict[str, str]) -> List[str]:
    """
    <no documentation>
    """
    """
    find required variables that are missing
    """
    missing = []
    for cfgoption in cfg_opts.get_required_options():
        if cfgoption not in config:
            missing.append(cfgoption)
    return missing
