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


lasttime = time.time()
sender = ""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def conn2server(host, port, nick, ident, realname, password):
    s.connect((host, port))
    s.send(bytes("NICK %s\r\n" % nick, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (ident, host, realname), "UTF-8"))
    if password != 0:
        s.send(bytes("PRIVMSG NICKSERV :identify %s\r\n" % password, "UTF-8"))


def join2chan(channel, master):
    s.send(bytes("JOIN %s\r\n" % channel, "UTF-8"))
    s.send(bytes("PRIVMSG %s :Hello%s!\r\n" % (channel, " " + master), "UTF-8"))


def checkconnected(lasttime):
    currenttime = time.time()
    difftime = currenttime - lasttime
    return difftime


def pong(line):
    s.send(bytes("PONG %s\r\n" % line, "UTF-8"))
    global lasttime
    lasttime = time.time()


def defsender(line):
    global sender, lasttime
    sender = ""

    for char in line:
        if(char == "!"):
            break
        if(char != ":"):
            sender += char

    lasttime = time.time()


def message(channel, message):
    s.send(bytes("PRIVMSG %s :%s \r\n" % (channel, message), "UTF-8"))


def quit(channel):
    message(channel, "Bye!")
    s.close()
    raise SystemExit


def checkarg(list, index):
    try:
        t = list[index]
    except IndexError:
        return '3'   
    else:
        return '%s' % index

