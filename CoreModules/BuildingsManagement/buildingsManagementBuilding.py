from Services import Service_Game_Data as gdata
from Services import servicesmMapSpriteToFile as mapping
import CoreModules.TileManagement.tileManagementElement as element
import random, math


class Building(element.Element):
    def __init__(self, buildings_layer, _type, version="dwell"):
        self.risk_dico = {"fire" : 0, "collapse" : 0}
        self.risk_level_dico = {"fire": 0, "collapse" : 0} 
        self.fire_level = 0
        self.fire_risk_level = 0
        self.collapse_score = 0
        # Structure level is a number that indicates the level of the building
        # in fact some buildings like farms, dwells, grow up or grow down very often
        # we have to save these evolutions; so we use an attribute
        self.structure_level = 4 if version != "foundation_farm" else 0
        self.max_level = len(mapping.mapping_function(_type, version))

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
                else :
                    self.isDestroyed = True
                    self.isBurning = False

    def updateLikeability(self):
        pass

    def update_level(self, update_type: "stat_inc" or 'change_content'):
        if update_type == "change_content":
            self.structure_level = 0
            # self.file_path = something
        elif update_type == "stat_inc":
            self.structure_level += 1
            self.structure_level %= self.max_level

class Dwelling(Building):
    def __init__(self, buildings_layer, _type):
        super().__init__(buildings_layer, _type, "dwell")
        self.current_population = None
        self.max_population = None
        """
        Desirability can prevent a house from evolving. In order to evolve, a house also must have a certain 
        desirability in addition to more services. Desirability is calculated from the nearby buildings. 
        For example, a reservoir is an undesirable neighbour while a temple is rather desirable. A house requires more 
        desirability as it evolves.
        """
        self.desirability = 0

        # Requirements of housing to evolve
        """
        The general progression of housing is as follows:

        Tents: Basic housing, very prone to fires. Large tents need a water supply.
        
        Shacks: Shacks require food provided from a market.
        
        Hovels: Hovels require basic temple access.
        """
        # attributes will be added following our progression in the code
        self.water_supply = 0

    def update_with_supply(self):
        self.water_supply = 1
        self.update_level('stat_inc')

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

class WaterStructure(Building):
    def __init__(self, buildings_layer, _type, version="well"):
        super().__init__(buildings_layer, _type, version)
        self.range = mapping.get_structures_range(_type, version)
        self.functional = False