import random
from Services import servicesGlobalVariables as cst
from Services import Service_Walker_Sprite_To_File as wstf

#============================================#
# Relative to pathfinding--We use the library pathfinding
from pathfinding.core.grid import Grid
from pathfinding.finder import *

right = "right"
left = "left"
up = "up"
down = "down"

"""
    A walker is an entity,with a actual position, a destination (other tile to move to), to walk to the destination tile it has to do 
    at least several steps so we count the number of step (self.compteur)and we deduce the offset for the visual display , the choice 
    to the destination is random between tile with effective roads
"""


class Walker:
    def __init__(self, pos_ligne, pos_col, house, fps,zoom):
        self.fps = fps
        self.zoom = zoom
        self.head = left
        self.init_pos = (pos_ligne, pos_col)
        self.dest_pos = None
        self.compteur = 0
        self.offset_x, self.offset_y = 0, 0
        # self.init_pos[0] = pos_ligne
        # self.init_pos[1] = pos_col
        self.house = house
        self.paths_up, self.paths_down, self.paths_left, self.paths_right = wstf.walkers_to_sprite(self.__class__.__name__)
        self.direction = list()

        self.pathfinding_grid = Grid()

    def walk(self, road_layer):
        if not self.dest_pos:
            ran = 0
            self.direction.clear()

            r = (self.init_pos[0], self.init_pos[1] + 1)
            le = (self.init_pos[0], self.init_pos[1] - 1)
            u = (self.init_pos[0] + 1, self.init_pos[1])
            d = (self.init_pos[0] - 1, self.init_pos[1])
            (rr, ll, uu, dd) = ((road_layer.array[r[0]][r[1]]).dic["version"] != "null",
                                (road_layer.array[le[0]][le[1]]).dic["version"] != "null",
                                (road_layer.array[u[0]][u[1]]).dic["version"] != "null",
                                (road_layer.array[d[0]][d[1]]).dic["version"] != "null"
                                )
            """if (road_layer.array[r[0]][r[1]]).dic["version"] != "null":
                rr = True
            if (road_layer.array[le[0]][le[1]]).dic["version"] != "null":
               ll = True
            if (road_layer.array[u[0]][u[1]]).dic["version"] != "null":
                uu = True
            if (road_layer.array[d[0]][d[1]]).dic["version"] != "null":
                dd = True"""

            if self.head == right:
                if not (rr or dd or uu):
                    self.direction.append(left)
                else:
                    if rr:
                        self.direction.append(right)
                    if uu:
                        self.direction.append(up)
                    if dd:
                        self.direction.append(down)
            elif self.head == up:
                if not (rr or ll or uu):
                    self.direction.append(down)
                else:
                    if rr:
                        self.direction.append(right)
                    if uu:
                        self.direction.append(up)
                    if ll:
                        self.direction.append(left)
            elif self.head == left:
                if not (ll or dd or uu):
                    self.direction.append(right)
                else:
                    if ll:
                        self.direction.append(left)
                    if uu:
                        self.direction.append(up)
                    if dd:
                        self.direction.append(down)
            elif self.head == down:
                if not (rr or dd or ll):
                    self.direction.append(up)
                else:
                    if rr:
                        self.direction.append(right)
                    if ll:
                        self.direction.append(left)
                    if dd:
                        self.direction.append(down)

            ran = random.randint(0, len(self.direction))
            if self.direction[ran - 1] == right:
                self.dest_pos = (self.init_pos[0] + 1, self.init_pos[1])
                # self.init_pos[0] += 1
                self.head = right
            elif self.direction[ran - 1] == left:
                self.dest_pos = (self.init_pos[0] - 1, self.init_pos[1])
                # self.init_pos[0] -= 1
                self.head = left
            elif self.direction[ran - 1] == up:
                self.dest_pos = (self.init_pos[0], self.init_pos[1] + 1)
                # self.init_pos[1] += 1
                self.head = up
            elif self.direction[ran - 1] == down:
                self.dest_pos = (self.init_pos[0], self.init_pos[1] - 1)
                # self.init_pos[1] -= 1
                self.head = down
        else:
            if self.compteur != self.fps:
                self.compteur += 1
                self.offset_x, self.offset_y = self.variation_pos_visuel(self, self.init_pos,
                                                                         self.dest_pos) * self.compteur
            else:
                self.init_pos = self.dest_pos
                self.dest_pos = None
                self.offset_x, self.offset_y = (0, 0)
                self.compteur = 0

    def walk2(self, road_layer,zoom):
        self.zoom = zoom
        if not self.dest_pos:
            right_tile = (self.init_pos[0] + 1, self.init_pos[1])
            left_tile = (self.init_pos[0] - 1, self.init_pos[1])
            up_tile = (self.init_pos[0], self.init_pos[1] + 1)
            down_tile = (self.init_pos[0], self.init_pos[1] - 1)
            possible = []
            if (not (right_tile[0] == -1 or right_tile[0] == cst.TILE_COUNT or right_tile[1] == -1 or right_tile[
                1] == cst.TILE_COUNT)) and (road_layer.array[right_tile[0]][right_tile[1]]).dic["version"] not in [
                "null", "entry", "exit"] and self.head != left:
                possible.append(right_tile)

            if (not (left_tile[0] == -1 or left_tile[0] == cst.TILE_COUNT or left_tile[1] == -1 or left_tile[
                1] == cst.TILE_COUNT)) and (road_layer.array[left_tile[0]][left_tile[1]]).dic["version"] not in [
                "null", "entry", "exit"] and self.head != right:
                possible.append(left_tile)

            if (not (up_tile[0] == -1 or up_tile[0] == cst.TILE_COUNT or up_tile[1] == -1 or up_tile[
                1] == cst.TILE_COUNT)) and (road_layer.array[up_tile[0]][up_tile[1]]).dic["version"] not in [
                "null", "entry", "exit"] and self.head != down:
                possible.append(up_tile)

            if (not (down_tile[0] == -1 or down_tile[0] == cst.TILE_COUNT or down_tile[1] == -1 or down_tile[
                1] == cst.TILE_COUNT)) and (road_layer.array[down_tile[0]][down_tile[1]]).dic["version"] not in [
                "null","entry","exit"] and self.head != up:
                possible.append(down_tile)

            if len(possible) != 0:
                self.dest_pos = random.choice(possible)
                if self.dest_pos == right_tile:
                    self.head = right
                elif self.dest_pos == left_tile:
                    self.head = left
                elif self.dest_pos == up_tile:
                    self.head = up
                elif self.dest_pos == down_tile:
                    self.head = down
            else:
                if self.head == right:
                    self.dest_pos = left_tile
                    self.head = left
                elif self.head == left:
                    self.dest_pos = right_tile
                    self.head = right
                elif self.head == up:
                    self.dest_pos = down_tile
                    self.head = down
                elif self.head == down:
                    self.dest_pos = up_tile
                    self.head = up

        else:
            if self.compteur < self.fps - 1:
                self.compteur += 1
                (a, b) = self.variation_pos_visuel(self.init_pos, self.dest_pos)
                self.offset_x = a * self.compteur
                self.offset_y = b * self.compteur
            else:
                self.init_pos = self.dest_pos
                self.dest_pos = None
                self.offset_x, self.offset_y = (0, 0)
                self.compteur = 0

    def walk_to_a_building(self, road_layer, building_layer, building_target_pos):
        """
        This function uses pathfinding to calculate the path that a walker should follow to move from its position to
        a building position.
        This path is calculated with the library pathfinding
        param: road_layer
        param: building_target_pos: a tuple
        """
        self.pathfinding_grid.clear()
        self.pathfinding_grid = Grid(matrix=road_layer)
        finder = best_first.BestFirst()
        line, column = building_target_pos
        cells_number = building_layer[line][column].dic['cells_number']
        possible_cells_to_approch_target = []
        for i in range(cells_number):
            possible_cells_to_approch_target.append((line + i, column - 1))
            possible_cells_to_approch_target.append((line - 1, column + i))
            possible_cells_to_approch_target.append((line + cells_number, column + i))
            possible_cells_to_approch_target.append((line + i, column + cells_number))

        for i in range(len(possible_cells_to_approch_target)):
            _end = self.pathfinding_grid.node(possible_cells_to_approch_target[i])
            path, runs = finder.find_path(self.init_pos, _end, self.pathfinding_grid)
            if path:
                # we have a valide path, so we have to move the walker with this path
                # ie a list of destpos; ex: path = [(1,1), (2, 2)]
                pass
    def work(self):
        pass

    def variation_pos_visuel(self, depart, arrive):
        if depart[0] < arrive[0] and depart[1] == arrive[1]:
            return (cst.TILE_WIDTH*self.zoom / (2 * self.fps), cst.TILE_HEIGHT*self.zoom / (2 * self.fps))
        if depart[0] > arrive[0] and depart[1] == arrive[1]:
            return (-1 * cst.TILE_WIDTH *self.zoom/ (2 * self.fps), -1 * cst.TILE_HEIGHT*self.zoom / (2 * self.fps))
        if depart[0] == arrive[0] and depart[1] < arrive[1]:
            return (cst.TILE_WIDTH*self.zoom / (2 * self.fps), -1 * cst.TILE_HEIGHT*self.zoom / (2 * self.fps))
        if depart[0] == arrive[0] and depart[1] > arrive[1]:
            return (-1 * cst.TILE_WIDTH*self.zoom / (2 * self.fps), cst.TILE_HEIGHT*self.zoom / (2 * self.fps))


class Engineer(Walker):
    def work(self):
        pass


class Prefect(Walker):
    def work(self):
        pass


class Immigrant(Walker):
    def find_house(self):
        # Parcourir la liste des maisons, trouver celle dans lesquelle peut s'installer(nombre d'habitant, niveau d'habitaion)
        pass


class Cart_Pusher(Walker):
    def work(self):
        pass


class Delivery_Boy(Walker):
    def work(self):
        pass


class Market_Trader(Walker):
    def work(self):
        pass