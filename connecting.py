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

import sys
import socket

import config as conf

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn2server():
  s.connect((conf.HOST, conf.PORT))
  s.send(bytes("NICK %s\r\n" % conf.NICK, "UTF-8"))
  s.send(bytes("USER %s %s bla :%s\r\n" % (conf.IDENT, conf.HOST, conf.REALNAME), "UTF-8"))

def join2chan():
  s.send(bytes("JOIN %s\r\n" % conf.CHANNEL, "UTF-8"));
  s.send(bytes("PRIVMSG %s :Hello!\r\n" % conf.MASTER, "UTF-8"))

