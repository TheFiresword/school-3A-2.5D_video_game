from Services import servicesGlobalVariables as globalVar
from Services.Service_Game_Data import building_dico, road_dico, removing_cost
from CoreModules.BuildingsManagement import buildingsManagementBuilding as buildings
from CoreModules.WalkersManagement import walkersManagementWalker as walkers

INIT_MONEY = 1000000000


class Game:
    def __init__(self, _map,name="save"):
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

    def print_money(self):
        print("#========You have " + str(self.money) + " left========#")

    def startGame(self):
        # ---------------------------------#
        pass

    def foodproduction(self):
        # ---------------------------------#
        pass
    
    def updatebuilding(self,building:buildings.Building):
        if not building.isDestroyed:
            building.update_risk("fire")
            building.update_risk("collapse")
        pass

    def updateReligion(self):
        pass

    

    

    def updategame(self):
        self.automatic_building_update()
        # ---------------------------------#
        pass
    
    def create_walker(self):
        self.walkersAll.append(walkers.Walker(globalVar.TILE_COUNT-2,20,None,1/self.framerate))

    def walkersGetOut(self):
        for k in self.walkersAll:
            self.walkersOut.append(k)
        pass

    def walkersOutUpdates(self,fps): #fps = 1/self.framerate
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

        road,tree,building = self.map.roads_layer.get_cell(line,column),self.map.trees_layer.get_cell(line,column),self.map.buildings_layer.get_cell(line,column)

        if road.dic["version"] != "null":
            if self.map.roads_layer.remove_cell(line, column):
                self.money -= removing_cost
                return globalVar.LAYER4
        elif tree.dic["version"] != "null":
            if self.map.trees_layer.remove_cell(line, column):
                self.money -= removing_cost
                return globalVar.LAYER3
        elif building.dic["version"] != "null": 
            if self.map.buildings_layer.remove_cell(line, column):
                if self.buildinglist:
                    self.buildinglist.remove(building)
                self.money -= removing_cost
                return globalVar.LAYER5
        return None

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
        status, count = self.map.roads_layer.add_roads_serie(start_pos, end_pos, self.map.collisions_layers,
                                                             memorize=dynamically)
        if status:
            self.money -= road_dico['cost'] * count
        return status

    def add_building(self, line, column, version) -> bool:
        if self.money < building_dico[version].cost:
            print("Not enough money")
            return False
        # we have to determine the exact class of the building bcause they have not the same prototype
        match version:
            case 'dwell':
                building = buildings.Dwelling(self.map.buildings_layer, globalVar.LAYER5)
                self.buildinglist.append(building)
            case "fruit_farm" | "olive_farm" | "pig_farm" | "vegetable_farm" | "vine_farm" | "wheat_farm":
                building = buildings.Farm(self.map.buildings_layer, globalVar.LAYER5, version)
                self.buildinglist.append(building.farm_at_02)
                self.buildinglist.append(building.farm_at_12)
                self.buildinglist.append(building.farm_at_01)
                self.buildinglist.append(building.farm_at_00)
                self.buildinglist.append(building.farm_at_22)
                self.buildinglist.append(building.foundation)
            case _:
                building = buildings.Building(self.map.buildings_layer, globalVar.LAYER5, version)
                self.buildinglist.append(building)

        status = self.map.buildings_layer.set_cell_constrained_to_bottom_layer(self.map.collisions_layers, line, column,
                                                                               building)

        if status:
            self.money -= building_dico[version].cost
        return status

    def automatic_building_update(self):
        for k in self.buildinglist:
            self.updatebuilding(k)
        pass