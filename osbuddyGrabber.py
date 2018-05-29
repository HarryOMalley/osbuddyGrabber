import json
import urllib.request
import urllib
import time

buyList = {}
sellList = {}
averageList = {}
nameList = {}
idList = {}
storeList = {}


def openURL(url):
    def response(itemURL):
        with urllib.request.urlopen(itemURL) as response:
            return response.read()
    return response(url)


def processItem(id, itemName):
    url = "https://api.rsbuddy.com/grandExchange?a=graph&g=30&start=1424870382000&i=%s" % id
    print("Attempting to open URL")
    dataLength = 0
    data = 0
    retry = 0
    res = 0
    while dataLength < 100:
        if retry > 0:
            print(' - Too little entries returned, retry %s' % retry)
            time.sleep(1)
        if retry > 20:
            print(' - Failed too many times, going with the data we have')
            break
        try:
            res = openURL(url)
        except:
            res = openURL(url)
        print("Opened URL", end='', flush=True)
        data = json.loads(res)
        print(", Loaded data", end='', flush=True)
        dataLength = len(data)
        retry += 1
    print(', Number of entries: ' + str(dataLength))
    filename = 'data/' + str(id) + ' - ' + itemName + '.json'
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def getNames():
    print('Getting item list')
    try:
        url = "https://rsbuddy.com/exchange/summary.json"

        def response(url):
            with urllib.request.urlopen(url) as response:
                return response.read()

        res = response(url)
        a = 0
        data = json.loads(res)
        n = len(data)
        for p in data:
            buyList[int(p)] = data[p]["buy_average"]
            sellList[int(p)] = data[p]["sell_average"]
            averageList[int(p)] = data[p]["overall_average"]
            nameList[int(p)] = data[p]["name"]
            idList[int(p)] = data[p]["id"]
            storeList[int(p)] = data[p]["sp"]
            a += 1
    except:
        print("Error occurred when getting item list, trying again in 5 seconds")
        time.sleep(5)
        getNames()


def getData():
    getNames()
    b = 0
    print('Item list obtained, beginning to scrape data for items')
    for i in sorted(idList):
        itemName = nameList[i]
        print('Processing ' + itemName)
        processItem(i, itemName)
        print("Finished Processing " + itemName)
        b += 1


def getData2():
    getNames()
    b = 0
    startPoint = input("Enter the Item ID you would like to start from: ")
    print('Item list obtained, beginning to scrape data for items')
    for i in sorted(idList):
        if i < int(startPoint):
            continue
        itemName = nameList[i]
        print('Processing ' + itemName)
        try:
            processItem(i, itemName)
        except:
            print('Error occurred processing, attempting again in 5 seconds')
            time.sleep(5)
            processItem(i, itemName)
            pass
        finally:
            print("Finished Processing " + itemName)
            b += 1
            #time.sleep(5)

def manualRun():
    getNames()
    itemName = ''
    try:
        id = int(input("Enter Item ID: "))
        itemName = nameList[id]
    except:
        print("Invalid Item ID")
        manualRun()
    print('Processing ' + itemName)
    try:
        processItem(id, itemName)
    except:
        print("Error occurred, trying again in 5 seconds")
        time.sleep(5)
        processItem(id, itemName)
    finally:
        print("Finished processing " + itemName)
        return 1

def menu():
    print("1. Automatic Gather")
    print("2. Manual")
    print("3. Automatic from start point")
    program = input("Enter Program: ")
    if program == '1':
        print('Starting to gather data...')
        #time.sleep(1)
        getData()
    elif program == '2':
        manualRun()
    elif program == '3':
        getData2()
    else:
        print("Invalid Option")
        menu()

menu()