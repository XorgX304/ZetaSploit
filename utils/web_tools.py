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

import requests
import url_normalize

class web_tools:
    def head_url(self, url):
        url = self.normalize_url(url)
        return requests.head(url, verify=False).headers
    
    def get_url(self, url):
        url = self.normalize_url(url)
        return requests.get(url, verify=False)
    
    def post_url(self, url, data, headers=None):
        url = self.normalize_url(url)
        if headers:
            return requests.post(url, data=data, headers=headers, verify=False)
        return requests.post(url, data=data, verify=False)
    
    def strip_scheme(self, url):
        url = url.replace('http://', '', 1)
        url = url.replace('https://', '', 1)
        return url.replace('/', '')
    
    def normalize_url(self, url):
        return url_normalize.url_normalize(url)
