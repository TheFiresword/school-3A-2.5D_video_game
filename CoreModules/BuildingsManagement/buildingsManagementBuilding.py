from Services import Service_Game_Data as gdata

import CoreModules.TileManagement.tileManagementElement as element
import random, math


class Building(element.Element):
    def __init__(self, buildings_layer, _type, version="dwell"):
        self.risk_dico = {"fire" : 0, "collapse" : 0}
        self.risk_level_dico = {"fire": 0, "collapse" : 0} 
        self.fire_level = 0
        self.fire_risk_level = 0
        self.collapse_score = 0
        self.structure_level = 1
        self.isBurning = False
        self.BurningTime = 0
        self.isDestroyed = False
        self.randombuf = 0

        super().__init__(buildings_layer, _type, version)
       
    def update_risk(self,risk):
        if risk == "fire" and self.isBurning:
            if self.BurningTime <= 60000000000000000000000000000000:
                self.BurningTime += 1
            else:
                self.isDestroyed = True
                self.isBurning = False
        else:
            self.randombuf += random.random()
            if  self.randombuf> gdata.risk_random_ratio:
                self.randombuf = 0
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
                    self.isBurning = False
                    print("Destroyed")

    def updateLikeability(self):
        pass




class Dwelling(Building):
    def __init__(self, buildings_layer, _type):
        super().__init__(buildings_layer, _type, "dwell")
        self.current_population = None
        self.max_population = None

class Farm(Building):
    def __init__(self, buildings_layer, _type, production="wheat_farm"):
        # opt: empecher l'attribut d'id a l'init
        super().__init__(buildings_layer, _type, production)
        self.foundation = Building(buildings_layer, _type, "foundation_farm")
        self.farm_at_00 = Building(buildings_layer, _type, production)
        self.farm_at_01 = Building(buildings_layer, _type, production)
        self.farm_at_02 = Building(buildings_layer, _type, production)
        self.farm_at_12 = Building(buildings_layer, _type, production)
        self.farm_at_22 = Building(buildings_layer, _type, production)

        self.total_cells = self.foundation.dic['cells_number'] ** 2 + self.farm_at_22.dic['cells_number'] ** 2 + \
                           self.farm_at_12.dic['cells_number'] ** 2 +self.farm_at_00.dic['cells_number'] ** 2 + \
                           self.farm_at_01.dic['cells_number'] ** 2 + self.farm_at_02.dic['cells_number'] ** 2

        self.total_cells = int(math.sqrt(self.total_cells))
        # we change the cells_number attribute so that to have the exact cells number
        self.dic['cells_number'] = self.total_cells