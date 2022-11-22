import arcade
from pyglet.math import Vec2
import math
from Services import servicesGlobalVariables
from CoreModules.MapManagement import mapManagementLayer as overlay
LAYER1 = "grass"
LAYER2 = "hills"
LAYER3 = "trees"
LAYER4 = "building"

"""
 A map is constituted by the grass layer, the hills layer and the trees layer.
 But also the walkers list and buildings list 
 The layers are generated with the software Tiled
"""

# A scene is a list of spriteLists
class RealMap():
    def __init__(self):
        # Booléen qui dit si la map est affichée ou pas
        self.active = False

        self.grass_layer = overlay.Layer(LAYER1)
        self.grass_layer.automatic_fill_layer()

        self.hills_layer = overlay.Layer(LAYER2)
        self.trees_layer = overlay.Layer(LAYER3)

        self.building_layer = overlay.Layer(LAYER4)
        # liste de Walker()
        self.walkers_list = []


class MapGraphic(arcade.Scene):
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



