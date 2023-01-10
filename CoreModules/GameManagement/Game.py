from Services import servicesGlobalVariables as globalVar
from Services.Service_Game_Data import building_dico, road_dico, removing_cost
from CoreModules.GameManagement import Update as updates
from CoreModules.BuildingsManagement import buildingsManagementBuilding as buildings
from CoreModules.WalkersManagement import walkersManagementWalker as walkers

INIT_MONEY = 1000000000

import time

class Game:
    def __init__(self, _map, name="save"):
        self.name = name
        self.map = _map
        self.money = INIT_MONEY
        self.food = 0
        self.potery = 0
        self.likeability = 0
        self.gods_favors = [0, 0, 0, 0, 0]
        self.caesar_score = 0
        self.unemployement = 0
        self.isPaused = False
        self.buildinglist = []
        self.walkersAll = []
        self.walkersOut = []
        self.framerate = globalVar.DEFAULT_FPS
        self.updated = []

        # some lists of specific buildings
        self.water_structures_list = []
        self.food_structures_list = []
        self.temple_structures_list = []
        self.education_structures_list = []
        self.fountain_structures_list = []
        self.basic_entertainment_structures_list = []
        self.pottery_structures_list = []
        self.bathhouse_structures_list = []

        # Timer
        self.init_time = time.time()
        self.current_time = self.init_time
        self.duration = int(self.current_time-self.init_time)

        # a dic of timers to track dwells with no roads
        # it associates each position of dwell with a timer
        self.timer_track_dwells = {}

    def startGame(self):
        # ---------------------------------#
        pass
    def change_game_speed(self, step):
        """
        A step of 1 indicates incremental speed
        And -1 indicates decremental speed
        """
        if self.framerate > globalVar.DEFAULT_FPS:
            if step == 1 and self.framerate < 10*globalVar.DEFAULT_FPS:
                self.framerate += globalVar.DEFAULT_FPS
            elif step == -1:
                self.framerate -= globalVar.DEFAULT_FPS
        elif self.framerate < globalVar.DEFAULT_FPS:
            if step == 1:
                self.framerate += 0.1*globalVar.DEFAULT_FPS
            elif step == -1 and self.framerate > 0.1*globalVar.DEFAULT_FPS:
                self.framerate -= 0.1*globalVar.DEFAULT_FPS
        else:
            if step == 1:
                self.framerate += globalVar.DEFAULT_FPS
            elif step == -1:
                self.framerate -= 0.1*globalVar.DEFAULT_FPS

    def foodproduction(self):
        # ---------------------------------#
        pass

    def updatebuilding(self, building: buildings.Building):
        current_state = (building.isBurning, building.isDestroyed,building.risk_level_dico["fire"],building.risk_level_dico["collapse"])
        if not building.isDestroyed:
            building.update_risk("fire")
            building.update_risk("collapse")
        updated_state = (building.isBurning, building.isDestroyed,building.risk_level_dico["fire"],building.risk_level_dico["collapse"])
        dico_change = {"fire": current_state[0] != updated_state[0],
                       "collapse" : current_state[1] != updated_state[1],
                       "fire_level" : (current_state[2] != updated_state[2],building.risk_level_dico["fire"]),
                       "collapse_level"  : (current_state[3] != updated_state[3],building.risk_level_dico["collapse"])
                      }
        return  dico_change

    def updateReligion(self):
        pass


    def update_requirements(self, of_what: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                         'basic_entertainment' or 'pottery' or 'bathhouse'):
        """
        This functions searches for water structures on the map and for each one look for dwell within the range of
        the structure. If the dwell required a structure of this type, then its position will be added to the list of
        buildings to update.
        return: a set of positions of housings that will be updated, to avoid duplicate values
        """
        buildings_position_to_append_to_update_object = []
        tmp = of_what+'_structures_list'
        structures_list = getattr(self, tmp)

        for structure in structures_list:
            if not structure.is_functional():
                continue
            _range = structure.range
            _position = structure.position
            for i in range(-_range, _range+1, 1):
                for j in range(-_range, _range + 1, 1):
                    line, column = _position[0]+i, _position[1]+j
                    real_building = self.map.buildings_layer.get_cell(line, column)
                    if real_building.dic['version'] == "dwell" and real_building.is_required(of_what):
                        real_building.update_with_supply(of_what)
                        buildings_position_to_append_to_update_object.append(real_building.position)

        return set(buildings_position_to_append_to_update_object)

    def updategame(self):
        """
        This function updates the game
        In fact it updates the buildings of the game
        Differents types of updates can occur: a building evolving, a building burning or a building collapsing
        """
        self.current_time += 1/self.framerate
        self.duration = int(self.current_time - self.init_time)

        update = updates.LogicUpdate()

        update.has_evolved += self.update_requirements('water')
        update.has_evolved += self.update_requirements('food')
        update.has_evolved += self.update_requirements('temple')
        update.has_evolved += self.update_requirements('education')
        update.has_evolved += self.update_requirements('fountain')
        update.has_evolved += self.update_requirements('basic_entertainment')
        update.has_evolved += self.update_requirements('pottery')
        update.has_evolved += self.update_requirements('bathhouse')

        for buil in self.updated:
            update.has_evolved.append(buil.position)

        self.updated.clear()
        for k in self.buildinglist:

            pos = k.position
            cases = []
            # We don't want primitive housing (pannel) to burn or to collapse
            if type(k) == buildings.Dwelling and k.current_population < k.max_population:
                while k.current_population < k.max_population:
                    self.create_walker()

            if type(k) == buildings.Dwelling and not k.is_occupied():

                # we check if a road is next to this dwelling, if not we remove it after 5s
                removable = True
                line, column = k.position
                for i in range(-2, 2+1):
                    for j in range(-2, 2+1):
                        if self.map.roads_layer.is_real_road(line + i, column + j):
                            removable = False
                            break
                # update tracktimer of dwells
                built_since = int(self.current_time - self.timer_track_dwells[pos]) if pos in self.timer_track_dwells else 0
                if removable and built_since > 5:
                    # to avoid decreasing money
                    self.money += removing_cost
                    self.remove_element(pos)
                    update.removed.append(pos)
                    self.timer_track_dwells.pop(pos)

                elif built_since > 5:
                    self.timer_track_dwells.pop(pos)

            if k.dic['cells_number'] != 1:
                for i in range(0, k.dic['cells_number']):
                    for j in range(0, k.dic['cells_number']):
                        if (i, j) != (0, 0):
                            cases.append((pos[0] + i, pos[1] + j))

            building_update = self.updatebuilding(k)

            if building_update["fire"]:
                update.catchedfire.append(k.position)
                if k.dic['cells_number'] != 1:
                    for i in cases:
                        self.map.buildings_layer.array[i[0]][i[1]].isBurning = True
                        update.catchedfire.append(i)
            if building_update["collapse"]:
                update.collapsed.append(k.position)
                if k.dic['cells_number'] != 1:
                    for i in cases:
                        self.map.buildings_layer.array[i[0]][i[1]].isDestroyed = True
                        update.collapsed.append(i)

            if building_update["fire_level"][0]:
                update.fire_level_change.append((k.position,building_update["fire_level"][1]))
            if building_update["collapse_level"][0]:
                update.collapse_level_change.append((k.position,building_update["collapse_level"][1]))

        return update
        # ---------------------------------#


    def create_walker(self):
        walker = walkers.Immigrant(0, 20, None, 1 / self.framerate, globalVar.DEFAULT_FPS, self)
        self.walkersAll.append(walker)
        self.walkersGetOut(walker)

    def walkersGetOut(self, walker):
        self.walkersOut.append(walker)
        pass

    def walkersOutUpdates(self, exit=False):  # fps = self.framerate
        if exit:
            for walker in self.walkersOut:
                walker.get_out_city()
        else:
            for walker in self.walkersOut:
                walker.walk_to_a_building((globalVar.TILE_COUNT//2, globalVar.TILE_COUNT // 2 -4 ))
        pass

    def remove_element(self, pos) -> str | None:
        """
        Cette fonction permet d'enlever un element de la map à une position donnée
        On ne peut pas retirer de l'herbe ou une montagne
        """
        if self.money < removing_cost:
            print("Not enough money")
            return None
        line, column = pos[0], pos[1]
        status, element_type, _element = self.map.remove_element_in_cell(line, column)
        if status:
            self.money -= removing_cost
            if element_type == globalVar.LAYER5:
                if self.buildinglist:
                    """
                    # to remove the time tracker if the building is removed before 5s
                    if pos in self.timer_track_dwells:
                        self.timer_track_dwells.pop(pos)
                    """
                    self.buildinglist.remove(_element)
                if type(_element) == buildings.WaterStructure:
                    self.water_structures_list.remove(_element)
        return element_type

    def remove_elements_serie(self, start_pos, end_pos) -> set:
        """
        Pour clean une surface de la carte
        Elle va renvoyer un ensemble set qui contient les layers qui ont été modifiés
        """
        line1, column1 = start_pos[0], start_pos[1]
        line2, column2 = end_pos[0], end_pos[1]

        # 2 ranges qui vont servir à délimiter la surface de la map à clean
        vrange, hrange = None, None

        # le set
        _set = set()

        if line1 >= line2:
            vrange = range(line1, line2 - 1, -1)
        else:
            vrange = range(line2, line1 - 1, -1)

        if column1 <= column2:
            hrange = range(column2, column1 - 1, -1)
        else:
            hrange = range(column1, column2 - 1, -1)

        for i in vrange:
            for j in hrange:
                result = self.remove_element((i, j))
                if result:
                    _set.add(result)
        return _set

    def add_road(self, line, column) -> bool:
        # Precondition: we must have enough money for adding a road
        if self.money < road_dico['cost']:
            print("Not enough money")
            return False
        status = self.map.roads_layer.set_cell_constrained_to_bottom_layer(self.map.collisions_layers, line, column)
        if status:
            self.money -= road_dico['cost']
        return status

    def add_roads_serie(self, start_pos, end_pos, dynamically=False) -> bool:
        # Here we can't precisely calculate the money that will be needed to construct all the roads. we'll estimate
        # that
        estimated_counter_roads = (abs(start_pos[0] - end_pos[0])) + (abs(start_pos[1] - end_pos[1])) + 1
        if self.money < estimated_counter_roads * road_dico['cost']:
            print("Not enough money")
            return False

        status, count = self.map.roads_layer.add_roads_serie(start_pos, end_pos,
                    self.map.collisions_layers, memorize=dynamically)

        if status and not dynamically:
            self.money -= road_dico['cost'] * count
        return status

    def add_building(self, line, column, version) -> bool:
        txt= " ".join(version.split("_"))
        if self.money < building_dico[txt].cost:
            print("Not enough money")
            return False
        # we have to determine the exact class of the building bcause they have not the same prototype
        match version:
            case 'dwell':
                building = buildings.Dwelling(self.map.buildings_layer, globalVar.LAYER5)

            case "fruit_farm" | "olive_farm" | "pig_farm" | "vegetable_farm" | "vine_farm" | "wheat_farm":
                building = buildings.Farm(self.map.buildings_layer, globalVar.LAYER5, version)

            case "well" | "fountain"| "fountain1" | "fountain2" | "fountain3" | "fountain4" | "reservoir":
                building = buildings.WaterStructure(self.map.buildings_layer, globalVar.LAYER5, version)

            case _:
                building = buildings.Building(self.map.buildings_layer, globalVar.LAYER5, version)

        if version in ["fruit_farm", "olive_farm", "vegetable_farm", "vine_farm", "wheat_farm"]:
            # we should check if there is yellow grass on the future positions to check
            cells_number = building.total_cells
            can_build = all([self.map.grass_layer.cell_is_yellow_grass(line+i, column+j)
                             for j in range(0, cells_number) for i in range(0, cells_number)])

            if not can_build:
                return False
        status = self.map.buildings_layer.set_cell_constrained_to_bottom_layer(self.map.collisions_layers, line, column,
                                                                               building)

        if status:
            match version:
                case "fruit_farm" | "olive_farm" | "pig_farm" | "vegetable_farm" | "vine_farm" | "wheat_farm":
                    self.buildinglist.append(building.farm_at_02)
                    self.buildinglist.append(building.farm_at_12)
                    self.buildinglist.append(building.farm_at_01)
                    self.buildinglist.append(building.farm_at_00)
                    self.buildinglist.append(building.farm_at_22)
                    self.buildinglist.append(building.foundation)
                case _:
                    self.buildinglist.append(building)

            if version == "dwell":
                # if user just built a dwell we associate a timer so that the dwell can be removed after x seconds
                self.timer_track_dwells[(line, column)] = time.time()


            self.money -= building_dico[txt].cost
            if type(building) == buildings.WaterStructure:
                self.water_structures_list.append(building)
        return status

    def update_likability(self):
        pass