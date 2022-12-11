#requests library is necessary
#python -m pip install requests

import requests

class MugloarWebClient:
    def __init__(self):
        self.mugloarApiUrl = "https://dragonsofmugloar.com/api/v2"
        self.logFileName = ""
        self.logGame = False

    def startNewGame(self):
        url = self.mugloarApiUrl + "/game/start"
        response = requests.post(url)
        self.logFileName = response.json()["gameId"]
        self.logger("startNewGame", response)
        return response.json()
    
    def investigateReputation(self, gameId):
        url = self.mugloarApiUrl + "/" + gameId + "/investigate/reputation"
        response = requests.post(url)
        self.logger("investigateReputation, gameId:" + gameId, response)
        return response.json()

    def getAllMessages(self, gameId):
        url = self.mugloarApiUrl + "/" + gameId + "/messages"
        response = requests.get(url)
        self.logger("getAllMessages, gameId:" + gameId, response)
        return response.json()

    def solveMessage(self, gameId, adId):
        url = self.mugloarApiUrl + "/" + gameId + "/solve/" + adId
        response = requests.post(url)
        self.logger("solveMessage, gameId:" + gameId + " adId:" + adId, response)
        return response.json()

    def getShopItems(self, gameId):
        url = self.mugloarApiUrl + "/" + gameId + "/shop"
        response = requests.get(url)
        self.logger("getShopItems, gameId:" + gameId, response)
        return response.json()

    def purchaseShopItem(self, gameId, itemId):
        url = self.mugloarApiUrl + "/" + gameId + "/shop/buy/" + itemId
        response = requests.post(url)
        self.logger("purchaseShopItem, gameId:" + gameId + " itemId" + itemId, response)
        return response.json()

    def logger(self, request, response):
        if self.logGame:
            f = open(self.logFileName, "a")
            f.write(request + str(response.json()) + "\n")
            f.close()
