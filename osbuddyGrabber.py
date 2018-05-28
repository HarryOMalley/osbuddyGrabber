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


def processItem(id, itemName):
    url2 = "https://api.rsbuddy.com/grandExchange?a=graph&g=30&start=1424870382000&i=%s" % id

    def response(itemUrl):
        with urllib.request.urlopen(itemUrl) as response:
            return response.read()

    print('Opening URL')
    dataLength = 0
    data = 0
    retry = 0
    while dataLength < 1000:
        if retry > 0:
            print('Too little entries returned, retry %s' % retry)
            time.sleep(5)
        if retry > 50:
            print('Failed too many times, going with the data we have')
            break
        res = response(url2)
        data = json.loads(res)
        dataLength = len(data)
        retry += 1
    print('Number of entries: ' + str(dataLength))
    filename = str(id) + ' - ' + itemName + '.json'
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
        print("Error occurred")


def getData():
    getNames()
    b = 0
    print('Item list obtained, beginning to scrape data for items')
    for i in sorted(idList):
        itemName = nameList[i]
        print('Processing ' + itemName)
        try:
            processItem(i, itemName)
        except urllib.error.HTTPError:
            print('Error occurred, attempting again in 5 seconds')
            time.sleep(5)
            processItem(i, itemName)
            pass
        finally:
            print("Finished Processing " + itemName)
            b += 1
            time.sleep(5)


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
    program = input("Enter Program: ")
    if program == '1':
        print('Starting to gather data...')
        time.sleep(1)
        getData()
    elif program == '2':
        manualRun()
    else:
        print("Invalid Option")
        menu()

menu()