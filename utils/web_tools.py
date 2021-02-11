import requests
import url_normalize

class web_tools:
    def head_url(self, url):
        url = self.normalize_url(url)
        return requests.head(url, verify=False).headers
    
    def get_url(self, url):
        url = self.normalize_url(url)
        return requests.get(url, verify=False)
    
    def post_url(self, url, data):
        url = self.normalize_url(url)
        return requests.post(url, data, verify=False)
    
    def strip_scheme(self, url):
        url = url.replace('http://', '', 1)
        url = url.replace('https://', '', 1)
        return url.replace('/', '')
    
    def normalize_url(self, url):
        return url_normalize.url_normalize(url)
