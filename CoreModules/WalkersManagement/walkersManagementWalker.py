import random, copy
from Services import servicesGlobalVariables as cst
from Services import Service_Walker_Sprite_To_File as wstf
from Services import Service_Static_functions
from CoreModules.BuildingsManagement.buildingsManagementBuilding import Building, Dwelling


# ============================================#
# Relative to pathfinding--We use the library pathfinding
from pathfinding.core.grid import Grid
from pathfinding.finder import *
from pathfinding.finder import msp

right = "right"
left = "left"
up = "up"
down = "down"

"""
    A walker is an entity,with a actual position, a destination (other tile to move to), to walk to the destination tile it has to do 
    at least several steps so we count the number of step (self.compteur)and we deduce the offset for the visual display , the choice 
    to the destination is random between tile with effective roads
    
    Some rules about walkers
    * When a dwell is built immigrants are called till its capacity is reached  ###ok         
    * A walker lives in a house and if he works, he is linked to a work building (farm, prefecture, etc)
    * As soon as he starts working, 
        he stays no more not at home but he is still supposed to reside in his housing (in term of effective) ###ok
        he changes clothes and appearance ###ok
        he walks in the city within a range and distribute its service to the buildings that need it
        
        -But if he is a prefect he is called to wherever a building is burning and has to go there
        -And if he is a cart pusher he does not walk randomly but stays at farm building untill he is asked to push 
             product to somewhere.
    * When his house burns or collapses, he looks for another house that still has space -- if no house is found then
    he leaves the town ###ok
    * When his work building burns or collapses he goes back at home and is reallocated to another task if possible
    
    * We don't take account desirability for now
"""


class Walker:
    def __init__(self, pos_ligne, pos_col, house, zoom, game):

        self.map_associated = game.map
        self.game = game
        # some layers we need
        self.road_layer = game.map.roads_layer
        self.building_layer = game.map.buildings_layer

        self.fps = 10
        self.zoom = zoom
        self.head = right
        self.init_pos = (pos_ligne, pos_col)
        self.dest_pos = None
        self.compteur = 0
        self.offset_x, self.offset_y = 0, 0

        self.house = house
        self.work_building = None

        self.paths_up, self.paths_down, self.paths_left, self.paths_right = wstf.walkers_to_sprite(
            self.__class__.__name__)
        self.direction = list()
        self.current_path_to_follow = []
        self.dest_compteur = 0

        # Id obtained via an iterator
        self.id = Service_Static_functions.get_id()
        self.is_at_home = True

    def walk(self, zoom, back=False):
        self.zoom = zoom

        right_tile = (self.init_pos[0] + 1, self.init_pos[1])
        left_tile = (self.init_pos[0] - 1, self.init_pos[1])
        up_tile = (self.init_pos[0], self.init_pos[1] + 1)
        down_tile = (self.init_pos[0], self.init_pos[1] - 1)

        # If a calculated path has been given with pathfinding, that means the walker has to go to some precise position
        # Then we give each position of the path one by one as destination position and the random calculation is
        # skipped
        if self.current_path_to_follow:
            if self.dest_compteur == 0 and self.compteur == 0:
                pass
            self.dest_pos = self.current_path_to_follow[self.dest_compteur]

        if not self.dest_pos:
            possible = []
            if (not (right_tile[0] == -1 or right_tile[0] == cst.TILE_COUNT or right_tile[1] == -1 or right_tile[
                1] == cst.TILE_COUNT)) and self.road_layer.is_real_road(right_tile[0], right_tile[1]) and self.head != left:
                possible.append(right_tile)

            if (not (left_tile[0] == -1 or left_tile[0] == cst.TILE_COUNT or left_tile[1] == -1 or left_tile[
                1] == cst.TILE_COUNT)) and self.road_layer.is_real_road(left_tile[0], left_tile[1]) and self.head != right:
                possible.append(left_tile)

            if (not (up_tile[0] == -1 or up_tile[0] == cst.TILE_COUNT or up_tile[1] == -1 or up_tile[1] ==
                     cst.TILE_COUNT)) and self.road_layer.is_real_road(up_tile[0], up_tile[1]) and self.head != down:
                possible.append(up_tile)

            if (not (down_tile[0] == -1 or down_tile[0] == cst.TILE_COUNT or down_tile[1] == -1 or down_tile[
                1] == cst.TILE_COUNT)) and self.road_layer.is_real_road(down_tile[0], down_tile[1]) and self.head != up:
                possible.append(down_tile)

            if len(possible) != 0:
                self.dest_pos = random.choice(possible)
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

        # Then, following the destination position we have to calculate the direction of the walker head (like top,
        # bottom, left or right)
        if self.dest_pos == right_tile:
            self.head = right
        elif self.dest_pos == left_tile:
            self.head = left
        elif self.dest_pos == up_tile:
            self.head = up
        elif self.dest_pos == down_tile:
            self.head = down


        if self.compteur < self.fps - 1:
            self.compteur += 1
            (a, b) = self.variation_pos_visuel(self.init_pos, self.dest_pos)
            self.offset_x = a * self.compteur
            self.offset_y = b * self.compteur

        #  When the walker arrives where he had to, we intialise back all the  values
        #  but we set the new init position to the previous destination pos
        else:
            self.init_pos = self.dest_pos
            self.dest_pos = None
            self.offset_x, self.offset_y = (0, 0)
            self.compteur = 0
            if back:
                    if self.dest_compteur >= len(self.current_path_to_follow):
                        self.dest_compteur = 0
                        self.current_path_to_follow.reverse()
                    else:
                        self.current_path_to_follow=self.current_path_to_follow[self.dest_compteur]
                        self.current_path_to_follow.reverse()
                        self.dest_compteur += 1
            else:
                if self.current_path_to_follow:
                    if self.dest_compteur == len(self.current_path_to_follow) - 1:
                        self.dest_compteur = 0
                        self.current_path_to_follow.clear()

                        if type(self) == Immigrant:
                            return cst.IMMIGRANT_INSTALLED
                        elif isinstance(self, Citizen):
                            if self.init_pos == self.road_layer.get_exit_position():
                                return cst.CITIZEN_IS_OUT
                            else:
                                return cst.CITIZEN_ARRIVED

                        return 0
                    else:
                        self.dest_compteur += 1


    def exit_way(self):
        """
        The walker wants to leave the city
        I calculate the path he must take
        Note: The walker can use cells without roads to exit if there is no direct path to the exit
              Indeed, if there is no direct path he couldn't exit, but we want him to necessarily exit
        """
        # We pose that if the walker is already on a path to a building we can't give him another path simultaneously
        if self.current_path_to_follow:
            return None

        exit_pos = self.road_layer.get_exit_position()

        integer_array_associated_with_map = [
            [1 if self.map_associated.cell_is_walkable(row, column, can_walk_on_signal=True)
            else  50 if self.map_associated.cell_is_walkable_desperately(row, column)
            else 0 for column in range(cst.TILE_COUNT)]
            for row in range(cst.TILE_COUNT)]

        pathfinding_grid = Grid(matrix=integer_array_associated_with_map)

        finder = msp.MinimumSpanningTree()

        if self.dest_pos:
            _start = pathfinding_grid.node(self.dest_pos[1], self.dest_pos[0])
        else:
            _start = pathfinding_grid.node(self.init_pos[1], self.init_pos[0])

        _end = pathfinding_grid.node(exit_pos[1], exit_pos[0])

        path, runs = finder.find_path(_start, _end, pathfinding_grid)

        if type(finder) == msp.MinimumSpanningTree:
            path = list(path)
            for i in range(len(path)):
                path[i] = path[i].x, path[i].y

        assert path, "An error occured, walker can't get out the city"
        # We remove the first segment of the path if the walker is in the middle of a cell
        if not self.dest_pos:
            tmp = self.init_pos[1], self.init_pos[0]
            path.remove(tmp)

        self.current_path_to_follow = path
        for count in range(len(self.current_path_to_follow)):
            self.current_path_to_follow[count] = tuple(reversed(self.current_path_to_follow[count]))

        return self.current_path_to_follow

    def variation_pos_visuel(self, depart, arrive):
        if depart[0] < arrive[0] and depart[1] == arrive[1]:
            return cst.TILE_WIDTH * self.zoom / (2 * self.fps), cst.TILE_HEIGHT * self.zoom / (2 * self.fps)
        if depart[0] > arrive[0] and depart[1] == arrive[1]:
            return -1 * cst.TILE_WIDTH * self.zoom / (2 * self.fps), -1 * cst.TILE_HEIGHT * self.zoom / (2 * self.fps)
        if depart[0] == arrive[0] and depart[1] < arrive[1]:
            return cst.TILE_WIDTH * self.zoom / (2 * self.fps), -1 * cst.TILE_HEIGHT * self.zoom / (2 * self.fps)
        if depart[0] == arrive[0] and depart[1] > arrive[1]:
            return -1 * cst.TILE_WIDTH * self.zoom / (2 * self.fps), cst.TILE_HEIGHT * self.zoom / (2 * self.fps)

    def change_profession(self, new_type):
        new = None
        if new_type == "citizen":
            new = Citizen(self.init_pos[0],self.init_pos[1],self.house,self.zoom,self.game,self.fps,self.head,
            self.init_pos,self.dest_pos,self.compteur,self.offset_x,self.offset_y,self.id,self.is_at_home,
                          self.direction,self.current_path_to_follow.copy(),self.dest_compteur)
        elif new_type == "prefect":
            new = Prefect(self.init_pos[0],self.init_pos[1],self.house,self.zoom,self.game,self.fps,self.head,
            self.init_pos,self.dest_pos,self.compteur,self.offset_x,self.offset_y,self.id,self.is_at_home,
                          self.direction,self.current_path_to_follow.copy(),self.dest_compteur)
        elif new_type == "engineer":
            new = Engineer(self.init_pos[0],self.init_pos[1],self.house,self.zoom,self.game,self.fps,self.head,
            self.init_pos,self.dest_pos,self.compteur,self.offset_x,self.offset_y,self.id,self.is_at_home,
                          self.direction,self.current_path_to_follow.copy(),self.dest_compteur)
        return new


    def move_to_another_dwell(self, target_pos, init_pos_adjacence):
        # Normally init_pos is the dwell position
        for adjacence in init_pos_adjacence:
            if self.map_associated.walk_to_a_building(adjacence, None, target_pos, self.current_path_to_follow)[1]:
                return True
        return False


class Immigrant(Walker):

    def __init__(self, pos_ligne, pos_col, house, zoom, game, path=[], building=None):
        super(Immigrant, self).__init__(pos_ligne, pos_col, house, zoom, game)
        self.current_path_to_follow = path
        self.dest_compteur = 0
        self.house = building
        building.current_number_of_employees += cst.WALKER_UNIT

    def settle_in(self):
        """
        Return the same walker but with a different profession
        Or None if he is removed
        """
        # As many immigrants are created when a dwell is built the dwell state must be modified only by the first one
        # but we should also verify that the dwell is not removed before the immigrant goes in
        assert self in self.game.walkersOut
        self.game.walkersOut.remove(self)

        if self.house != self.building_layer.array[self.house.position[0]][self.house.position[1]]:
            # The walker shoud be destroyed
            self.game.walkersAll.remove(self)
            del self
            return None
        if not self.house.is_occupied():
            self.house.set_functional(True)
            self.game.updated.append(self.house)
        # Then we add the walker to the dwell employees
        self.house.add_employee(self.id)
        return self.change_profession("citizen")

    """def find_house(self,path=[]):
        # Parcourir la liste des maisons, trouver celle dans lesquelle peut s'installer(nombre d'habitant, niveau d'habitaion)
        for building in self.game.buildinglist:
            if type(building) == Dwelling and building.current_population<building.max_population:
                if not path:
                    self.current_path_to_follow = self.map_associated.walk_to_a_building(self.init_pos,self.dest_pos,building.position,self.current_path_to_follow)[1]
                self.house = building
                building.current_population += 1
                return
        pass"""

class Citizen(Walker):

    def __init__(self,pos_ligne, pos_col, house, zoom, game,fps,head,init_pos,dest_pos,compteur,offset_x,offset_y,id,
                 is_at_home,direction,current_path,dest_compteur):
        super(Citizen, self).__init__(pos_ligne, pos_col, house, zoom, game)
        self.fps = fps
        self.zoom = zoom
        self.head = head
        self.init_pos = init_pos
        self.dest_pos = dest_pos
        self.compteur = compteur
        self.offset_x, self.offset_y = offset_x, offset_y
        self.house = house
        self.direction = direction
        self.current_path_to_follow = current_path
        self.dest_compteur = dest_compteur
        self.id = id
        self.is_at_home = is_at_home

    def work(self, buildings, game_update_object):
        pass

    def get_out_city(self):
        self.game.walkersAll.remove(self)
        self.game.walkersOut.remove(self)
        if self in self.game.unemployedCitizens:
            self.game.unemployedCitizens.remove(self)
        del self

    def set_working_building(self, building):
        self.work_building = building

class Engineer(Citizen):
    def __init__(self,pos_ligne, pos_col, house, zoom, game,fps,head,init_pos,dest_pos,compteur,offset_x,offset_y,id,
                 is_at_home,direction,current_path, dest_compteur):
        super(Engineer, self).__init__(pos_ligne, pos_col, house, zoom, game,fps,head,init_pos,dest_pos,compteur,offset_x,offset_y,id,
                 is_at_home,direction,current_path,dest_compteur)
        self.fps = fps
        self.zoom = zoom
        self.head = head
        self.init_pos = init_pos
        self.dest_pos = dest_pos
        self.compteur = compteur
        self.offset_x, self.offset_y = offset_x, offset_y
        self.house = house
        self.direction = direction
        self.current_path_to_follow = current_path
        self.dest_compteur = dest_compteur
        self.id = id
        self.is_at_home = is_at_home

    def work(self, buildings, game_update_object):
        """
        This function receives a list of buildings it must reset risk
        """
        for b in buildings:
            b.reset_damage_risk()
            game_update_object.collapse_level_change.append((b.position, self.game.updatebuilding(b)["collapse_level"][1]))
        pass


class Prefect(Citizen):
    def __init__(self,pos_ligne, pos_col, house, zoom, game,fps,head,init_pos,dest_pos,compteur,offset_x,offset_y,id,
                 is_at_home,direction,current_path, dest_compteur):
        super(Prefect, self).__init__(pos_ligne, pos_col, house, zoom, game,fps,head,init_pos,dest_pos,compteur,offset_x,offset_y,id,
                 is_at_home,direction,current_path,dest_compteur)
        self.fps = fps
        self.zoom = zoom
        self.head = head
        self.init_pos = init_pos
        self.dest_pos = dest_pos
        self.compteur = compteur
        self.offset_x, self.offset_y = offset_x, offset_y
        self.house = house
        self.direction = direction
        self.current_path_to_follow = current_path
        self.dest_compteur = dest_compteur
        self.id = id
        self.is_at_home = is_at_home

    def work(self, buildings, game_update_object):
        """
        This function receives a list of buildings it must reset risk
        """
        for b in buildings:
            b.reset_fire_risk()
            game_update_object.fire_level_change.append((b.position, self.game.updatebuilding(b)["fire_level"][1]))
        pass



class Cart_Pusher(Walker):
    def work(self, buildings=[]):
        pass


class Delivery_Boy(Walker):
    def work(self):
        pass


class Market_Trader(Walker):
    def work(self):
        pass