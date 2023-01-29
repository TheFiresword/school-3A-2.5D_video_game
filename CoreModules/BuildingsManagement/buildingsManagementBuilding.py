from Services import Service_Game_Data as gdata
from Services import servicesmMapSpriteToFile as mapping
import CoreModules.MapManagement.tileManagementElement as element
import random, math
import time

# global var
max_burning_time = 60000000000000000000000000000000
DELTA_TIME = 0.2666666
class Building(element.Element):
    def __init__(self, buildings_layer, _type, version="dwell"):

        self.risk_dico = {"fire" : 0, "collapse" : 0}
        self.risk_level_dico = {"fire": 0, "collapse" : 0}

        self.current_number_of_employees = 0
        txt= " ".join(version.split("_"))
        self.max_number_of_employees = gdata.building_dico[txt].max_employs if version != "null" else 0

        # A list of walkers id
        self.employees_id = set()

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

        # when it's constructed, a building is non functional (ex: farm, granary, prefecture, even dwell)
        self.functional = False

        # A timer to control animation of buildings
        self.previous_time = None

        super().__init__(buildings_layer, _type, version)

    def add_employee(self, id: int):
        self.employees_id.add(id)

    def flush_employee(self):
        self.employees_id = set()
        self.current_number_of_employees = 0
    def rem_employee(self, id:int):
        self.employees_id.remove(id)
        self.current_number_of_employees -= 1
    def get_all_employees(self):
        return  self.employees_id

    def is_functional(self):
        return self.functional

    def set_functional(self, value: bool):
        if value and not self.functional:
            self.update_level("stat_inc")
            self.functional = True
        elif not value and self.functional:
            self.update_level("reset")
            self.functional = False

    def update_risk_speed_with_level(self):
        if self.structure_level == 0:
            self.risk_increasing_speed = 0 if self.dic['version'] == 'dwell' else 0.8
        else:
            self.risk_increasing_speed = 1/self.structure_level if self.dic['version'] == 'dwell' else 0.8/self.structure_level



    def update_risk(self,risk):
        if risk == "fire" and self.isBurning:
            if self.BurningTime <= max_burning_time:
                self.BurningTime += 1
            else:
                self.isDestroyed = True
                self.risk_dico["fire"], self.risk_level_dico = 0, 0
                self.risk_dico["collapse"], self.risk_level_dico = 0, 0
                self.isBurning = False
        else:
            self.randombuf += random.random() * self.risk_increasing_speed
            if self.randombuf > gdata.risk_random_ratio:
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
                else:
                    self.isDestroyed = True
                    self.isBurning = False

    def updateLikeability(self):
        pass

    def update_functional_building_animation(self) ->bool:
        """
        This function will change the structure_level in a circular way so that the visual animation of the building
        can be obtained
        """
        # the animation of functional buildings
        if self.is_functional():
            if self.dic['version'] != 'dwell' and self.max_level > 1:
                if not self.previous_time:
                    self.previous_time = time.time()

                else:
                    if self.dic['version'] not in ["fruit_farm", "olive_farm", "pig_farm", "vegetable_farm",
                                                       "vine_farm",
                                                       "wheat_farm"]:
                        delta_timer = DELTA_TIME
                        init_level = 1
                    else:
                        delta_timer = 3*DELTA_TIME
                        init_level = 0

                    if time.time()- self.previous_time > delta_timer:
                        self.previous_time = time.time()
                        self.structure_level += 1
                        if self.structure_level == self.max_level:
                            self.structure_level = init_level
                        assert (self.structure_level <= self.max_level - 1)
                        return True

                    return False
        return False


    def update_level(self, update_type: "stat_inc" or 'change_content' or 'stat_dec' or 'reset'):
        if update_type == "change_content":
            self.structure_level = 0
            # self.file_path = something

        elif update_type == "stat_inc":
            if self.structure_level < self.max_level:
                self.structure_level += 1

        elif update_type == "stat_dec":
            if self.structure_level > 0:
                self.structure_level -= 1

        elif update_type == "reset":
            self.structure_level = 0

class Dwelling(Building):
    def __init__(self, buildings_layer, _type):
        super().__init__(buildings_layer, _type, "dwell")
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

        self.all_requirements_for_level = None


    def update_requirements(self):
        self.all_requirements_for_level = gdata.get_housing_requirements(self.structure_level)

    def has_access(self, supply: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                          'basic_entertainment' or 'pottery' or 'bathhouse'):
        tmp = supply + '_access'
        return getattr(self, tmp)
    def set_access(self, supply: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                          'basic_entertainment' or 'pottery' or 'bathhouse', value:bool):
        tmp = supply + '_access'
        setattr(self, tmp, value)

    def update_with_supply(self, supply: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                         'basic_entertainment' or 'pottery' or 'bathhouse', evolvable=True) ->bool:
        """
        This functions receives a supply type and check the requirements of the dwell
        When all requirements needed for its level are satisfied then the dwell is updated with stat_inc
        Its level increases by 1
        Else if he just loses a requirement needed for a previous level then the dwell is downgraded with stat_dec
        Its level decreases by 1
        return: True when the dwell level is changed
        """
        if not self.is_occupied():
            return False

        self.set_access(supply, evolvable)

        # a building is downgraded when one of its needs of previous level is satisfied no more
        # So we check if it just loose access to a supply in which case we downgrade it
        if not evolvable:
            previous_requirements = gdata.get_housing_requirements(self.structure_level-1)
            for previous_requirement in previous_requirements:
                if not self.has_access(previous_requirement):
                    self.update_level('stat_dec')
                    return True
        else:
            for requirement in self.all_requirements_for_level:
                if not self.has_access(requirement):
                    return False
            # building has access to all requirements
            self.update_level('stat_inc')
            return True
        return False


    def is_occupied(self):
        return self.structure_level > 0


class Farm(Building):
    MAX_PRODUCTION = 50
    PRODUCTION_PER_PART = 10
    def __init__(self, buildings_layer, _type, production="wheat_farm"):
        super().__init__(buildings_layer, _type, production)
        quantity = 0

    def is_haverstable(self):
        return self.quantity == MAX_PRODUCTION

class WaterStructure(Building):
    def __init__(self, buildings_layer, _type, version="well"):
        super().__init__(buildings_layer, _type, version)
        self.range = mapping.get_structures_range(_type, version)
        if version == "well":
            # a well is always functional and don't need employees
            self.functional = True

