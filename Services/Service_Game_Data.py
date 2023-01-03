from Services import servicesGlobalVariables as const
from Services import servicesmMapSpriteToFile as mapping

class Building_info:

    def __init__(self, cost, size, max_employs, sprite_name, road_dependency, water_dependency):
        self.cost = cost
        self.size = size
        self.max_employs = max_employs
        if sprite_name != "":
            self.spritepath = mapping.mapping_function(const.LAYER5,sprite_name)
        else :
            self.spritepath = mapping.mapping_function(const.LAYER5,"dwell")
        # (self.spritepath, self.cells_number) = mapping.mapping_function(const.LAYER5, sprite_type)
        self.road_dependency = road_dependency
        self.water_dependency = water_dependency


# Some data are not accurate, only copy paste name and fill some building
building_dico = {
    "academy": Building_info(100, -1, 30, "", False, False),
    "actor_colony": Building_info(50, -1, 5, "", False, False),
    "architect_guild": Building_info(200, -1, 8, "", False, False),
    "aqueduct": Building_info(40, -1, 10, "aqueduct", True, False),
    "arena": Building_info(500, 4, 6,"arena", False, False),
    "ares temple": Building_info(50, -1, 8, "", False, False),
    "neptune temple": Building_info(50, -1, 8, "", False, False),
    "mercury temple": Building_info(50, -1, 8, "", False, False),
    "mars temple": Building_info(50, -1, 8, "", False, False),
    "venus temple": Building_info(50, -1, 8, "", False, False),
    "amphitheater": Building_info(100, -1, 12, "", False, False),
    "barber": Building_info(25, -1, 2, "", True, False),
    "baths": Building_info(50, -1, 10, "", False, True),
    "clay pit": Building_info(40, -1, 10, "", True, False),
    "colosseum": Building_info(500, -1, 25, "", False, False),
    "dock": Building_info(100, -1, 12, "", False, False),
    "doctor": Building_info(30, -1, 5, "", True, False),
    "dwell": Building_info(10, 1, 0, "dwell", False, False),
    "engineer's post": Building_info(30, 1, 6, "", False, False),
    "forum": Building_info(75, 4, 6, "forum", False, False),
    "fruit farm": Building_info(40, -1, 10, "", True, False),
    "furniture workshop": Building_info(40, -1, 10, "", True, False),
    "fort": Building_info(40, -1, 10, "", True, False),
    "fountain": Building_info(15, -1, 10, "foutain", True, False),
    "garden": Building_info(12, -1, 0, "", False, False),
    "gatehouse": Building_info(40, -1, 10, "", True, False),
    "gladiator school": Building_info(75, -1, 8, "", False, False),
    "governor housing house": Building_info(150, -1, 0, "", False, False),
    "governor housing villa": Building_info(400, -1, 0, "", False, False),
    "governor housing palace": Building_info(700, -1, 0, "", False, False),
    "granary": Building_info(40, -1, 10, "", True, False),
    "hospital": Building_info(300, -1, 30, "", True, False),
    "iron mine": Building_info(40, -1, 10, "", True, False),
    "library": Building_info(75, -1, 20, "", False, False),
    "lion house": Building_info(75, -1, 8, "", False, False),
    "low bridge": Building_info(40, -1, 8, "", False, False),
    "lararium": Building_info(30, -1, 8, "", False, False),
    "lighthouse": Building_info(1250, -1, 8, "", False, False),
    "marble quarry": Building_info(40, -1, 10, "", True, False),
    "market": Building_info(40, -1, 10, "", True, False),
    "oil workshop": Building_info(40, -1, 10, "", True, False),
    "olive farm": Building_info(40, -1, 10, "", True, False),
    "plaza": Building_info(15, -1, 0, "", False, False),
    "pig farm": Building_info(40, -1, 10, "", True, False),
    "prefecture": Building_info(40, -1, 10, "", True, False),
    "pottery workshop": Building_info(40, -1, 10, "", True, False),
    "reservoir": Building_info(40, -1, 10, "", True, False),
    "senate": Building_info(400, 20, 30, "", False, False),
    "school": Building_info(50, -1, 10, "", False, False),
    "ship bridge": Building_info(100, -1, 8, "", False, False),
    "theater": Building_info(50, -1, 8, "", False, False),
    "tower": Building_info(40, -1, 10, "", True, False),
    "timber yard": Building_info(40, -1, 10, "", True, False),
    "vegetable farm": Building_info(40, -1, 10, "", True, False),
    "vine farm": Building_info(40, -1, 10, "", True, False),
    "weapons workshop": Building_info(40, -1, 10, "", True, False),
    "wheat farm": Building_info(40, -1, 10, "wheat_farm", True, False),
    "wine workshop": Building_info(40, -1, 10, "", True, False),
    "warehouse": Building_info(40, -1, 10, "", True, False),
    "work camp": Building_info(150, -1, 8, "", False, False),
    "wall": Building_info(40, -1, 10, "", True, False),
    "well": Building_info(40, -1, 10, "well", True, False)
}

road_dico = {'cost': 4}

text_water = ["Reservoir","Aqueduct","Fountain","Well"]
text_health = ["Barber","Baths","Doctor","Hospital"]
text_religion = ["Ares Temple","Neptune Temple","Mercury Temple","Mars Temple","Venus Temple","Lararium"]
text_roll = ["School","Academy","Librairy"]
text_entertainment = ["Theater","Tower","Amphitheater","Arena","Colosseum","Gladiator School","Lion House","Actor Colony"]
text_education = ["Status","Trees","Parks","Paths","Governer's Mansion","Garden","Plaza","Road blocs","Forums","Senate"]
text_hammer = ["Engineer's post", "Low Bridge", "Ship Bridge", "Dock","Work camps","Architect's Guild","Light house"]
text_sword = ["Wall","Tower","Gate House","Palissade","Prefecture","Fort","Military academi","Barracks","Watchtowers"]
text_carry = ["Farms","Raw Materials","Workshops","Market","Granary","Warehouse","Caravan serai"]


removing_cost = 2
risk_random_ratio = 40