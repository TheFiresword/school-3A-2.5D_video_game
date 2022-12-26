from Services import servicesGlobalVariables as globalVar
from Services.Service_Game_Data import building_dico, road_dico, removing_cost
from CoreModules.BuildingsManagement.buildingsManagementBuilding import *
from CoreModules.WalkersManagement import walkersManagementWalker as walkers

INIT_MONEY = 1000000000


class Game:
    def __init__(self, _map):
        self.map = _map
        self.money = INIT_MONEY
        self.food = 0
        self.potery = 0
        self.likeability = 0
        self.gods_favors = [0, 0, 0, 0, 0]
        self.caesar_score = 0
        self.unemployement = 0
        self.isPaused = False
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

    def updateReligion(self):
        pass

    def updateFire(self):
        pass

    def updateCollapsing(self):
        pass

    def updateLikeability(self):
        pass

    def updategame(self):
        # ---------------------------------#
        pass
    
    def create_walker(self):
        self.walkersAll.append(walkers.Walker(21,20,None,1/self.framerate))

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
        if self.map.roads_layer.remove_cell(line, column):
            self.money -= removing_cost
            return globalVar.LAYER4
        elif self.map.trees_layer.remove_cell(line, column):
            self.money -= removing_cost
            return globalVar.LAYER3
        elif self.map.buildings_layer.remove_cell(line, column):
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
        building = Building(self.map.buildings_layer, globalVar.LAYER5, version)
        status = self.map.buildings_layer.set_cell_constrained_to_bottom_layer(self.map.collisions_layers, line, column,
                                                                               building)
        if status:
            self.money -= building_dico[version].cost
        return status

    def add_multiple_buildings(self, start_pos, end_pos, version) -> bool:
        # Here we can't precisely calculate the money that will be needed to construct all the roads. we'll estimate
        # that
        estimated_counter_buildings = (abs(start_pos[0] - end_pos[0]) + 1) * (abs(start_pos[1] - end_pos[1]) + 1)
        if self.money < estimated_counter_buildings * building_dico[version].cost:
            print("Not enough money")
            return False
        # building = Building(self.map.buildings_layer, globalVar.LAYER5, version)
        line1, column1 = start_pos[0], start_pos[1]
        line2, column2 = end_pos[0], end_pos[1]

        if line1 >= line2:
            vrange = range(line1, line2 - 1, -1)
        else:
            vrange = range(line2, line1 - 1, -1)

        if column1 <= column2:
            hrange = range(column2, column1 - 1, -1)
        else:
            hrange = range(column1, column2 - 1, -1)


        # a counter that will be returned as the number of roads added
        count = 0
        added = False
        # On dessine une ligne verticale de routes de la ligne de départ jusqu'à la ligne de fin

        for i in vrange:
            for j in hrange:
                if self.add_building(i, j, version):
                    added = True
                    count += 1
        if added:
            self.money -= building_dico[version].cost * count
        return added


