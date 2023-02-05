
import ProxyEngine
import requests

ENDPOINT = 'https://api.proxyscrape.com/v2/'
TIMEOUT = 10000

PARAMS = {
    "request" : "displayproxies",
    "protocol" : None,              # for now none
    "timeout" : TIMEOUT,
    "country" : "all",
    "ssl" : "all",
    "anonymity" : "all"
}

TIMEOUT = 10

class APIProxyScrape(ProxyEngine.ProxyEngine):

    def setup(self):
        self.proxy_list = []
    
    def scrape(self):
        """
        This Method should return list of ProxyObjects containing proxy information
        """
        for protocol in ['socks4', 'socks5', 'http', 'https']:
            try:
                PARAMS["protocol"] = protocol                   # setting protocol on each request so we know
                response = requests.get(ENDPOINT, params=PARAMS, timeout=TIMEOUT)
            except Exception:
                return []
                
            if response.status_code != 200:
                return []

            if '\n' not in response.text:
                return []

            for row in response.text.split('\n'):
                if ':' not in row:
                    continue

                ip, port = row.split(':')

                self.proxy_list.append(ProxyEngine.ProxyInfo(
                ip,
                port,
                "--",
                self.encodeProtocolBits([self.decideProtocol(protocol)]),
                ProxyEngine.AnonymityLevel.UNKNOWN))

        return self.proxy_list

    def getCurrentApiName(self):
        return ENDPOINT