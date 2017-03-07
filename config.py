#!/usr/bin/env python3

# config.py
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

import sys
import os
import shutil
import configparser

parser = configparser.ConfigParser()

home = os.path.expanduser("~")
config_path = '%s/.config/kircbot' % home
config_file = '%s/config.ini' % config_path

needcopy = "Not found config file, copy the default."
neededit = "Must to edit %s" % config_file
usedconf = "Used config: %s" % config_file

HOST = PORT = CHANNEL = NICK = IDENT = REALNAME = MASTER = 0

def readconnconf():
  parser.read(config_file)

  global HOST, PORT, CHANNEL, NICK, IDENT, REALNAME, MASTER

  HOST = parser.get('Server and channel options', 'Host')
  PORT = parser.getint('Server and channel options', 'Port')
  CHANNEL = parser.get('Server and channel options', 'Channel')
  NICK = parser.get('ID options', 'Nick')
  IDENT = parser.get('ID options', 'Ident')
  REALNAME = parser.get('ID options', 'Realname')
  MASTER = parser.get('ID options', 'Master')

def checkconf():
  for i in HOST, PORT, CHANNEL, NICK, IDENT, REALNAME, MASTER:
    if i == '"CHANGETHIS"':
      sys.exit(neededit)

def copyconf():
  os.makedirs(config_path, exist_ok=True)
  shutil.copyfile('default.ini', '% s' % config_file)

