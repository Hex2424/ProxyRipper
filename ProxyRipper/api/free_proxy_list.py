import ProxyEngine
import requests
from bs4 import BeautifulSoup

ENDPOINT = "https://free-proxy-list.net"
TIMEOUT = 10

class APIFreeProxyList(ProxyEngine.ProxyEngine):

    def setup(self):
        self.proxy_list = []
    
    def scrape(self):
        """
        This Method should return list of ProxyObjects containing proxy information
        """
        try:
            response = requests.get(ENDPOINT, timeout=TIMEOUT)
  
            soup = BeautifulSoup(response.text, "html.parser")

            rows = soup.find("tbody").find_all("tr")
       
        except Exception:
            return []
            
        if response.status_code != 200:
            return []
        for row in rows:
            cols = row.find_all("td")
            self.proxy_list.append(ProxyEngine.ProxyInfo(
            cols[0].text,
            cols[1].text,
            cols[2].text,
            self.encodeProtocolBits([ProxyEngine.Protocol.HTTPS if cols[6].text == 'yes' else ProxyEngine.Protocol.UNKNOWN]),
            self.decideAnonymity(cols[4].text.strip())
            ))

        return self.proxy_list

    def decideAnonymity(self, anonimityString):

        if anonimityString == "elite proxy":
            return ProxyEngine.AnonymityLevel.HIGH

        if anonimityString == "anonymous":
            return ProxyEngine.AnonymityLevel.MEDIUM

        if anonimityString == "transparent":
            return ProxyEngine.AnonymityLevel.LOW
        
        return ProxyEngine.AnonymityLevel.UNKNOWN

    def getCurrentApiName(self):
        return ENDPOINT