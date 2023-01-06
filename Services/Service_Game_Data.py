from Services import servicesGlobalVariables as const
from Services import servicesmMapSpriteToFile as mapping

class Building_info:

    def __init__(self, cost, size, max_employs, sprite_name, road_dependency, water_dependency):
        self.cost = cost
        self.size = size
        self.name = sprite_name
        self.max_employs = max_employs
        if sprite_name != "":
            self.spritepath = mapping.mapping_function(const.LAYER5,sprite_name)
            if self.spritepath:
                self.size = mapping.mapping_function(const.LAYER5,sprite_name)[0][1]
        else :
            self.spritepath = mapping.mapping_function(const.LAYER5,"dwell")
            self.size = 1
        # (self.spritepath, self.cells_number) = mapping.mapping_function(const.LAYER5, sprite_type)
        self.road_dependency = road_dependency
        self.water_dependency = water_dependency


# Some data are not accurate, only copy paste name and fill some building
building_dico = {
    "academy": Building_info(100, -1, 30, "academy", False, False),
    "actor colony": Building_info(50, -1, 5, "actor_colony", False, False),
    "architects guild": Building_info(200, -1, 8, "", False, False),
    "aqueduct": Building_info(40, -1, 10, "aqueduct", True, False),
    "arena": Building_info(500, 4, 6,"arena", False, False),
    "ares temple": Building_info(50, -1, 8, "ares_temple", False, False),
    "neptune temple": Building_info(50, -1, 8, "neptune_temple", False, False),
    "mercury temple": Building_info(50, -1, 8, "mercure_temple", False, False),
    "mars temple": Building_info(50, -1, 8, "mars_temple", False, False),
    "venus temple": Building_info(50, -1, 8, "venus_temple", False, False),
    "amphitheater": Building_info(100, -1, 12, "amphitheater", False, False),
    "barber": Building_info(25, -1, 2, "barber", True, False),
    "baths": Building_info(50, -1, 10, "baths", False, True),
    "barracks": Building_info(150, -1, 10, "barracks", False, True),
    "clay pit": Building_info(40, -1, 10, "clay_pit", True, False),
    "colosseum": Building_info(500, -1, 25, "colosseum", False, False),
    "dock": Building_info(100, -1, 12, "dock", False, False),
    "doctor": Building_info(30, -1, 5, "", True, False),
    "dwell": Building_info(10, 1, 0, "dwell", False, False),
    "engineer's post": Building_info(30, 1, 6, "engineer's_post", False, False),
    "forum": Building_info(75, 4, 6, "forum", False, False),
    "fruit farm": Building_info(40, -1, 10, "fruit_farm", True, False),
    "furniture workshop": Building_info(40, -1, 10, "furniture_workshop", True, False),
    "fort": Building_info(40, -1, 10, "fort", True, False),
    "fountain": Building_info(15, -1, 10, "fountain", True, False),
    "garden": Building_info(12, -1, 0, "garden", False, False),
    "gatehouse": Building_info(40, -1, 10, "", True, False),
    "gladiator school": Building_info(75, -1, 8, "gladiator_school", False, False),
    "governor housing house": Building_info(150, -1, 0, "gov_housing_house", False, False),
    "governor housing villa": Building_info(400, -1, 0, "gov_housing_villa", False, False),
    "governor housing palace": Building_info(700, -1, 0, "gov_housing_palace", False, False),
    "granary": Building_info(40, -1, 10, "granary", True, False),
    "hospital": Building_info(300, -1, 30, "hospital", True, False),
    "iron mine": Building_info(40, -1, 10, "iron_mine", True, False),
    "library": Building_info(75, -1, 20, "library", False, False),
    "lion house": Building_info(75, -1, 8, "lion_house", False, False),
    "low bridge": Building_info(40, -1, 8, "", False, False),
    "lararium": Building_info(30, -1, 8, "", False, False),
    "lighthouse": Building_info(1250, -1, 8, "", False, False),
    "marble quarry": Building_info(40, -1, 10, "marble_quarry", True, False),
    "market": Building_info(40, -1, 10, "market", True, False),
    "oil workshop": Building_info(40, -1, 10, "oil_workshop", True, False),
    "military academi": Building_info(1000, -1, 10, "military_academy", True, False),
    "olive farm": Building_info(40, -1, 10, "olive_farm", True, False),
    "palisade": Building_info(6, -1, 0, "", False, False),
    "plaza": Building_info(15, -1, 0, "plaza", False, False),
    "pig farm": Building_info(40, -1, 10, "pig_farm", True, False),
    "prefecture": Building_info(40, -1, 10, "prefecture", True, False),
    "pottery workshop": Building_info(40, -1, 10, "pottery_workshop", True, False),
    "reservoir": Building_info(40, -1, 10, "reservoir", True, False),
    "senate": Building_info(400, 20, 30, "senate", False, False),
    "school": Building_info(50, -1, 10, "school", False, False),
    "ship bridge": Building_info(100, -1, 8, "", False, False),
    "tavern": Building_info(40, -1, 8, "", False, False),
    "theater": Building_info(50, -1, 8, "theater", False, False),
    "tower": Building_info(40, -1, 10, "tower", True, False),
    "timber yard": Building_info(40, -1, 10, "timber_yard", True, False),
    "vegetable farm": Building_info(40, -1, 10, "vegetable_farm", True, False),
    "vine farm": Building_info(40, -1, 10, "vine_farm", True, False),
    "watchtower": Building_info(100, -1, 10, "", False, True),
    "weapons workshop": Building_info(40, -1, 10, "weapons_workshop", True, False),
    "wheat farm": Building_info(40, -1, 10, "wheat_farm", True, False),
    "wine workshop": Building_info(40, -1, 10, "wine_workshop", True, False),
    "warehouse": Building_info(40, -1, 10, "warehouse", True, False),
    "work camp": Building_info(150, -1, 8, "", False, False),
    "wall": Building_info(40, -1, 10, "wall", True, False),
    "well": Building_info(40, -1, 10, "well", True, False)
}

road_dico = {'cost': 4}

text_water = ["Reservoir","Aqueduct","Fountain","Well"]
text_health = ["Barber","Baths","Doctor","Hospital"]
text_religion = ["Ares Temple","Neptune Temple","Mercury Temple","Mars Temple","Venus Temple","Lararium"]
text_roll = ["School","Academy","Librairy"]
text_entertainment = ["Theater","Tavern","Amphitheater","Arena","Colosseum","Gladiator School","Lion House","Actor Colony"]
text_education = ["Status","Trees","Parks","Paths","Governer's Mansion","Garden","Plaza","Road blocs","Forums","Senate"]
text_hammer = ["Engineer's post", "Low Bridge", "Ship Bridge", "Dock","Work camp","Architects Guild","Lighthouse"]
text_sword = ["Wall","Tower","Gatehouse","Palisade","Prefecture","Fort","Military academi","Barracks","Watchtower"]
text_carry = ["Wheat Farm","Vegetable Farm","Olive Farm","Clay Pit","Iron Mine","Weapons Workshop","Wine Workshop","Furniture Workshop","Pottery Workshop","Market","Granary","Warehouse","Caravan serai"]


removing_cost = 2
risk_random_ratio = 40