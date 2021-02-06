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

import sys

sys.stdout.write("\033]0;ZetaSploit Framework\007")

import os
import readline

from core.io import io
from core.tip import tip
from core.jobs import jobs
from core.execute import execute
from core.loader import loader
from core.config import config
from core.badges import badges
from core.banner import banner
from core.storage import storage
from core.modules import modules
from core.exceptions import exceptions

class console:
    def __init__(self):
        self.io = io()
        self.tip = tip()
        self.jobs = jobs()
        self.execute = execute()
        self.loader = loader()
        self.config = config()
        self.badges = badges()
        self.banner = banner()
        self.storage = storage()
        self.modules = modules()
        self.exceptions = exceptions()

    def check_root(self):
        if os.getuid() == 0:
            return True
        self.badges.output_error("Operation not permitted!")
        return False
    
    def check_install(self):
        if os.path.exists(self.config.path_config['base_paths']['root_path']):
            return True
        self.badges.output_error("ZetaSploit is not installed!")
        self.badges.output_information("Consider running ./install.sh")
        return False

    def start_zsf(self):
        try:
            self.loader.load_all()
        except Exception:
            sys.exit(1)

    def launch_menu(self):
        while True:
            try:
                if not self.modules.check_current_module():
                    prompt = '(zsf)> '
                else:
                    module = self.modules.get_current_module_name()
                    name = self.modules.get_platform(module) + '/' + self.modules.get_name(module)
                    prompt = '(zsf: ' + self.modules.get_category(module) + ': ' + self.badges.RED + self.badges.BOLD + name + self.badges.END + ')> '
                commands, arguments = self.io.input(prompt)
                
                self.jobs.stop_dead()
                self.execute.execute_command(commands, arguments)

            except (KeyboardInterrupt, EOFError):
                self.badges.output_empty("")
            except self.exceptions.GlobalException:
                pass
            except Exception as e:
                self.badges.output_error("An error occurred: " + str(e) + "!")
            
    def launch_shell(self):
        readline.read_history_file(self.config.path_config['base_paths']['history_path'])
        readline.write_history_file(self.config.path_config['base_paths']['history_path'])
        readline.parse_and_bind("tab: complete")
        
        version = self.config.core_config['details']['version']
        codename = self.config.core_config['details']['codename']
        if self.config.core_config['console']['clear']:
            self.execute.execute_system("clear")

        if self.config.core_config['console']['banner']:
            self.banner.print_random_banner()
        
        if self.config.core_config['console']['header']:
            plugins = self.storage.get("plugins")
            modules = self.storage.get("modules")
            
            plugins_total = 0
            modules_total = 0
            
            if plugins:
                for database in plugins.keys():
                    plugins_total += len(plugins[database])
            if modules:
                for database in modules.keys():
                    for module_category in modules[database].keys():
                        for module_platform in modules[database][module_category].keys():
                            modules_total += len(modules[database][module_category][module_platform])

            header = ""
            header += f"{self.badges.END}\n"
            if codename and not codename.isspace():
                header += f"    --=( {self.badges.YELLOW}ZetaSploit Framework {codename} {version}{self.badges.END}\n"
            else:
                header += f"    --=( {self.badges.YELLOW}ZetaSploit Framework {version}{self.badges.END}\n"
            header += f"--==--=( Developed by EntySec ({self.badges.LINE}https://entysec.netlify.app/{self.badges.END})\n"
            header += f"    --=( {modules_total} modules loaded | {plugins_total} plugins available\n"
            header += f"{self.badges.END}"
            self.badges.output_empty(header)
            
        if self.config.core_config['console']['tip']:
            self.tip.print_random_tip()
            self.badges.output_empty("")

    def shell(self):
        self.start_zsf()
        self.launch_shell()
        self.launch_menu()
