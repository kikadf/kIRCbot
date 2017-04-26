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
    # ncore download [url] where
    if (ce.checkarg(args, 0)):
        args0 = args[0]
    else:
        ce.message("Something is missing...")
        ce.message("Use: download or list commands")
        return False

    if (ce.checkarg(args, 1)):
        args1 = args[1]
    else:
        if (args0 == "download"):
            ce.message("Missing url...")
            return False
        elif (args0 == "list"):
            ce.message("Missing list options")
            return False

    if (ce.checkarg(args, 2)):
        args2 = args[2]
    else:
        args2 = None

    if (args0 == "download"):
        if (args2 != None):
            ce.message("fine with specified save dir")
        else:
            ce.message("fine with default save dir")
    elif (args0 == "list"):
        if (args1 == "full"):
            ce.message("full list")
        else:
            ce.message("Missing options (full)")
    else:
        ce.message("Wrong command (download or list)")



# List of useable events
ncoremission_events = {
                        'ncore' : ncore
                      }


ce.eventmerge(ce.events, ncoremission_events)


