import requests
import ProxyEngine
from threading import Thread

def check_proxy(object,check_url, timeout, attempts, callback, isAsync=False):

    STATUS = None
    protocol_list = getProtocolsList(object.protocol)
    dummy = ProxyEngine.ProxyEngine()
    for _ in range(attempts):
        
        for protocol_string in protocol_list:
            try:
                # print(f"{protocol_string}://{object.ip}:{object.port}")
                response = requests.get(check_url, proxies={
                    'https': f"{protocol_string}://{object.ip}:{object.port}",
                    'http' : f"{protocol_string}://{object.ip}:{object.port}"
                }, timeout=timeout)
                
                if (response.status_code == 200):

                    # setting latency
                    object.setLatency(round(response.elapsed.microseconds / 1000))

                    # changing protocol to the one who was valid one
                    object.protocol = ProxyEngine.ProxyEngine.encodeProtocolBits([dummy.decideProtocol(protocol_string)])
                    if isAsync:
                        callback(object)
                        return
                    else:
                        return object
                else:
                    print(response.status_code)
                    STATUS = None
            except requests.exceptions.ConnectTimeout:
                STATUS = None
            except requests.exceptions.ConnectionError:
                STATUS = None
            except requests.exceptions.ReadTimeout:
                STATUS = None
            except Exception as e:
                print(e)
                STATUS = None
        # print("checked")
    if isAsync:
        callback(STATUS)
        return
    else:
        return STATUS

def checkUrl(url, timeout):
    try:
        return requests.get(url, timeout=timeout).status_code
    except Exception:
        return 404

def getProtocolsList(bitmap):
    protocols = []

    if ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.SOCKS5):
        protocols.append('socks5')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.SOCKS4):
        protocols.append('socks4')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.HTTP):
        protocols.append('http')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.HTTPS):
        protocols.append('https')

    elif ProxyEngine.ProxyEngine.checkProtocolExistence(bitmap, ProxyEngine.Protocol.UNKNOWN):
        protocols.append('https')
        protocols.append('http')
        protocols.append('socks4')
        protocols.append('socks5')

    return protocols