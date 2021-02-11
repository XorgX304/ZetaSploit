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

import socket
import requests
import url_normalize

class web_tools:
    def send_head_to_url(self, url):
        url = self.normalize_url(url)
        return requests.head(url, verify=False).headers
    
    def send_get_to_url(self, url):
        url = self.normalize_url(url)
        return requests.get(url, verify=False)
    
    def send_post_to_url(self, url, data, buffer_size=1024):
        remote_host, remote_port = self.get_host(url), self.get_port(url)
        output = self.send_port_to_host(remote_host, remote_port, data, buffer_size)
        return output
    
    def send_post_to_host(self, remote_host, remote_port, data, buffer_size=1024):
        sock = socket.socket()
        sock.connect((remote_host, int(remote_port)))
        sock.send(data.encode())
        output = sock.recv(buffer_size)
        sock.close()
        return output.decode().strip()
    
    def get_url_port(self, url):
        url = self.strip_scheme(url)
        return url.split(':')[1]
        
    def get_url_host(self, url):
        url = self.strip_scheme(url)
        return url.split(':')[0]
    
    def strip_scheme(self, url):
        url = url.replace('http://', '', 1)
        url = url.replace('https://', '', 1)
        return url.split('/')[0]
    
    def normalize_url(self, url):
        return url_normalize.url_normalize(url)
