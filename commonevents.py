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
import socket
import sys
import os
import shutil
import configparser
import keyring
import getpass


home = os.path.expanduser("~")
config_path = '%s/.config/kircbot' % home
config_file = '%s/config.ini' % config_path
plugins_path = './plugins'
parser = configparser.ConfigParser()
lasttime = time.time()
#sender = ""
s = socket.socket()


HOST = PORT = CHANNEL = NICK = IDENT = REALNAME = MASTER = REGISTERED = PLUGINS = None


# Functions for configuration
def readconnconf(config):
    print("Used config: %s" % config)
    parser.read(config)

    global HOST, PORT, CHANNEL, NICK, IDENT, REALNAME, MASTER, REGISTERED, PLUGINS

    HOST = parser['Server and channel options']['Host']
    PORT = int(parser['Server and channel options']['Port'])
    CHANNEL = parser['Server and channel options']['Channel']
    NICK = parser['ID options']['Nick']
    IDENT = parser['ID options']['Ident']
    REALNAME = parser['ID options']['Realname']
    MASTER = parser['ID options']['Master'].split(',')
    PLUGINS = parser['Main options']['Plugins'].split(',')
    try:
        REGISTERED = int(parser['ID options']['Registered'])
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


# To get values from config.ini
checkconf(config_path, config_file)


# Functions for password handling
def k_setpassword(service, username):
    print('Set password for %s.' % username)
    password = getpass.getpass(prompt='Password: ', stream=None)
    keyring.set_password(service, username, password)
    return password


def k_password(service, username):
    if REGISTERED == 1:
        password = keyring.get_password(service, username)

        if password is None:
            password = k_setpassword(service, username)

        return password

    elif REGISTERED == 2:
        password = k_setpassword(service, username)

        print("Edit config: %s" % config_file)
        shutil.copyfile(config_file, config_file + '.old')
        parser.read(config_file)
        parser['ID options']['Registered'] = '1'
        fileout = open(config_file, 'w')
        parser.write(fileout)
        fileout.close()

        return password


# Functions for connection
def conn2server(host = HOST, port = PORT, ident = IDENT, realname = REALNAME, registered = REGISTERED):
    s.connect((host, port))
    s.send(bytes("NICK %s\r\n" % ident, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (ident, host, realname), "UTF-8"))
    if registered is not None:
        password = k_password("kIRCbot", ident)
        s.send(bytes("PRIVMSG NICKSERV :identify %s\r\n" % password, "UTF-8"))


def join2chan(channel = CHANNEL, nick = NICK):
    s.send(bytes("NICK %s\r\n" % nick, "UTF-8"))
    s.send(bytes("JOIN %s\r\n" % channel, "UTF-8"))
    s.send(bytes("PRIVMSG %s :Hello!\r\n" % channel, "UTF-8"))


def conns():
    conn2server()
    time.sleep(20) # Must give enough time, while logging, because of +i server mode.
    join2chan()    # After logged, succesfull join. Invite exception: /mode #channel +I $a:ident


def checkconnected(lsttime):
    currenttime = time.time()
    difftime = currenttime - lsttime
    return difftime


def activation():
    global lasttime
    lasttime = time.time()


def pong(line):
    s.send(bytes("PONG %s\r\n" % line, "UTF-8"))
    activation()


# Functions to working
def defsender(line):
    sender = ""
    for char in line:
        if(char == "!"):
            break
        if(char != ":"):
            sender += char
    return sender


def message(message, channel = CHANNEL):
    s.send(bytes("PRIVMSG %s :%s \r\n" % (channel, message), "UTF-8"))
    activation()


def checkarg(list, index):
    try:
        t = list[index]
    except IndexError:
        return False
    else:
        return True


def eventhandler(word, args):
    event = events['%s' % word]
    event(args)


def pluginhandler(plugins = PLUGINS):
    used_plugins = []
    for i in plugins:
        if os.path.isfile('%s/%s.py' % (plugins_path, i)):
            print("Use %s plugin." % i)
            used_plugins.append('%s' % i)
        else:
            print("Not found %s plugin." % i)
    return used_plugins


def eventconvert(dict):
    for key, value in dict.items():
        dict[key] = "sample." + key
    return dict


def eventmerge(basedict, newdict):
    basedict.update(newdict)


# Main event functions
def quit(args):
    message("Bye!")
    s.send(bytes("QUIT\r\n", "UTF-8"))
    raise SystemExit


def restart(args):
    message("brb")
    s.send(bytes("QUIT\r\n", "UTF-8"))
    os.execv(sys.executable, ['python'] + sys.argv)


def _events(args):
    message(list(events.keys()))


def test1(args):
    message("test1, yoo")


def test2(args):
    message("test2 wazze")


# List of useable events
events = {
            'test1' : test1,
            'test2' : test2,
            'exit' : quit,
            'restart' : restart,
            'events' : _events
         }


from plugins import *

