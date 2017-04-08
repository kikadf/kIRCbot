#!/usr/bin/env python3

# sample.py, part of kIRCbot
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


SAMPLE = None

# Function to read the plugin's part in config file
def sample_readconf(config):
    print("Read config of Sample plugin")
    ce.parser.read(config)

    global SAMPLE

    try:
        SAMPLE = ce.parser['Sample options']['What']
    except configparser.NoOptionError:
        print("No options for Sample plugin")


# To get the plugin's configuration values
sample_readconf(ce.config_file)


# The plugin's event functions
def sample():
    ce.message("Read your own, check plugins/sample.py.")


# List of useable events
events = {
            'sample' : sample
         }

