import ProxyEngine

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
PURPLE = '\033[95m'
UNDERLINE = '\033[4m'



DEFAULT_COLOR = ENDC
PROTOCOL_COLOR = OKBLUE
IP_COLOR = DEFAULT_COLOR
PORT_COLOR = DEFAULT_COLOR
ANONYMITY_COLOR = OKCYAN
COUNTRY_COLOR = PURPLE
NEW_PARAGRAPH_COLOR = PURPLE

API_ETA_COLOR = OKCYAN
API_NAME_COLOR = OKGREEN

LATENCY_GOOD = OKGREEN 
LATENCY_VERYGOOD = OKGREEN
LATENCY_MEDIUM = WARNING
LATENCY_BAD = FAIL


ANONYMITY_HIGH_CHAR = '\u2162'
ANONYMITY_MEDIUM_CHAR = '\u2161'
ANONYMITY_LOW_CHAR = '\u2160'
ANONYMITY_UNKNOWN_CHAR = ' '



SEPERATOR = ''

def printProxyInfo(proxyObject):

    printProtocols(proxyObject.protocol)
    printLatency(proxyObject.latency)
    printAnonymity(proxyObject.secureLevel)
    printCountry(proxyObject.country)
    printAddress(proxyObject)
    
    print()

def printProtocols(protocolBitmap):

    print(f"{DEFAULT_COLOR}[{PROTOCOL_COLOR}", end='')

    if ProxyEngine.ProxyEngine.checkProtocolExistence(protocolBitmap, ProxyEngine.Protocol.SOCKS5):
        print(ProxyEngine.Protocol.SOCKS5.name, end='')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(protocolBitmap, ProxyEngine.Protocol.SOCKS4):
        print(ProxyEngine.Protocol.SOCKS4.name, end='')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(protocolBitmap, ProxyEngine.Protocol.HTTP):
        print(f"{ProxyEngine.Protocol.HTTP.name}  ", end='')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(protocolBitmap, ProxyEngine.Protocol.HTTPS):
        print(f"{ProxyEngine.Protocol.HTTPS.name} ", end='')

    else:
        print(ProxyEngine.Protocol.UNKNOWN.name, end='')

    print(f"{DEFAULT_COLOR}]", end=SEPERATOR)


def printAddress(object):
    print(f"{DEFAULT_COLOR}[{IP_COLOR}{object.ip}:{PORT_COLOR}{object.port}{DEFAULT_COLOR}]", end=SEPERATOR)

def printLatency(latency):

    print(f"{DEFAULT_COLOR}[", end='')
    
    if(ProxyEngine.ProxyEngine.getLatencyStatus(latency) == ProxyEngine.LatencyStatus.VERY_GOOD):
        print(LATENCY_VERYGOOD, end='')

    elif(ProxyEngine.ProxyEngine.getLatencyStatus(latency) == ProxyEngine.LatencyStatus.GOOD):
        print(LATENCY_GOOD, end='')

    elif(ProxyEngine.ProxyEngine.getLatencyStatus(latency) == ProxyEngine.LatencyStatus.MEDIUM):
        print(LATENCY_MEDIUM, end='')

    elif(ProxyEngine.ProxyEngine.getLatencyStatus(latency) == ProxyEngine.LatencyStatus.BAD):
        print(LATENCY_BAD, end='')
    print(f"{latency}ms{DEFAULT_COLOR}]", end=SEPERATOR)

def printAnonymity(anonimity):

    print(f"{DEFAULT_COLOR}[{ANONYMITY_COLOR}", end='')
    
    if anonimity == ProxyEngine.AnonymityLevel.HIGH:
        print(ANONYMITY_HIGH_CHAR, end='')
        
    elif anonimity == ProxyEngine.AnonymityLevel.MEDIUM:
        print(ANONYMITY_MEDIUM_CHAR, end='')

    elif anonimity == ProxyEngine.AnonymityLevel.LOW:
        print(ANONYMITY_LOW_CHAR, end='')
    
    else:
        print(ANONYMITY_UNKNOWN_CHAR, end='')

    print(f"{DEFAULT_COLOR}]", end=SEPERATOR)

def printCountry(country):
    print(f"{DEFAULT_COLOR}[{COUNTRY_COLOR}{country}{DEFAULT_COLOR}]", end=SEPERATOR)
    

def printCurrentApi(name, scrapped, max):
    print(f"{DEFAULT_COLOR}[{API_ETA_COLOR}>>{DEFAULT_COLOR}][{API_NAME_COLOR}{name}{DEFAULT_COLOR}][{API_ETA_COLOR} {scrapped} / {max}{DEFAULT_COLOR} ]\n")

def printUrlCheck(url, proxyCount, passed, inprogress):
    print(f"{DEFAULT_COLOR}[{API_ETA_COLOR}>>{DEFAULT_COLOR}][{API_NAME_COLOR}{url}{DEFAULT_COLOR}][{API_ETA_COLOR} {proxyCount} {DEFAULT_COLOR}][", end='')
    if inprogress:
        print(f"{API_ETA_COLOR}CHECK{DEFAULT_COLOR}]", end=SEPERATOR)
    else:
        if passed:
            print(f"{LATENCY_GOOD}PASS{DEFAULT_COLOR}]       ", end=SEPERATOR) 
        else:
            print(f"{LATENCY_BAD}FAIL{DEFAULT_COLOR}]        ", end=SEPERATOR)

def replaceLine():
    print(end='\r')

def newParagraph(name):
    print(f"\n\n[ {NEW_PARAGRAPH_COLOR}{name}{DEFAULT_COLOR} ]:\n")
