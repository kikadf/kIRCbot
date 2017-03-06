#!/usr/bin/env python3

# connecting.py
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

import socket

HOST = "CHANGETHIS"
PORT = 6667
CHANNEL = "CHANGETHIS"

NICK = "CHANGETHIS"
IDENT = "CHANGETHIS"
REALNAME = "CHANGETHIS"
MASTER = "CHANGETHIS"

s = socket.socket( )

def conn2server():
  s.connect((HOST, PORT))

  s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
  s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))

def join2chan():
  s.send(bytes("JOIN %s\r\n" % CHANNEL, "UTF-8"));
  s.send(bytes("PRIVMSG %s :Hello!\r\n" % MASTER, "UTF-8"))

