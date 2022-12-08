import random

from CoreModules.MapManagement import mapManagementLayer as overlay
import CoreModules.BuildingsManagement.buildingsManagementBuilding as building
import Services.servicesGlobalVariables as globalVar

LAYER1 = "grass"
LAYER2 = "hill"
LAYER3 = "tree"
LAYER4 = "road"
LAYER5 = "building"


class MapLogic:
    def __init__(self):
        # Booléen qui dit si la map est affichée ou pas
        self.active = True

        # Remplissage de chaque layer de la map

        # -------------------------------------------------------------------------------------------------------------#
        # GRASS
        self.grass_layer = overlay.Layer(LAYER1)

        possible_grass = ["00079", "yellow", "00082", "normal", "00091", "buisson", "00114", "00094", "00027", "00070"]

        for i in range(0, globalVar.TILE_COUNT):
            for j in range(0, globalVar.TILE_COUNT):
                random_version = random.choice(possible_grass)
                my_grass = {"version": random_version, "cells_number": 1}
                self.grass_layer.set_cell(i, j, my_grass)

        # -------------------------------------------------------------------------------------------------------------#
        # HILLS
        self.hills_layer = overlay.Layer(LAYER2)

        possible_1_cell_hills = ["small-mountain1", "small-mountain2", "small-mountain3", "small-mountain4",
                                 "small-mountain5", "small-mountain6", "small-mountain7", "small-mountain8"]

        possible_2_cell_hills = ["big-mountain1", "big-mountain2", "big-mountain3"]

        possible_3_cell_hills = ["geant-mountain1", "geant-mountain2"]

        for i in range(0, int(globalVar.TILE_COUNT * 2 / 5)):
            random_1_cell_version = random.choice(possible_1_cell_hills)
            random_2_cell_version = random.choice(possible_2_cell_hills)
            random_3_cell_version = random.choice(possible_3_cell_hills)

            second_random_version = random.choice([random_1_cell_version, random_2_cell_version, random_3_cell_version])
            if second_random_version == random_1_cell_version:
                the_dic = {"version": second_random_version, "cells_number": 1}
            elif second_random_version == random_2_cell_version:
                the_dic = {"version": second_random_version, "cells_number": 3}
            else:
                the_dic = {"version": second_random_version, "cells_number": 4}

            self.hills_layer.set_cell(i, globalVar.TILE_COUNT - 3, the_dic)

        for i in range(int(globalVar.TILE_COUNT * 2 / 5), int(globalVar.TILE_COUNT * 3 / 5)):

            random_1_cell_version = random.choice(possible_1_cell_hills)
            random_2_cell_version = random.choice(possible_2_cell_hills)
            random_3_cell_version = random.choice(possible_3_cell_hills)

            second_random_version = random.choice([random_1_cell_version, random_2_cell_version,
                                                   random_3_cell_version])
            if second_random_version == random_1_cell_version:
                the_dic = {"version": second_random_version, "cells_number": 1}
            elif second_random_version == random_2_cell_version:
                the_dic = {"version": second_random_version, "cells_number": 3}
            else:
                the_dic = {"version": second_random_version, "cells_number": 4}

            status = self.hills_layer.set_cell(i, globalVar.TILE_COUNT - (i % 7), the_dic)

        for i in range(int(globalVar.TILE_COUNT * 3 / 5), int(globalVar.TILE_COUNT * 4 / 5)):
            for j in range(globalVar.TILE_COUNT - 10, globalVar.TILE_COUNT):
                random_1_cell_version = random.choice(possible_1_cell_hills)
                random_2_cell_version = random.choice(possible_2_cell_hills)
                random_3_cell_version = random.choice(possible_3_cell_hills)

                second_random_version = random.choice([random_1_cell_version, random_2_cell_version,
                                                       random_3_cell_version])
                if second_random_version == random_1_cell_version:
                    the_dic = {"version": second_random_version, "cells_number": 1}
                elif second_random_version == random_2_cell_version:
                    the_dic = {"version": second_random_version, "cells_number": 3}
                else:
                    the_dic = {"version": second_random_version, "cells_number": 4}

                self.hills_layer.set_cell(i, j, the_dic)

        # -------------------------------------------------------------------------------------------------------------#
        # TREES
        self.trees_layer = overlay.Layer(LAYER3)

        possible_trees = ["normal", "00033", "00012", "00043"]
        for i in range(int(globalVar.TILE_COUNT / 4), int(globalVar.TILE_COUNT * 3 / 4)):
            random_version = random.choice(possible_trees)
            my_normal_tree = {"version": random_version, "cells_number": 1}
            self.trees_layer.set_cell(i, 5, my_normal_tree)
            self.trees_layer.set_cell(i, 6, my_normal_tree)

        # -------------------------------------------------------------------------------------------------------------#
        # ROADS
        self.roads_layer = overlay.Layer(LAYER4)
        my_normal_road = {"version": "normal", "cells_number": 1}
        entry_road = {"version": "entry", "cells_number": 1}
        exit_road = {"version": "exit", "cells_number": 1}
        middle = int(globalVar.TILE_COUNT * 1 / 2)
        self.roads_layer.set_cell(2 * middle - 1, middle - 1, entry_road)
        self.roads_layer.set_cell(0, middle - 1, exit_road)

        for i in range(0, 2 * middle):
            self.roads_layer.set_cell_constrained_to_bottom_layer([self.hills_layer, self.trees_layer],
                                                                  i, middle, my_normal_road)

        # -------------------------------------------------------------------------------------------------------------#
        # BUILDINGS
        self.buildings_layer = building.BuildingLayer(LAYER5)
        my_dwelling = building.Dwelling(self.buildings_layer, LAYER5, 1, 0, 10)
        for i in range(0, 10):
            self.buildings_layer.set_cell(globalVar.TILE_COUNT-3, 2+i, my_dwelling)

        # liste de Walker()
        self.walkers_list = []
