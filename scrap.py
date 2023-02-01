from ProxyEngine import *
from api.geonode_api import APIGeonode

import proxycheck
import threading
import time
import printer
import os
import signal


MAX_THREAD_POOL_SIZE = 10
PROXY_TIMEOUT = 2
PROXY_RECHECK_TIMEOUT = 3

ATTEMPTS_ON_FAILURE = 2
PROTOCOL_FILTER = [Protocol.SOCKS5]

currentThreadCount = 0
threadLock = threading.Lock()
RUN_PROGRAM = True

proxyScrappersList = [
    APIGeonode()
]

validProxies = {}



currentAPIURL = ""
currentAPICountItems = 0
currentAPIItemsChecked = 0

def checkValidity(proxyList):
    global currentThreadCount
    global currentAPIItemsChecked
    global currentAPICountItems

    currentAPIItemsChecked = 0
    currentAPICountItems = len(proxyList)

    for proxyObject in proxyList:

        while(currentThreadCount > (MAX_THREAD_POOL_SIZE - 1)):
            time.sleep(0.1)
            if not RUN_PROGRAM:
                return
            pass
        
        threading.Thread(target=proxycheck.check_proxy, args=[proxyObject, PROXY_TIMEOUT, ATTEMPTS_ON_FAILURE, proxyCheckCallback, True]).start()
        currentAPIItemsChecked += 1
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
    with threadLock:
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
    pass
    # global threadLock

    # while True:
        
    #     to_delete = []
    #     for key, value in validProxies.items():
    #         if(proxycheck.check_proxy(value, PROXY_RECHECK_TIMEOUT, ATTEMPTS_ON_FAILURE, None, False)) == None:
    #             to_delete.append(key)
        
    #     with threadLock:
    #         for key in to_delete:
    #             pass
    #             # print(key)
    #             # del validProxies[key]
    #     time.sleep(3)
    # pass

def printingThread():
    global threadLock

    while RUN_PROGRAM:
        os.system('clear')
        printer.printCurrentApi(currentAPIURL, currentAPIItemsChecked, currentAPICountItems)
        with threadLock:
            for key, value in sorted(validProxies.items(), key=lambda x: x[1].latency):
                printer.printProxyInfo(value)
        time.sleep(3)
    

def runScraping():
    global currentAPIURL

    threading.Thread(target=printingThread, args=[]).start()
    threading.Thread(target=cleanerThread, args=[]).start()


    with open("cache.json", 'w') as file:
        file.write('')

    for proxyScrapper in proxyScrappersList:
        proxyScrapper.setup()
        currentAPIURL = proxyScrapper.getCurrentApiName()
        proxy_list = proxyScrapper.scrape()

        if proxy_list == None:
            print("Error occured")
            continue

        checkValidity(proxy_list)


def handle_ctrl_c(signal, frame):
    RUN_PROGRAM = False
    # cleanup process here
    exit(0)

signal.signal(signal.SIGINT, handle_ctrl_c)