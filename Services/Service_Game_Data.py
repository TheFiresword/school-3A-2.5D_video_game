from Services import servicesGlobalVariables as const
from Services import servicesmMapSpriteToFile as mapping


class Building_info:

    def __init__(self, cost, size, max_employs, sprite_name, road_dependency, water_dependency):
        self.cost = cost
        self.size = size
        self.name = sprite_name
        self.max_employs = max_employs

        if sprite_name != "":
            self.spritepath = mapping.mapping_function(const.LAYER5, sprite_name)[0][0]
            if self.spritepath:
                self.size = mapping.mapping_function(const.LAYER5, sprite_name)[0][1]
        else:
            self.spritepath = mapping.mapping_function(const.LAYER5, "dwell")[0][0]
            self.size = 1
        # (self.spritepath, self.cells_number) = mapping.mapping_function(const.LAYER5, sprite_type)

        self.road_dependency = road_dependency
        self.water_dependency = water_dependency


# Some data are not accurate, only copy paste name and fill some building
building_dico = {
    "academy": Building_info(100, -1, 6 * const.WALKER_UNIT, "academy", False, False),
    "actor colony": Building_info(50, -1, 1 * const.WALKER_UNIT, "actor_colony", False, False),
    "architects guild": Building_info(200, -1, 2 * const.WALKER_UNIT, "", False, False),
    "aqueduct": Building_info(40, -1, 2 * const.WALKER_UNIT, "aqueduct", True, False),
    # "arena": Building_info(500, 4, 6,"arena", False, False),
    "ares temple": Building_info(50, -1, 1 * const.WALKER_UNIT, "ares_temple", False, False),
    "neptune temple": Building_info(50, -1, 1 * const.WALKER_UNIT, "neptune_temple", False, False),
    "mercury temple": Building_info(50, -1, 1 * const.WALKER_UNIT, "mercury_temple", False, False),
    "mars temple": Building_info(50, -1, 1 * const.WALKER_UNIT, "mars_temple", False, False),
    "venus temple": Building_info(50, -1, 1 * const.WALKER_UNIT, "venus_temple", False, False),
    "amphitheater": Building_info(100, -1, 2 * const.WALKER_UNIT, "amphitheater", False, False),
    "barber": Building_info(25, -1, 1 * const.WALKER_UNIT, "barber", True, False),
    "normal bath": Building_info(50, -1, 0 * const.WALKER_UNIT, "normal_bath", False, True),

    "barracks": Building_info(150, -1, 2 * const.WALKER_UNIT, "barracks", False, True),
    "clay pit": Building_info(40, -1, 2 * const.WALKER_UNIT, "clay_pit", True, False),
    "colosseum": Building_info(500, -1, 5 * const.WALKER_UNIT, "colosseum", False, False),
    "dock": Building_info(100, -1, 2 * const.WALKER_UNIT, "dock", False, False),
    "doctor": Building_info(30, -1, 1 * const.WALKER_UNIT, "", True, False),
    "dwell": Building_info(10, 1, 1 * const.WALKER_UNIT, "dwell", False, False),
    "engineer's post": Building_info(30, 1, 1 * const.WALKER_UNIT, "engineer's_post", False, False),
    "forum": Building_info(75, 4, 1 * const.WALKER_UNIT, "forum", False, False),
    "fruit farm": Building_info(40, -1, 1 * const.WALKER_UNIT, "fruit_farm", True, False),
    "furniture workshop": Building_info(40, -1, 2 * const.WALKER_UNIT, "furniture_workshop", True, False),
    "fort": Building_info(40, -1, 2 * const.WALKER_UNIT, "fort", True, False),
    "fountain": Building_info(15, -1, 0 * const.WALKER_UNIT, "fountain", True, False),
    "garden": Building_info(12, -1, 0 * const.WALKER_UNIT, "garden", False, False),
    "gatehouse": Building_info(40, -1, 2 * const.WALKER_UNIT, "", True, False),
    "gladiator school": Building_info(75, -1, 2 * const.WALKER_UNIT, "gladiator_school", False, False),
    "governor housing house": Building_info(150, -1, 0 * const.WALKER_UNIT, "gov_housing_house", False, False),
    "governor housing villa": Building_info(400, -1, 0 * const.WALKER_UNIT, "gov_housing_villa", False, False),
    "governor housing palace": Building_info(700, -1, 0 * const.WALKER_UNIT, "gov_housing_palace", False, False),
    "granary": Building_info(40, -1, 1 * const.WALKER_UNIT, "granary", True, False),
    "hospital": Building_info(300, -1, 6 * const.WALKER_UNIT, "hospital", True, False),
    "iron mine": Building_info(40, -1, 2 * const.WALKER_UNIT, "iron_mine", True, False),
    "library": Building_info(75, -1, 4 * const.WALKER_UNIT, "library", False, False),
    "lion house": Building_info(75, -1, 2 * const.WALKER_UNIT, "lion_house", False, False),
    "low bridge": Building_info(40, -1, 2 * const.WALKER_UNIT, "", False, False),
    "lararium": Building_info(30, -1, 2 * const.WALKER_UNIT, "", False, False),
    "lighthouse": Building_info(1250, -1, 2 * const.WALKER_UNIT, "", False, False),
    "luxurious bath": Building_info(50, -1, 0 * const.WALKER_UNIT, "luxurious_bath", False, True),
    "marble quarry": Building_info(40, -1, 2 * const.WALKER_UNIT, "marble_quarry", True, False),
    "market": Building_info(40, -1, 2 * const.WALKER_UNIT, "market", True, False),
    "oil workshop": Building_info(40, -1, 2 * const.WALKER_UNIT, "oil_workshop", True, False),
    "military academy": Building_info(1000, -1, 1 * const.WALKER_UNIT, "military_academy", True, False),
    "olive farm": Building_info(40, -1, 1 * const.WALKER_UNIT, "olive_farm", True, False),
    "palisade": Building_info(6, -1, 0 * const.WALKER_UNIT, "", False, False),
    "plaza": Building_info(15, -1, 0 * const.WALKER_UNIT, "plaza", False, False),
    "pig farm": Building_info(40, -1, 1 * const.WALKER_UNIT, "pig_farm", True, False),
    "prefecture": Building_info(40, -1, 1 * const.WALKER_UNIT, "prefecture", True, False),
    "pottery workshop": Building_info(40, -1, 2 * const.WALKER_UNIT, "pottery_workshop", True, False),
    "reservoir": Building_info(40, -1, 0 * const.WALKER_UNIT, "reservoir", True, False),
    "senate": Building_info(400, 20, 6 * const.WALKER_UNIT, "senate", False, False),
    "school": Building_info(50, -1, 2 * const.WALKER_UNIT, "school", False, False),
    "ship bridge": Building_info(100, -1, 2 * const.WALKER_UNIT, "", False, False),
    "tavern": Building_info(40, -1, 2 * const.WALKER_UNIT, "", False, False),
    "theater": Building_info(50, -1, 2 * const.WALKER_UNIT, "theater", False, False),
    "tower": Building_info(40, -1, 2 * const.WALKER_UNIT, "tower", True, False),
    "timber yard": Building_info(40, -1, 2 * const.WALKER_UNIT, "timber_yard", True, False),
    "vegetable farm": Building_info(40, -1, 1 * const.WALKER_UNIT, "vegetable_farm", True, False),
    "vine farm": Building_info(40, -1, 1 * const.WALKER_UNIT, "vine_farm", True, False),
    "watchtower": Building_info(100, -1, 2 * const.WALKER_UNIT, "", False, True),
    "weapons workshop": Building_info(40, -1, 2 * const.WALKER_UNIT, "weapons_workshop", True, False),
    "wheat farm": Building_info(40, -1, 1 * const.WALKER_UNIT, "wheat_farm", True, False),
    "wine workshop": Building_info(40, -1, 2 * const.WALKER_UNIT, "wine_workshop", True, False),
    "warehouse": Building_info(40, -1, 2 * const.WALKER_UNIT, "warehouse", True, False),
    "work camp": Building_info(150, -1, 2 * const.WALKER_UNIT, "", False, False),
    "wall": Building_info(40, 1, 0 * const.WALKER_UNIT, "wall", True, False),
    "well": Building_info(40, 1, 0 * const.WALKER_UNIT, "well", True, False)
}

road_dico = {'cost': 4}

text_water = ["Reservoir", "Fountain", "Well"]
text_health = ["Barber", "Normal Bath", "Luxurious Bath", "Hospital"]
text_religion = ["Ares Temple", "Neptune Temple", "Mercury Temple", "Mars Temple", "Venus Temple"]
text_roll = ["School"]
text_entertainment = ["Theater", "Amphitheater", "Colosseum", "Gladiator School", "Lion House", "Actor Colony"]
text_education = ["Senate"]
text_hammer = ["Engineer's post"]
text_sword = ["Prefecture", "military academy"]
text_carry = ["Wheat Farm", "Vegetable Farm", "Olive Farm", "Vine Farm", "Pig Farm", "Fruit Farm", "Clay Pit",
              "Furniture Workshop", "Market", "Granary"]

removing_cost = 2
risk_random_ratio = 40

MAX_PRODUCTION = 200
PRODUCTION_PER_PART = 10


def get_housing_requirements(level):
    level_requirements = []
    match level:
        case 1:
            level_requirements = ['water']
        case 2:
            level_requirements = ['water', 'food']
        case 3:
            level_requirements = ['water', 'food', 'temple']
        case 4:
            level_requirements = ['water', 'food', 'temple', 'education', 'fountain', 'basic_entertainment']
        case 5:
            level_requirements = ['water', 'food', 'temple', 'education', 'fountain', 'basic_entertainment', 'pottery',
                                  'bathhouse']
    return level_requirements