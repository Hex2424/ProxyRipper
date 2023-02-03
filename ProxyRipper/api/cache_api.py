from ..ProxyEngine import ProxyEngine, ProxyInfo
import json

CACHE_PATH = "cache.json"

class APICache(ProxyEngine):

    def setup(self):
        self.proxy_list = []
    
    def scrape(self):
        try:
            with open(CACHE_PATH, 'r') as file:
                dictionary = json.load(file)
        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError:
            return []

        for dictionaryItem in dictionary:
            self.proxy_list.append(ProxyInfo(
                dictionaryItem["ip"],
                dictionaryItem["port"],
                dictionaryItem["country"],
                dictionaryItem["protocol"],
                dictionaryItem["anonymity"]))
        
        return self.proxy_list

    def getCurrentApiName(self):
        return "file://"+ CACHE_PATH

        