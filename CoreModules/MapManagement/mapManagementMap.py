import arcade
from pyglet.math import Vec2
import math
from Services import servicesGlobalVariables

LAYER1 = "grass"
LAYER2 = "hills"
LAYER3 = "trees"
"""
 A map is constituted by the grass layer, the hills layer and the trees layer.
 But also the walkers list and buildings list 
 The layers are generated with the software Tiled
"""

# A scene is a list of spriteLists
class RealMap():
    def __init__(self):
        self.grass_layer = []
        self.hills_layer = []
        self.trees_layer = []

        self.buildings_list = []
        self.walkers_list = []

        self.map = []

    def setup(self):
        for i in range(servicesGlobalVariables.TILE_COUNT*servicesGlobalVariables.TILE_COUNT):
            self.grass_layer.append(0)
        for i in range(servicesGlobalVariables.TILE_COUNT*servicesGlobalVariables.TILE_COUNT):
            self.hills_layer.append(0)
        for i in range(servicesGlobalVariables.TILE_COUNT*servicesGlobalVariables.TILE_COUNT):
            self.trees_layer.append(0)

        self.map = {LAYER1: self.grass_layer,
                    LAYER2: self.hills_layer,
                    LAYER3: self.trees_layer}

class Map(arcade.Scene):
    def __init__(self, map_file):
        super().__init__()

        # The scaling of the sprites of this layer
        self.map_scaling = servicesGlobalVariables.SPRITE_SCALING

        self.map_file = map_file
        self.tilemap = None

        self.grass_layer = None
        self.hills_layer = None
        self.trees_layer = None

        self.buildings_list = None
        self.walkers_list = None

    def setup(self):

        self.tilemap = arcade.load_tilemap(self.map_file, scaling=self.map_scaling)

        self.grass_layer = self.tilemap.sprite_lists[LAYER1]
        self.hills_layer = self.tilemap.sprite_lists[LAYER2]
        self.trees_layer = self.tilemap.sprite_lists[LAYER3]

        self.add_sprite_list(LAYER1, sprite_list=self.grass_layer)
        self.add_sprite_list(LAYER2, sprite_list=self.hills_layer)
        self.add_sprite_list(LAYER3, sprite_list=self.trees_layer)

        self.buildings_list = arcade.SpriteList()
        self.walkers_list = arcade.SpriteList()
        #self.walkers_list.append(walkersManagementWalker.Walker().walker_sprite)
    def clear(self):
        self.sprite_lists.clear()

    def get_map_center(self):
        center_tile = self.grass_layer[int(len(self.grass_layer)//2 + servicesGlobalVariables.TILE_COUNT//2)]
        return Vec2(center_tile.center_x, center_tile.center_y)



