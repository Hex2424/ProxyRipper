from .ProxyEngine import ProxyEngine, Protocol, ProxyInfo


from .api.geonode_api import APIGeonode
from .api.cache_api import APICache
import validators

from . import proxycheck
import threading
import time
from . import printer
import os
import signal
import json


MAX_THREAD_POOL_SIZE = None
PROXY_TIMEOUT = None
ATTEMPTS_ON_FAILURE = None
DISABLE_CACHE = None
CHECK_URL = None


PROTOCOL_FILTER = [Protocol.SOCKS5]

currentThreadCount = 0

threadLock = threading.Lock()
RUN_PROGRAM = True

proxyScrappersList = [
    APICache(),
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
        # with threadLock:
        #     if f"{object.ip}:{object.port}" in validProxies:
        #         del validProxies[f"{object.ip}:{object.port}"]
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

def cacheProxies():
    dumpList = []

    with threadLock:
        for key, proxy in validProxies.items():
            # pickle.dump(object, file)
            writable = {}

            writable["ip"] = proxy.ip
            writable["port"] = proxy.port
            writable["protocol"] = proxy.protocol
            writable["country"] = proxy.country
            writable["anonymity"] = proxy.secureLevel

            dumpList.append(writable)
        
    with open("cache.json", 'w') as file:
        json.dump(dumpList, file)
        


def passesFilters(object):
    for protocolFilter in PROTOCOL_FILTER:
        if(ProxyEngine.checkProtocolExistence(object.protocol, protocolFilter)):
            return True                                         # found atleast one matching protocol
    return False                                                # not found any matching protocols


def cleanerThread():
    # global threadLock
    # global currentThreadCount

    # while True:
        
    #     for proxyObject in validProxies:
    #         while(currentThreadCount > (MAX_THREAD_POOL_SIZE - 1)):
    #             time.sleep(0.1)
    #             if not RUN_PROGRAM:
    #                 return
    #             pass
            
    #         threading.Thread(target=proxycheck.check_proxy, args=[proxyObject, PROXY_TIMEOUT, ATTEMPTS_ON_FAILURE, proxyCheckCallback, True]).start()
    #         currentThreadCount += 1
    pass

def printingThread():
    global threadLock

    while RUN_PROGRAM:
        os.system('clear')
        printer.printCurrentApi(currentAPIURL, currentAPIItemsChecked, currentAPICountItems)
        with threadLock:
            for key, value in sorted(validProxies.items(), key=lambda x: x[1].latency):
                printer.printProxyInfo(value)
        time.sleep(3)
    

def initializeArgs(args):
    global MAX_THREAD_POOL_SIZE
    global PROXY_TIMEOUT
    global ATTEMPTS_ON_FAILURE 
    global DISABLE_CACHE
    global CHECK_URL

    MAX_THREAD_POOL_SIZE = args.threads
    PROXY_TIMEOUT = args.timeout
    ATTEMPTS_ON_FAILURE = args.attempts
    DISABLE_CACHE = args.disable_cache
    CHECK_URL = args.check_url

    if not validators.url(CHECK_URL):
        print(f"URL:\"{CHECK_URL}\" is not seem like a URL")
        return False

    if MAX_THREAD_POOL_SIZE > 100:
        print("Thread count too big, your pc will crash")
        return False

    if MAX_THREAD_POOL_SIZE < 1:
        print("There must be atleast 1 thread running, threads doesn't count as negative either")
        return False

    if ATTEMPTS_ON_FAILURE > 50:
        print("I am sure you don't need such attempts count")
        return False 

    if ATTEMPTS_ON_FAILURE < 1:
        print("Need atleast have 1 attempt to validate proxy")
        return False

    return True


def runScraping(args):
    if not initializeArgs(args):
        print("Exiting app")
        exit(0)
    
    global currentAPIURL

    threading.Thread(target=printingThread, args=[]).start()
    threading.Thread(target=cleanerThread, args=[]).start()

    for proxyScrapper in proxyScrappersList:
        proxyScrapper.setup()
        currentAPIURL = proxyScrapper.getCurrentApiName()
        proxy_list = proxyScrapper.scrape()

        if proxy_list == None:
            print("Error occured")
            continue

        checkValidity(proxy_list)

    exitApp()


def handle_ctrl_c(signal, frame):
    RUN_PROGRAM = False
    # cleanup process here
    print("exiting app")
    exitApp()

def exitApp():
    global threadLock

    
    cacheProxies()

    exit(0)

signal.signal(signal.SIGINT, handle_ctrl_c)