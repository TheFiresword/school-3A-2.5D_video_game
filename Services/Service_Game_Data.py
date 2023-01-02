from Services import servicesGlobalVariables as const
from Services import servicesmMapSpriteToFile as mapping

class Building_info:

    def __init__(self, cost, size, max_employs, sprite, road_dependency, water_dependency):
        self.cost = cost
        self.size = size
        self.max_employs = max_employs
        self.spritepath = sprite
        # (self.spritepath, self.cells_number) = mapping.mapping_function(const.LAYER5, sprite_type)
        self.road_dependency = road_dependency
        self.water_dependency = water_dependency


# Some data are not accurate, only copy paste name and fill some building
building_dico = {
    "forum": Building_info(75, 4, 6, "forum", False, False),
    "senate": Building_info(400, 20, 30, "", False, False),
    "gov_housing_house": Building_info(150, -1, 0, "", False, False),
    "gov_housing_villa": Building_info(400, -1, 0, "", False, False),
    "gov_housing_palace": Building_info(700, -1, 0, "", False, False),
    "academy": Building_info(100, -1, 30, "", False, False),
    "library": Building_info(75, -1, 20, "", False, False),
    "school": Building_info(50, -1, 10, "", False, False),
    "garden": Building_info(12, -1, 0, "", False, False),
    "plaza": Building_info(15, -1, 0, "", False, False),
    "engineer's post": Building_info(30, 1, 6, "", False, False),
    "dock": Building_info(100, -1, 12, "", False, False),
    "theater": Building_info(50, -1, 8, "", False, False),
    "amphitheater": Building_info(100, -1, 12, "", False, False),
    "colosseum": Building_info(500, -1, 25, "", False, False),
    "actor_colony": Building_info(50, -1, 5, "", False, False),
    "gladiator_school": Building_info(75, -1, 8, "", False, False),
    "lion_house": Building_info(75, -1, 8, "", False, False),
    "barber": Building_info(25, -1, 2, "", True, False),
    "baths": Building_info(50, -1, 10, "", False, True),
    "doctor": Building_info(30, -1, 5, "", True, False),
    "hospital": Building_info(300, -1, 30, "", True, False),
    "fruit_farm": Building_info(40, -1, 10, "", True, False),
    "olive_farm": Building_info(40, -1, 10, "", True, False),
    "pig_farm": Building_info(40, -1, 10, "", True, False),
    "vegetable_farm": Building_info(40, -1, 10, "", True, False),
    "vine_farm": Building_info(40, -1, 10, "", True, False),
    "wheat_farm": Building_info(40, -1, 10, "wheat_farm", True, False),
    "iron_mine": Building_info(40, -1, 10, "", True, False),
    "timber_yard": Building_info(40, -1, 10, "", True, False),
    "marble_quarry": Building_info(40, -1, 10, "", True, False),
    "clay_pit": Building_info(40, -1, 10, "", True, False),
    "furniture_workshop": Building_info(40, -1, 10, "", True, False),
    "oil_workshop": Building_info(40, -1, 10, "", True, False),
    "pottery_workshop": Building_info(40, -1, 10, "", True, False),
    "weapons_workshop": Building_info(40, -1, 10, "", True, False),
    "wine_workshop": Building_info(40, -1, 10, "", True, False),
    "market": Building_info(40, -1, 10, "", True, False),
    "granary": Building_info(40, -1, 10, "", True, False),
    "warehouse": Building_info(40, -1, 10, "", True, False),
    "wall": Building_info(40, -1, 10, "", True, False),
    "tower": Building_info(40, -1, 10, "", True, False),
    "gatehouse": Building_info(40, -1, 10, "", True, False),
    "prefecture": Building_info(40, -1, 10, "", True, False),
    "fort": Building_info(40, -1, 10, "", True, False),
    "military_academy": Building_info(40, -1, 10, "", True, False),
    "reservoir": Building_info(40, -1, 10, "", True, False),
    "aqueduct": Building_info(40, -1, 10, "aqueduct", True, False),
    "well": Building_info(40, -1, 10, "well", True, False),
    "dwell": Building_info(10, 1, 0, const.SPRITE_PATH + "Land/housng/Housng1a_00000.png", False, False)
}

road_dico = {'cost': 4}

text_water = ["Reservoir","Aqueduct","Fountain","Well"]
text_health = ["Barber","Baths","Doctor","Hospital"]
text_religion = ["Small temple"]
text_roll = ["test"]
text_entertainment = ["Theater","Amphitheater","Arena","Colosseum","Gladiator School","Lion House","Actor Colony"]
text_education = ["Status","Trees","Parks","Paths","Governer's Mansion","Garden","Plaza","Road blocs","Forums","Senate"]
text_hammer = ["Engineer's post", "Low Bridge", "Ship Bridge", "Dock","Work camps","Architect's Guild","Light house"]
text_sword = ["Wall","Tower","Gate House","Palissade","Prefecture","Fort","Military academi","Barracks","Watchtowers"]
text_carry = ["Farms","Raw Materials","Workshops","Market","Granary","Warehouse","Caravan serai"]


removing_cost = 2
risk_random_ratio = 40