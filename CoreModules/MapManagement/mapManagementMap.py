import random

from CoreModules.MapManagement import mapManagementLayer as overlay
import CoreModules.BuildingsManagement.buildingsManagementBuilding as building
import CoreModules.MapManagement.buildingsManagementRoad as roadoverlay
import CoreModules.MapManagement.tileManagementElement as element
import Services.servicesGlobalVariables as globalVar
import Services.servicesmMapSpriteToFile as nameSprite
# ============================================#
# Relative to pathfinding--We use the library pathfinding
from pathfinding.core.grid import Grid
from pathfinding.finder import *
from pathfinding.finder import msp

class MapLogic:
    def __init__(self):
        # Booléen qui dit si la map est affichée ou pas
        self.active = True

        # Remplissage de chaque layer de la map
        """
        !!!!!!!!!! IMPORTANT """  # POUR PLACER UN ELEMENT DANS UN LAYER, IL FAUT LE CREER ET PAS JUSTE COPIER UN
        # ELEMENT PRECEDEMMENT CREE !!!!!!!!!! L'opérateur = en python est un monstre impitoyable qui m'a arraché les
        # cheveux

        # -------------------------------------------------------------------------------------------------------------#
        # GRASS
        self.grass_layer = overlay.Layer(globalVar.LAYER1)

        possible_grass = ["00079", "00082", "normal", "00091", "buisson", "00114", "00094", "00070", "00221", "00274",
                          "00239", "00081", "00244"]
        possible_yellow_grass = [ "yellow"] + ["000" + str(i)for i in range(18, 30)]

        possible_water_ground = nameSprite.water_types

        for i in range(0, globalVar.TILE_COUNT):
            for j in range(0, globalVar.TILE_COUNT):
                if i <= globalVar.TILE_COUNT//4 and j <= 2*globalVar.TILE_COUNT//5:
                    random_version = random.choice(possible_yellow_grass)
                elif globalVar.TILE_COUNT-7 < i <= globalVar.TILE_COUNT-1:
                    random_version = random.choice(possible_water_ground)
                else:
                    random_version = random.choice(possible_grass)

                my_grass = element.Element(self.grass_layer, globalVar.LAYER1, random_version)
                self.grass_layer.set_cell(i, j, my_grass)

        # -------------------------------------------------------------------------------------------------------------#
        # HILLS
        self.hills_layer = overlay.Layer(globalVar.LAYER2)

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
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
            elif second_random_version == random_2_cell_version:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
            else:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)

            self.hills_layer.set_cell(i, globalVar.TILE_COUNT - 3, my_hill)

        for i in range(int(globalVar.TILE_COUNT * 2 / 5), int(globalVar.TILE_COUNT * 3 / 5)):

            random_1_cell_version = random.choice(possible_1_cell_hills)
            random_2_cell_version = random.choice(possible_2_cell_hills)
            random_3_cell_version = random.choice(possible_3_cell_hills)

            second_random_version = random.choice([random_1_cell_version, random_2_cell_version,
                                                   random_3_cell_version])
            if second_random_version == random_1_cell_version:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
            elif second_random_version == random_2_cell_version:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
            else:
                my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)

            status = self.hills_layer.set_cell(i, globalVar.TILE_COUNT - (i % 7), my_hill)

        for i in range(int(globalVar.TILE_COUNT * 3 / 5), int(globalVar.TILE_COUNT * 4 / 5)):
            for j in range(globalVar.TILE_COUNT - 10, globalVar.TILE_COUNT):
                random_1_cell_version = random.choice(possible_1_cell_hills)
                random_2_cell_version = random.choice(possible_2_cell_hills)
                random_3_cell_version = random.choice(possible_3_cell_hills)

                second_random_version = random.choice([random_1_cell_version, random_2_cell_version,
                                                       random_3_cell_version])
                if second_random_version == random_1_cell_version:
                    my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
                elif second_random_version == random_2_cell_version:
                    my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)
                else:
                    my_hill = element.Element(self.hills_layer, globalVar.LAYER2, second_random_version)

                self.hills_layer.set_cell(i, j, my_hill)

        # -------------------------------------------------------------------------------------------------------------#
        # TREES
        self.trees_layer = overlay.Layer(globalVar.LAYER3)

        possible_trees = ["normal", "00033", "00012", "00043"]
        for i in range(int(globalVar.TILE_COUNT / 4), int(globalVar.TILE_COUNT * 3 / 4)):
            random_version = random.choice(possible_trees)
            my_normal_tree = element.Element(self.trees_layer, globalVar.LAYER3, random_version)
            self.trees_layer.set_cell(i, 5, my_normal_tree)

            my_normal_tree = element.Element(self.trees_layer, globalVar.LAYER3, random_version)
            self.trees_layer.set_cell(i, 7, my_normal_tree)

        # -------------------------------------------------------------------------------------------------------------#
        # ROADS
        middle = int(globalVar.TILE_COUNT * 1 / 2)
        self.roads_layer = roadoverlay.RoadLayer((0, 0),(middle, middle*2-1))

        # -------------------------------------------------------------------------------------------------------------#
        # BUILDINGS
        self.buildings_layer = overlay.Layer(globalVar.LAYER5)
        # -------------------------------------------------------------------------------------------------------------#
        # A list of layers to check for collision
        self.collisions_layers = [self.buildings_layer, self.hills_layer, self.trees_layer, self.roads_layer]

    def get_element_in_cell(self, line, column):
        """
        This function returns the highest level element on a cell
        Priority of elements is as follows: building - road - tree - hill - grass
        return: the type of this element
        """
        if self.buildings_layer.array[line][column].dic['version'] != "null":
            return globalVar.LAYER5
        elif self.roads_layer.array[line][column].dic['version'] != "null":
            return globalVar.LAYER4
        elif self.trees_layer.array[line][column].dic['version'] != "null":
            return globalVar.LAYER3
        elif self.hills_layer.array[line][column].dic['version'] != "null":
            return globalVar.LAYER2
        return globalVar.LAYER1

    def remove_element_in_cell(self, line, column):
        """
        Remove if only it is not grass, not hill
        """
        type = self.get_element_in_cell(line, column)
        for layer in [self.roads_layer, self.buildings_layer, self.trees_layer] :
            if layer.type == type:
                _element = layer.get_cell(line, column)
                status = layer.remove_cell(line, column)
                return status, type, _element
        return False, None, None
    def cell_is_walkable(self, line, column, can_walk_on_signal=False):
        """A cell is walkable when it contains a valid road"""
        if can_walk_on_signal:
            return self.get_element_in_cell(line, column) == globalVar.LAYER4
        return self.get_element_in_cell(line, column) == globalVar.LAYER4 and self.roads_layer.is_real_road(line,
                                                                                                            column)

    def cell_is_walkable_desperately(self, line, column):
        """A cell is walkable desperately when it is just a grass"""
        return self.get_element_in_cell(line, column) == globalVar.LAYER1
    

    def walk_to_a_building(self,init_pos,dest_pos=None, building_target_pos=None,current_path_to_follow=None) -> bool:
        """
        This function uses pathfinding to calculate the path that a walker should follow to move from its position to
        a building position.
        This path is calculated with the library pathfinding
        param: building_target_pos: a tuple
        It returns if the path has been effectively calculated
        """
        # We pose that if the walker is already on a path to a building we can't give him another path simultaneously
        if current_path_to_follow:
            return False,[]
        # I create an array that associates value 1 to any road that is not 'null' and 0 if not.
        integer_array_associated_with_roads_layer = [
            [1 if self.cell_is_walkable(row, column) else 0 for column in range(globalVar.TILE_COUNT) ]
            for row in range(globalVar.TILE_COUNT)]

        pathfinding_grid = Grid(matrix=integer_array_associated_with_roads_layer)

        finder = bi_a_star.AStarFinder()


        line, column = building_target_pos

        cells_number = self.buildings_layer.get_cells_number(line, column)

        # If the building is a dwell then the walker can walk to it if there is a road in a range of 2 cells
        building = self.buildings_layer.get_cell(line, column)
        dwell = building.dic['version'] == 'dwell'
        assert cells_number

        path_founds = []

        possible_cells_to_approch_target = []
        for i in range(cells_number):
            if self.roads_layer.is_real_road(line + i, column - 1):
                possible_cells_to_approch_target.append((line + i, column - 1))
            # If the building is a dwell then the walker can walk to it if there is a road in a range of 2 cells
            elif self.roads_layer.is_real_road(line + i, column - 2) and dwell:
                possible_cells_to_approch_target.append((line + i, column - 2))

            if self.roads_layer.is_real_road(line - 1, column + i):
                possible_cells_to_approch_target.append((line - 1, column + i))
            elif self.roads_layer.is_real_road(line - 2, column + i) and dwell:
                possible_cells_to_approch_target.append((line - 2, column + i))


            if self.roads_layer.is_real_road(line + cells_number, column + i):
                possible_cells_to_approch_target.append((line + cells_number, column + i))
            elif self.roads_layer.is_real_road(line + cells_number + 1, column + i) and dwell:
                possible_cells_to_approch_target.append((line + cells_number + 1, column + i))

            if self.roads_layer.is_real_road(line + i, column + cells_number):
                possible_cells_to_approch_target.append((line + i, column + cells_number))
            elif self.roads_layer.is_real_road(line + i, column + cells_number+1) and dwell:
                possible_cells_to_approch_target.append((line + i, column + cells_number+1))

        # we have to take in consideration the case where the walker is already walking to a random destination
        # then the start position for the pathfinding is considered to be this destination
        if dest_pos:
            _start = pathfinding_grid.node(dest_pos[1], dest_pos[0])
        else:
            _start = pathfinding_grid.node(init_pos[1], init_pos[0])

        for i in range(len(possible_cells_to_approch_target)):
            pathfinding_grid.cleanup()
            _end = pathfinding_grid.node(possible_cells_to_approch_target[i][1],
                                              possible_cells_to_approch_target[i][0])

            path, runs = finder.find_path(_start, _end, pathfinding_grid)
            if path:
                # we have a valide path, so we have to move the walker with this path
                # ie a list of destpos; ex: path = [(1,1), (2, 2)]
                if not dest_pos:
                    tmp = init_pos[1], init_pos[0]
                    path.remove(tmp)
                path_founds.append(path)


        if path_founds:
            # we have at least one valid path, we choose the smallest one and we move the walker through this path
            # ie a list of destpos; ex: path = [(1,1), (2, 2)]
            current_path_to_follow = min(path_founds, key=len)
            # then we reverse each tuple because the implementation of Grid nodes in the library pathfinding considers
            # that our row is their column
            for count in range(len(current_path_to_follow)):
                current_path_to_follow[count] = tuple(reversed(current_path_to_follow[count]))

            # print(f'taille: {len(path_founds)} -- {self.current_path_to_follow}')
            return True,current_path_to_follow
        # There is no path to this building
        # print("Sorry no path")
        return False,current_path_to_follow


    def path_entry_to_exit(self, entry, exit):
        integer_array_associated_with_map = [
            [1 if self.cell_is_walkable_desperately(row, column) else 0 for column in range(globalVar.TILE_COUNT)]
            for row in range(globalVar.TILE_COUNT)]

        pathfinding_grid = Grid(matrix=integer_array_associated_with_map)

        finder = bi_a_star.AStarFinder()

        if entry[0] == 0 or entry[0] == globalVar.TILE_COUNT-1:
            entry_cell = (entry[0], entry[1]+1)
        else:
            entry_cell = (entry[0]+1, entry[1])
        if exit[0] == 0 or exit[0] == globalVar.TILE_COUNT-1:
            exit_cell = (exit[0], exit[1]+1)
        else:
            exit_cell = (exit[0]+1, exit[1])

        _start = pathfinding_grid.node(entry_cell[1], entry_cell[0])
        _end = pathfinding_grid.node(exit_cell[1], exit_cell[0])
        path, runs = finder.find_path(_start, _end, pathfinding_grid)
        assert path
        for count in range(len(path)):
            path[count] = tuple(reversed(path[count]))
        return path