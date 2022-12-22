from Services import servicesGlobalVariables as globalVar

INIT_MONEY = 4000


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

    def walkersGetOut(self):
        pass

    def walkersOutUpdates(self):
        pass

    def remove_element(self, pos):
        """
        Cette fonction permet d'enlever un element de la map à une position donnée
        On ne peut pas retirer de l'herbe ou une montagne
        """
        line, column = pos[0], pos[1]
        if self.map.roads_layer.remove_cell(line, column):
            return globalVar.LAYER4
        elif self.map.trees_layer.remove_cell(line, column):
            return globalVar.LAYER3
        elif self.map.buildings_layer.remove_cell(line, column):
            return globalVar.LAYER5
        return None

    def remove_elements_serie(self, start_pos, end_pos):
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
                if self.map.roads_layer.remove_cell(i, j):
                    _set.add(globalVar.LAYER4)
                elif self.map.trees_layer.remove_cell(i, j):
                    _set.add(globalVar.LAYER3)
                elif self.map.buildings_layer.remove_cell(i, j):
                    _set.add(globalVar.LAYER5)
        return _set

    def add_road(self, line, column) -> bool:
        return self.map.roads_layer.set_cell_constrained_to_bottom_layer(self.map.collisions_layers, line,
                                                                         column)

    def add_roads_serie(self, start_pos, end_pos, dynamically=False) -> bool:
        return self.map.roads_layer.add_roads_serie(start_pos, end_pos, self.map.collisions_layers,
                                                    memorize=dynamically)
