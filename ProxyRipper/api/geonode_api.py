from ..ProxyEngine import ProxyEngine, ProxyInfo
import requests

PAGE_LIMIT = 500
ENDPOINT = "https://proxylist.geonode.com/api/proxy-list"
PARAMS = {
    "limit" : PAGE_LIMIT,
    "page" : 1,
    "sort_by" : "lastChecked",
    "sort_type" : "desc"
}




class APIGeonode(ProxyEngine):

    def setup(self):
        self.proxy_list = []
    
    def scrape(self):
        """
        This Method should return list of ProxyObjects containing proxy information
        """
        try:
            response = requests.get(ENDPOINT, params=PARAMS, timeout=10)
        except Exception:
            return []
            
        if response.status_code != 200:
            return []

        json_responses = response.json()["data"]

        for proxy_info in json_responses:
            self.proxy_list.append(ProxyInfo(
                proxy_info["ip"],
                proxy_info["port"],
                proxy_info["country"],
                self.encodeProtocolBits([self.decideProtocol(pt) for pt in proxy_info["protocols"]]),
                self.decideAnonymity(proxy_info["anonymityLevel"])
            ))
        
        return self.proxy_list

    def getCurrentApiName(self):
        return ENDPOINT