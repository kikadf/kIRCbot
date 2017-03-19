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

import config as conf
import commonevents as ce


readbuffer = ""


def connecting():
    conf.checkconf(conf.config_path, conf.config_file)
    conf.k_password("kIRCbot", conf.IDENT)
    ce.conn2server(conf.HOST, conf.PORT, conf.NICK, conf.IDENT, conf.REALNAME, conf.PASSWORD)
    ce.join2chan(conf.CHANNEL, conf.MASTER)


connecting()

while 1:
    readbuffer = readbuffer + ce.s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop( )

    if conn.checkconnected(ce.lasttime) > 300:
        print('Reconnect...')
        ce.s.close()
        connecting()

    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            ce.pong(line[1])

        if(line[1] == "PRIVMSG"):
            ce.defsender(line[0])

            size = len(line)
            i = 3
            message = ""
            while(i < size): 
                message += line[i] + " "
                i = i + 1
            message.lstrip(":")
            ce.message(ce.sender, message)

        for index, i in enumerate(line):
            print(line[index])
