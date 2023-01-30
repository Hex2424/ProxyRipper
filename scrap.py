from ProxyEngine import *
from api.geonode_api import APIGeonode

import proxycheck
import threading
import time
import printer
import os


MAX_THREAD_POOL_SIZE = 10
PROXY_TIMEOUT = 2
PROXY_RECHECK_TIMEOUT = 3

ATTEMPTS_ON_FAILURE = 3
PROTOCOL_FILTER = [Protocol.SOCKS5]

currentThreadCount = 0
threadLock = False

proxyScrappersList = [
    APIGeonode()
]

validProxies = {}

def checkValidity(proxyList):
    global currentThreadCount

    for proxyObject in proxyList:

        while(currentThreadCount > (MAX_THREAD_POOL_SIZE - 1)):
            time.sleep(0.1)
            pass

        threading.Thread(target=proxycheck.check_proxy, args=[proxyObject, PROXY_TIMEOUT, ATTEMPTS_ON_FAILURE, proxyCheckCallback, True]).start()

        currentThreadCount += 1


def proxyCheckCallback(object):
    global currentThreadCount
    global threadLock
    # print("responded")
    if(object == None):
        currentThreadCount -= 1
        return
    # print(object.latency)
    # if not passesFilters(object):
    #     print(object.protocol)
    #     return
    # print("Sss")
    # saveProxy(object)
    while threadLock:
        pass

    validProxies[f"{object.ip}:{object.port}"] = object
    currentThreadCount -= 1

def saveProxy(object):
    with open("cache.json", 'a') as file:
        # pickle.dump(object, file)
        file.write('\n')


def passesFilters(object):
    for protocolFilter in PROTOCOL_FILTER:
        if(ProxyEngine.checkProtocolExistence(object.protocol, protocolFilter)):
            return True                                         # found atleast one matching protocol
    return False                                                # not found any matching protocols


def cleanerThread():
    global threadLock
    
    while True:
        while threadLock:
            pass

        threadLock = True
        for key, value in validProxies.items():
            if(proxycheck.check_proxy(value, PROXY_RECHECK_TIMEOUT, ATTEMPTS_ON_FAILURE, None)) == None:
                del validProxies[key]
        threadLock = False

def printingThread():
    global threadLock

    while True:
        os.system('clear')
        while threadLock:
            pass

        threadLock = True
        
        for key, value in sorted(validProxies.items(), key=lambda x: x[1].latency):
            printer.printProxyInfo(value)
        time.sleep(3)

        threadLock = False
    

def runScraping():

    threading.Thread(target=printingThread, args=[]).start()    # establishing printing threads
    threading.Thread(target=cleanerThread, args=[]).start()

    with open("cache.json", 'w') as file:
        file.write('')

    for proxyScrapper in proxyScrappersList:
        proxyScrapper.setup()

        proxy_list = proxyScrapper.scrape()

        if proxy_list == None:
            print("Error occured")
            continue

        checkValidity(proxy_list)