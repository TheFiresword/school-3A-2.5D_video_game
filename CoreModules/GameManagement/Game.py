from CoreModules import *
from Services import Service_Game_Data, servicesGlobalVariables, servicesmMapSpriteToFile


class Game:
    def __init__(self, map):
        self.map = map
        self.money = 0
        self.food = 0
        self.potery = 0
        self.likeability = 0
        self.gods_favors = [0, 0, 0, 0, 0]
        self.caesar_score = 0
        self.unemployement = 0
        self.isPaused = False
        self.walkersAll = []
        self.walkersOut = []

    def startGame(self):
        # ---------------------------------#
        pass

    def foodproduction(self):
        # ---------------------------------#
        pass

    def updateReligion(self):
        pass

    def updateFire(self):
        pass

    def updateCollapsing(self):
        pass

    def updateLikeability(self):
        pass

    def updategame(self):
        # ---------------------------------#
        pass

    def walkersGetOut(self):
        pass

    def walkersOutUpdates(self):
        pass
