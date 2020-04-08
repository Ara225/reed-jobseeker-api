import requests
from pprint import pprint

class ReedAPI():
    def __init__(self, apikey, apiurl='https://www.reed.co.uk/api/1.0'):
        self.apikey = apikey
        self.apiurl = apiurl
    
    def search(self, **kwargs):
        searchURL = self._generateURL(kwargs, self.apiurl + '/search?')
        response = requests.get(searchURL, auth=(self.apikey, ''))


    def _generateURL(self, kwargs, URLBase):
        count = 0
        for arg in kwargs:
            value = str(kwargs[arg]).replace(' ', '%20').replace('True', 'true').replace('False', 'false')
            if count == 0:
                URLBase += arg + '=' + value
            else:
                URLBase += '&' + arg + '=' + value
            count += 1
        return URLBase
        
        