import random

from CoreModules.MapManagement import mapManagementLayer as overlay
import Services.servicesGlobalVariables as globalVar

LAYER1 = "grass"
LAYER2 = "hill"
LAYER3 = "tree"
LAYER4 = "building"


class MapLogic:
    def __init__(self):
        # Booléen qui dit si la map est affichée ou pas
        self.active = True

        # Remplissage de chaque layer de la map

        # -------------------------------------------------------------------------------------------------------------#
        self.grass_layer = overlay.Layer(LAYER1)

        possible_grass = ["00079", "yellow", "normal", "buisson", "00114", "00094"]

        for i in range(0, globalVar.TILE_COUNT):
            for j in range(0, globalVar.TILE_COUNT):
                random_version = random.choice(possible_grass)
                my_grass = {"version": random_version, "cells_number": 1}
                self.grass_layer.set_cell(i, j, my_grass)

        # -------------------------------------------------------------------------------------------------------------#

        self.hills_layer = overlay.Layer(LAYER2)

        my_normal_hill = {"version": "normal", "cells_number": 1}
        my_double_hill = {"version": "double", "cells_number": 2}
        for i in range(0, int(globalVar.TILE_COUNT*3/5)):
            if i % 2 == 0:
                self.hills_layer.set_cell(i, globalVar.TILE_COUNT-10-1, my_normal_hill)
                self.hills_layer.set_cell(i, globalVar.TILE_COUNT - 11 - 1, my_normal_hill)
                self.hills_layer.set_cell(i, globalVar.TILE_COUNT - 12 - 1, my_normal_hill)
            else:
                self.hills_layer.set_cell(i, globalVar.TILE_COUNT-6-1, my_double_hill)

        # -------------------------------------------------------------------------------------------------------------#
        self.trees_layer = overlay.Layer(LAYER3)

        possible_trees = ["normal", "00033", "00012", "00043"]
        for i in range(int(globalVar.TILE_COUNT/4), int(globalVar.TILE_COUNT*3/4)):
            random_version = random.choice(possible_trees)
            my_normal_tree = {"version": random_version, "cells_number": 1}
            self.trees_layer.set_cell(i, 5, my_normal_tree)
            self.trees_layer.set_cell(i, 6, my_normal_tree)

        # -------------------------------------------------------------------------------------------------------------#

        self.building_layer = overlay.Layer(LAYER4)

        # liste de Walker()
        self.walkers_list = []
