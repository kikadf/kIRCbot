#!/usr/bin/env python3

# commonevents.py, part of kIRCbot
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

import time

import connecting as conn


lasttime = time.time()
sender = ""

def _pong(line):
    conn.s.send(bytes("PONG %s\r\n" % line, "UTF-8"))
    global lasttime
    lasttime = time.time()

def defsender(line):
    global sender
    sender = ""
    for char in line:
        if(char == "!"):
            break
        if(char != ":"):
            sender += char 
