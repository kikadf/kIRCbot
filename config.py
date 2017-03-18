#!/usr/bin/env python3

# config.py, part of kIRCbot
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
import keyring
import getpass

home = os.path.expanduser("~")
config_path = '%s/.config/kircbot' % home
config_file = '%s/config.ini' % config_path
parser = configparser.ConfigParser()
HOST = PORT = CHANNEL = NICK = IDENT = REALNAME = MASTER = ""
REGISTERED = PASSWORD = 0


def readconnconf(config):
    print("Used config: %s" % config)
    parser.read(config)

    global HOST, PORT, CHANNEL, NICK, IDENT, REALNAME, MASTER
    global REGISTERED

    HOST = parser.get('Server and channel options', 'Host')
    PORT = parser.getint('Server and channel options', 'Port')
    CHANNEL = parser.get('Server and channel options', 'Channel')
    NICK = parser.get('ID options', 'Nick')
    IDENT = parser.get('ID options', 'Ident')
    REALNAME = parser.get('ID options', 'Realname')
    MASTER = parser.get('ID options', 'Master')
    try:
        REGISTERED = parser.getint('ID options', 'Registered')
    except configparser.NoOptionError:
        print('Use %s without identify.' % IDENT)


def checkconf(path, config):
    if not os.path.isfile(config):
        print("Not found config file, copy the default.")
        os.makedirs(path, exist_ok=True)
        shutil.copyfile('default.ini', config)

    readconnconf(config)

    for i in HOST, PORT, CHANNEL, NICK, IDENT, REALNAME, MASTER:
        if i == '"CHANGETHIS"':
            sys.exit("Must to edit %s" % config)


def k_setpassword(service, username):
    global PASSWORD

    PASSWORD = getpass.getpass(prompt='Password: ', stream=None)
    print('Set password for %s.' % IDENT)
    keyring.set_password(service, username, PASSWORD)


def k_password(service, username):
    global PASSWORD

    if REGISTERED == 1:
        PASSWORD = keyring.get_password(service, username)

        if PASSWORD == None:
            k_setpassword(service, username)

    elif REGISTERED == 2:
        k_setpassword(service, username)
        print("Edit config: %s" % config_file)
        shutil.copyfile(config_file, config_file + '.old')
        parser.read(config_file)
        parser.set('ID options', 'Registered', '1')
        fileout = open(config_file, 'w')
        parser.write(fileout)
        fileout.close()

    else:
        PASSWORD = 0


