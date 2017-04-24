#!/usr/bin/env python3

# plugins/ncore.py, part of kIRCbot
# Copyright (C) 2017 : kikadf <kikadf.01@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. 

import configparser
import commonevents as ce


TARGET = USER = None

# Function to read the plugin's part in config file
def ncoremission_readconf(config):
    print("Read config by nCore-Transmission plugin")
    ce.parser.read(config)

    global TARGET, USER

    try:
        TARGET = ce.parser['nCore-Transmission options']['Target']
        USER = ce.parser['nCore-Transmission options']['User']
    except KeyError:
        True
    except configparser.NoOptionError:
        print("Not found options for nCore-Transmission plugin")


# To get the plugin's configuration values
ncoremission_readconf(ce.config_file)


# The plugin's event functions
def ncore(args):
    ce.message("nCore")


# List of useable events
ncoremission_events = {
                        'sample' : ncore
                      }


ce.eventmerge(ce.events, ncoremission_events)


