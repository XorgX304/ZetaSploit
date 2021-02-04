#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
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

from core.io import io
from core.badges import badges
from core.storage import storage

class pseudo_shell:
    def __init__(self):
        self.io = io()
        self.badges = badges()
        self.storage = storage()
        
        self.execute_method = self.storage.get("pseudo_execute_method")
        self.prompt = 'pseudo % '
        
    def pseudo_shell_header(self):
        self.io.output("")
        self.badges.output_information("--=( Welcome to Pseudo shell )=--")
        self.badges.output_information("Interface for executing commands on the target.")
        self.badges.output_information("Commands are sent to the target via provided execute method.")
        self.io.output("")
        
    def spawn_pseudo_shell(self, execute_method):
        self.badges.output_process("Spawning Pseudo shell...")
        self.badges.output_success("Congratulations, you won Pseudo shell!")
        
        self.pseudo_shell_header()
        self.storage.set("pseudo_execute_method", execute_method)
        
    def execute_pseudo_command(self, command):
        if command == "exit":
            self.storage.delete("pseudo_execute_method")
        else:
            try:
                self.execute_method(command)
            except Exception:
                self.badges.output_error("Failed to use given execute method!")
