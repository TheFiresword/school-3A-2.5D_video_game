from Services import Service_Game_Data as gdata

import CoreModules.TileManagement.tileManagementElement as element
import random


class Building(element.Element):
    def __init__(self, buildings_layer, _type, version="normal"):
        super().__init__(buildings_layer, _type, version)
        self.risk_dico = {"fire" : 0, "collapse" : 0}
        self.risk_level_dico = {"fire": 0, "collapse" : 0} 
        self.fire_level = 0
        self.fire_risk_level = 0
        self.collapse_score = 0
        self.structure_level = 0
        self.isBurning = False
        self.BurningTime = 0
        self.isDestroyed = False
       
    def update_risk(self,risk):
        if risk == "fire" and self.isBurning:
            if self.BurningTime <= 600:
                self.BurningTime += 1
            else:
                self.isDestroyed = True
                self.isBurning = False
        else:
            if random.random() > gdata.risk_random_ratio:
                self.risk_dico[risk] += 5
            if self.risk_dico[risk] == 0:
                self.risk_level_dico[risk] = 0
            elif self.risk_dico[risk] < 20:
                self.risk_level_dico[risk] = 1
            elif self.risk_dico[risk] < 50:
                self.risk_level_dico[risk] = 2
            elif self.risk_dico[risk] < 80:
                self.risk_level_dico[risk] = 3
            elif self.risk_dico[risk] < 100:
                self.risk_level_dico[risk] = 4
            else:
                if risk == "fire":
                    self.isBurning = True
                    self.BurningTime = 0
                    print("j ai pris feu",self.position)
                else :
                    self.isDestroyed = True

    def updateLikeability(self):
        pass




class Dwelling(Building):
    def __init__(self, buildings_layer, _type, version="dwell"):
        super().__init__(buildings_layer, _type, version)
        self.current_population = None
        self.max_population = None




