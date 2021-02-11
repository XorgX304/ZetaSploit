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

from requests.packages.urllib3.exceptions import InsecureRequestWarning

class web_tools:
    def __init__(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    #
    # Functions to send something to URL
    #
    
    def send_head_to_url(self, url, path=None):
        url = self.normalize_url(url)
        if path:
            if not path.startswith('/') and not url.endswith('/'):
                path = '/' + path
            url += path
        try:
            response = requests.head(url, verify=False).headers
        except Exception:
            return None
        return response
    
    def send_get_to_url(self, url, path=None):
        url = self.normalize_url(url)
        if path:
            if not path.startswith('/') and not url.endswith('/'):
                path = '/' + path
            url += path
        try:
            response = requests.get(url, verify=False)
        except Exception:
            return None
        return response
    
    def send_post_to_url(self, url, path=None, data):
        url = self.normalize_url(url)
        if path:
            if not path.startswith('/') and not url.endswith('/'):
                path = '/' + path
            url += path
        try:
            response = requests.post(url, data, verify=False)
        except Exception:
            return None
        return response
    
    #
    # Functions to send something to host and port
    #
    
    def send_post_to_host(self, remote_host, remote_port, data, buffer_size=1024):
        sock = socket.socket()
        sock.connect((remote_host, int(remote_port)))
        sock.send(data.encode())
        output = sock.recv(buffer_size)
        sock.close()
        return output.decode().strip()
    
    #
    # Functions to parse host and port
    #
    
    def format_host_and_port(self, remote_host, remote_port):
        return remote_host + ':' + remote_port
    
    #
    # Functions to parse URL
    #
    
    def craft_url(self, remote_host, remote_port):
        url = remote_host + ':' + remote_port
        return self.normalize_url(url)
    
    def get_url_port(self, url):
        url = self.strip_scheme(url)
        return url.split(':')[1]
        
    def get_url_host(self, url):
        url = self.strip_scheme(url)
        return url.split(':')[0]
    
    def strip_scheme(self, url, strip_path=True):
        url = url.replace('http://', '', 1)
        url = url.replace('https://', '', 1)
        if strip_path:
            url = url.split('/')[0]
        return url
    
    def normalize_url(self, url):
        url = self.strip_scheme(url, False)
        url = 'http://' + url
        return url

    #
    # Functions to get something from URL
    #
    
    def get_url_server(self, url):
        header = self.send_head_to_url(url)
        if header:
            if 'Server' in header.keys():
                return header['Server']
        return None
