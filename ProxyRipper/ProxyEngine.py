from enum import IntEnum


class AnonymityLevel(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    UNKNOWN = 0

class Protocol(IntEnum):
    SOCKS5 = 1
    SOCKS4 = 2
    HTTP = 3
    HTTPS = 4

    UNKNOWN = 0

class LatencyStatus(IntEnum):
    VERY_GOOD = 1
    GOOD = 2
    MEDIUM = 3
    BAD = 4

class ProxyEngine:

    def setup(self):
        """
        Initialization of api (if needed)
        """
        pass
    
    def scrape(self):
        """
        This Method should return list of ProxyObjects containing proxy information
        """
        pass

    def decideAnonymity(self, anonimityString):
        """
        Function which decided from anonimity keywords ENUM, defaults setted here
        """

        if anonimityString == "elite":
            return AnonymityLevel.HIGH

        if anonimityString == "anonymous":
            return AnonymityLevel.MEDIUM

        if anonimityString == "transparent":
            return AnonymityLevel.LOW
        
        return AnonymityLevel.UNKNOWN
    

    def decideProtocol(self, protocolString):
        """
        Function which decided from protocol keywords ENUM, defaults setted here
        """

        if protocolString == "socks5":
            return Protocol.SOCKS5

        if protocolString == "socks4":
            return Protocol.SOCKS4

        if protocolString == "http":
            return Protocol.HTTP
        
        if protocolString == "https":
            return Protocol.HTTPS

        return Protocol.UNKNOWN

    @staticmethod
    def encodeProtocolBits(protocols):
        bitmask = 0
        for protocol in protocols:
            bitmask |= (1 << protocol.value)
        return bitmask

    @staticmethod
    def checkProtocolExistence(bitmap, protocolSearch):
        return bitmap & (1 << protocolSearch.value) != 0
    
    @staticmethod
    def getLatencyStatus(latency):
        latencystatus = LatencyStatus.VERY_GOOD

        if latency > 100:
            latencystatus = LatencyStatus.GOOD

        if latency > 500:
            latencystatus = LatencyStatus.MEDIUM
        if latency > 700:
            latencystatus = LatencyStatus.BAD

        return latencystatus

    def getCurrentApiName(self):
        """
        Name tag of current scrapping api service
        """
        return ''

class ProxyInfo:

    def __init__(self, ip, port, countryCode, protocol=0, anonLevel=AnonymityLevel.UNKNOWN):
        self.secureLevel = anonLevel
        self.ip = ip
        self.port = port
        self.country = countryCode
        self.protocol = protocol
        self.latency = 0

    def setLatency(self, latency):
        self.latency = latency
