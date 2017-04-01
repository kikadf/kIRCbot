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
parser = configparser.ConfigParser()
lasttime = time.time()
sender = ""
s = socket.socket()


HOST = PORT = CHANNEL = NICK = IDENT = REALNAME = MASTER = ""
REGISTERED = PASSWORD = 0


def readconnconf(config):
    print("Used config: %s" % config)
    parser.read(config)

    global HOST, PORT, CHANNEL, NICK, IDENT, REALNAME, MASTER
    global REGISTERED

    HOST = parser['Server and channel options']['Host']
    PORT = int(parser['Server and channel options']['Port'])
    CHANNEL = parser['Server and channel options']['Channel']
    NICK = parser['ID options']['Nick']
    IDENT = parser['ID options']['Ident']
    REALNAME = parser['ID options']['Realname']
    MASTER = parser['ID options']['Master'].split(',')
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


def k_setpassword(service, username):
    global PASSWORD

    print('Set password for %s.' % username)
    PASSWORD = getpass.getpass(prompt='Password: ', stream=None)
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
        parser['ID options']['Registered'] = '1'
        fileout = open(config_file, 'w')
        parser.write(fileout)
        fileout.close()

    else:
        PASSWORD = 0



# To get values from config.ini
checkconf(config_path, config_file)
k_password("kIRCbot", IDENT)



def conn2server(host = HOST, port = PORT, ident = IDENT, realname = REALNAME, password = PASSWORD):
    s.connect((host, port))
    s.send(bytes("NICK %s\r\n" % ident, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (ident, host, realname), "UTF-8"))
    if password != 0:
        s.send(bytes("PRIVMSG NICKSERV :identify %s\r\n" % password, "UTF-8"))


def join2chan(channel = CHANNEL, nick = NICK):
    s.send(bytes("NICK %s\r\n" % nick, "UTF-8"))
    s.send(bytes("JOIN %s\r\n" % channel, "UTF-8"))
    s.send(bytes("PRIVMSG %s :Hello!\r\n" % channel, "UTF-8"))


def conns():
    conn2server()
    time.sleep(15) # Must give enough time, while logging, because of +i server mode.
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


def defsender(line):
    global sender
    sender = ""

    for char in line:
        if(char == "!"):
            break
        if(char != ":"):
            sender += char

    activation()


def message(message, channel = CHANNEL):
    s.send(bytes("PRIVMSG %s :%s \r\n" % (channel, message), "UTF-8"))
    activation()


def quit():
    message("Bye!")
    raise SystemExit


def restart():
    message("brb")
    s.send(bytes("QUIT\r\n", "UTF-8"))
    os.execv(sys.executable, ['python'] + sys.argv)


def checkarg(list, index):
    try:
        t = list[index]
    except IndexError:
        return 3
    else:
        return '%s' % index


def test1():
    print(">>> %s" % IDENT)
    s.send(bytes("PRIVMSG NICKSERV INFO %s\r\n" % IDENT, "UTF-8"))


def test2():
    s.send(bytes("PRIVMSG NICKSERV INFO %s\r\n" % NICK, "UTF-8"))


def eventhandler(word):
    event = events['%s' % word]
    event()

events = {
            'test1' : test1,
            'test2' : test2,
            'exit' : quit,
            'restart' : restart
         }
