#!/usr/bin/env python3

# kircbot.py, part of kIRCbot
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

import commonevents as ce


readbuffer = ""


ce.conns()

while 1:
    readbuffer = readbuffer + ce.s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop( )

    if ce.checkconnected(ce.lasttime) > 500:
        ce.restart()

    for line in temp:
        print(line)
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            ce.pong(line[1])

        if(line[1] == "PRIVMSG"):
            ce.activation()
            if(line[3].strip(":") == ce.NICK):
                ce.defsender(line[0])
                calledevent = line[ce.checkarg(line, 4)]
                if( calledevent in ce.events and ce.sender in ce.MASTER ):
                    ce.eventhandler(calledevent, line[5:])
                else:
                    ce.message("WTF?")

