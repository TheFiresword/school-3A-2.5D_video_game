from Services import Service_Game_Data as gdata
from Services import servicesmMapSpriteToFile as mapping
import CoreModules.TileManagement.tileManagementElement as element
import random, math

# global var
max_burning_time = 60000000000000000000000000000000

class Building(element.Element):
    def __init__(self, buildings_layer, _type, version="dwell"):
        self.risk_dico = {"fire" : 0, "collapse" : 0}
        self.risk_level_dico = {"fire": 0, "collapse" : 0} 

        # A factor that will be used to control risk increasing speed -- It must takes account the structure level
        # ie a building at level 4 will have a risk speed lower than a another at level 1
        self.risk_increasing_speed = 0

        # Structure level is a number that indicates the level of the building
        # in fact some buildings like farms, dwells, grow up or grow down very often
        # we have to save these evolutions; so we use an attribute
        self.structure_level = 0
        self.max_level = len(mapping.mapping_function(_type, version))

        self.isBurning = False
        self.BurningTime = 0
        self.isDestroyed = False
        self.randombuf = 0
        self.update_risk_speed_with_level()

        super().__init__(buildings_layer, _type, version)


    def update_risk_speed_with_level(self):
        if self.structure_level == 0:
            self.risk_increasing_speed = 0 if self.dic['version'] == 'dwell' else 0.8
        else:
            self.risk_increasing_speed = 1/self.structure_level if self.dic['version'] == 'dwell' else 0.8/self.structure_level
    def update_risk(self,risk):
        # As update_risk function is called very often we use this to update risk_speed simultaneously
        self.update_risk_speed_with_level()

        if risk == "fire" and self.isBurning:
            if self.BurningTime <= max_burning_time:
                self.BurningTime += 1
            else:
                self.isDestroyed = True
                self.isBurning = False
        else:
            self.randombuf += random.random()*self.risk_increasing_speed
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

    def update_level(self, update_type: "stat_inc" or 'change_content' or 'stat_dec' or 'reset'):
        if update_type == "change_content":
            self.structure_level = 0
            # self.file_path = something

        elif update_type == "stat_inc":
            self.structure_level += 1
            self.structure_level %= self.max_level

        elif update_type == "stat_dec":
            if self.structure_level > 0:
                self.structure_level -= 1

        elif update_type == "reset":
            self.structure_level = 0

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

        * Tents: Basic housing, very prone to fires. Large tents need a water supply.
        
        * Shacks: Shacks require food provided from a market.
        
        * Hovels: Hovels require basic temple access.
        
        * Casas: Small casas are 'bread and butter' housing, requiring only food, basic education, fountain access 
        and basic entertainment. Large casas require pottery and bathhouse access.

        * Insulae: Medium insulae require furniture, and Large insulae, oil. Large insulae require at least a 2x2 plot of 
        land, and will expand if necessary to do so. Grand Insulae will require access to a library, school, barber, 
        doctor, two food types and 'some access' to entertainment venues (e.g. theatre + amphitheatre + 2 shows + 
        average overall city entertainment coverage.) Grand insulae are the most developed form of plebian housing.

        * Villas and Palaces: Small villas require wine and access to temples to 2 different Gods. Large villas will 
        expand to 3x3 plots. Grand Villas will require access to a hospital, academy, and temples to 3 different Gods. 
        Small palaces will require a second source of wine (imported if the city's primary source of wine is local, 
        or vice-versa.) Large palaces will expand to 4x4 plots. Steadily increasing entertainment values are the main 
        requirement for patrician housing to develop, and those for a Luxury Palace are near-perfect.
        
        """
        # attributes will be added following our progression in the code
        self.water_access = False
        self.food_access = False
        self.temple_access = False
        self.education_access = False
        self.fountain_access = False
        self.basic_entertainment_access = False
        self.pottery_access = False
        self.bathhouse_access = False

        self.possible_requirements = {'water','food','temple', 'education', 'fountain', 'basic_entertainment', 'pottery',
                             'bathhouse'}
        self.current_requirements = {}

    def update_requirements(self):
        for i in range(self.structure_level):
            self.current_requirements.add(list(self.possible_requirements)[i])

    def is_required(self, what: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                          'basic_entertainment' or 'pottery' or 'bathhouse'):
        return what in self.current_requirements
    def has_access(self, supply: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                          'basic_entertainment' or 'pottery' or 'bathhouse'):
        tmp = supply + '_access'
        return getattr(self, tmp)
    def set_access(self, supply: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                          'basic_entertainment' or 'pottery' or 'bathhouse', value:bool):
        tmp = supply + '_access'
        setattr(self, tmp, value)
        if value:
            self.current_requirements.remove(supply)
        else:
            self.current_requirements.add(supply)

    def update_with_supply(self, supply: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                         'basic_entertainment' or 'pottery' or 'bathhouse', evolve=True):
        self.set_access(supply, evolve)
        if evolve:
            self.update_level('stat_inc')
        else:
            self.update_level('stat_dec')

    def is_occupied(self):
        return self.structure_level > 0

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

    def reset_farm(self):
        self.farm_at_00.update_level('reset')
        self.farm_at_01.update_level('reset')
        self.farm_at_02.update_level('reset')
        self.farm_at_12.update_level('reset')
        self.farm_at_22.update_level('reset')

class WaterStructure(Building):
    def __init__(self, buildings_layer, _type, version="well"):
        super().__init__(buildings_layer, _type, version)
        self.range = mapping.get_structures_range(_type, version)
        if version == "well":
            self.functional = True
        else:
            self.functional = False

    def is_functional(self):
        return self.functional
    def set_functional(self, value: bool):
        self.functional = value
