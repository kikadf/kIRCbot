#!/usr/bin/env python3

# kircbot.py
# Copyright (C) 2017 : kikadf <kikadf.01@gmail.com>
# Based on ircecho.py
#
# ircecho.py
# Copyright (C) 2011 : Robert L Szkutak II - http://robertszkutak.com
#
# More copyright references: https://gist.github.com/GarrettSocling/371917661f98c6c54beea49de94ce1d9
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
import string

import connecting as c

readbuffer = ""

c.conn2server()

c.join2chan()

while 1:
    readbuffer = readbuffer+c.s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            c.s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        if(line[1] == "PRIVMSG"):
            sender = ""
            for char in line[0]:
                if(char == "!"):
                    break
                if(char != ":"):
                    sender += char 
            size = len(line)
            i = 3
            message = ""
            while(i < size): 
                message += line[i] + " "
                i = i + 1
            message.lstrip(":")
            c.s.send(bytes("PRIVMSG %s %s \r\n" % (sender, message), "UTF-8"))
        for index, i in enumerate(line):
            print(line[index])
