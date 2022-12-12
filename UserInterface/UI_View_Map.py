import arcade
import arcade.gui

from Services import servicesGlobalVariables as constantes
from Services import servicesmMapSpriteToFile as map_sprite
from Services import Service_Game_Data as gdata

from CoreModules.MapManagement.mapManagementMap import LAYER1, LAYER2, LAYER3, LAYER4, LAYER5
from pyglet.math import Vec2

from UserInterface import UI_Section as uis
from UserInterface import UI_buttons
from UserInterface import  UI_HUD_Build as hudb
MAP_CAMERA_SPEED = 0.5
"""
 A map is constituted by the grass layer, the hills layer and the trees layer.
 But also the walkers list and buildings list 
 The layers are generated with the software Tiled
"""


class MapView(arcade.View):
    # Notes: Rescale function
    red_sprite = arcade.Sprite()
    tmp = False

    def __init__(self, logic_map):
        super().__init__()
        # self.map = MapGraphic(mapManagementMap.MapLogic())
        # The scaling of the sprites of this layer
        self.map_scaling = constantes.SPRITE_SCALING

        # Pour utiliser la logique
        self.logic_map = logic_map

        self.grass_layer = None
        self.hills_layer = None
        self.trees_layer = None
        self.roads_layer = None
        self.buildings_layer = None

        self.walkers_list = None

        # Les tableaux logiques des layers
        self.grass_array = []
        self.hills_array = []
        self.trees_array = []
        self.roads_array = []
        self.buildings_array = []

        # 4 booleans to check the key pressed
        self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed = False, False, False, False

        self.setup()

        self.convert_map_cartesian_to_isometric()

        # a camera to travel through the map
        # set up the camera and centre it
        self.map_camera = arcade.Camera()
        self.menu_camera = arcade.Camera()

        self.center_map()

        ##############################

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.secmanager = arcade.SectionManager(view=self)
        self.menusect = uis.MenuSect()
        self.secmanager.add_section(self.menusect)
        self.tab = arcade.load_texture(constantes.SPRITE_PATH + "PanelsOther/paneling_00017.png")
        buttons_render = UI_buttons.buttons
        self.buttons = [arcade.gui.UITextureButton(x=b0, y=b1, texture=b2, texture_hovered=b3, texture_pressed=b4) for
                        (b0, b1, b2, b3, b4) in buttons_render]
        # self.b1 = constantes.DEFAULT_SCREEN_WIDTH - 155,
        #                                     y=constantes.DEFAULT_SCREEN_HEIGHT - 200 , texture=arcade.load_texture(
        #        constantes.SPRITE_PATH + "Panel/Panel13/paneling_00080.png"),
        #                                     texture_hovered=arcade.load_texture(
        #                                         constantes.SPRITE_PATH + "Panel/Panel13/paneling_00081.png"),
        #                                     texture_pressed=arcade.load_texture(
        #                                         constantes.SPRITE_PATH + "Panel/Panel13/paneling_00079.png"))

        for k in self.buttons:
            self.manager.add(k)
        arcade.set_background_color(arcade.color.BLACK)
        self.builder_mode = False

    def setup(self):
        # On crée les SpriteList pour chaque layer
        self.grass_layer = arcade.SpriteList()
        self.hills_layer = arcade.SpriteList()
        self.trees_layer = arcade.SpriteList()
        self.roads_layer = arcade.SpriteList()
        self.buildings_layer = arcade.SpriteList()

        # On récupère le tableau logique associé à chaque layer
        self.grass_array = self.logic_map.grass_layer.array
        self.hills_array = self.logic_map.hills_layer.array
        self.trees_array = self.logic_map.trees_layer.array
        self.roads_array = self.logic_map.roads_layer.array
        self.buildings_array = self.logic_map.buildings_layer.array

        # On remplit les SpriteList de chaque layer
        self.create_sprite_list(self.grass_layer, LAYER1, self.grass_array)
        self.create_sprite_list(self.hills_layer, LAYER2, self.hills_array)
        self.create_sprite_list(self.trees_layer, LAYER3, self.trees_array)
        self.create_sprite_list(self.roads_layer, LAYER4, self.roads_array)
        self.create_sprite_list(self.buildings_layer, LAYER5, self.buildings_array)

        self.walkers_list = arcade.SpriteList()

    def create_sprite_list(self, layer, layer_name, array):
        for i in range(0, len(array)):  # I=On parcout le tableau logique du bas vers le haut
            line = array[i]
            for j in range(0, len(line)):
                file_name = map_sprite.mapping_function(layer_name, array[i][j].dic['version'])
                if file_name != "":
                    _sprite = arcade.Sprite(file_name, self.map_scaling)
                else:
                    _sprite = arcade.Sprite()
                # Les coordonnées de départ sont en cartésien
                count = array[i][j].dic['cells_number']
                overflowing_width = (_sprite.width - constantes.TILE_WIDTH * self.map_scaling * count) / 2
                overflowing_height = (_sprite.height - constantes.TILE_HEIGHT * self.map_scaling * count) / 2

                _sprite.center_x = constantes.TILE_WIDTH * self.map_scaling * (j + 1 / 2 + (count - 1) / 2) + \
                                   overflowing_width
                _sprite.center_y = constantes.TILE_HEIGHT * self.map_scaling * (i + 1 / 2 + (count - 1) / 2) + \
                                   overflowing_height
                layer.append(_sprite)

    def on_show_view(self):
        self.secmanager.enable()

    def on_draw(self):
        self.clear()

        self.map_camera.use()
        # On draw la map que si elle est activée
        if self.logic_map.active:
            self.grass_layer.draw()
            self.hills_layer.draw()
            self.trees_layer.draw()
            self.roads_layer.draw()
            self.buildings_layer.draw()
            if self.tmp: self.red_sprite.draw_hit_box(color=(255, 0, 0), line_thickness=1)

        if self.builder_mode:
            sprite = hudb.hollow_build(self.mouse_pos[0], self.mouse_pos[1], gdata.building_dico["Dwell"])
            sprite.draw()

        self.menu_camera.use()
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH - 81,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - 275 - 25,
                                      width=162, height=constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                      texture=self.tab)
        self.manager.draw()

    def on_hide(self):
        self.manager.disable()
        self.secmanager.disable()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """
        Quand on clique un sprite orange se dessine sur le sprite le plus proche du point cliqué
        """
        (x, y) = Vec2(x, y) + self.map_camera.position
        self.tmp = True
        self.red_sprite = arcade.Sprite("./Assets/sprites/C3/Land/LandOverlay/Land2a_00037.png",
                                        scale=self.map_scaling, center_x=x,
                                        center_y=y, hit_box_algorithm="Detailed")

        (nearest_sprite, d) = arcade.get_closest_sprite(self.red_sprite, self.grass_layer)
        self.red_sprite.center_x, self.red_sprite.center_y = nearest_sprite.center_x, nearest_sprite.center_y

    def on_update(self, delta_time: float):
        self.grass_layer.update()
        self.hills_layer.update()
        self.trees_layer.update()
        self.roads_layer.update()
        self.buildings_layer.update()

        self.move_map_camera_with_keys()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """
        A mouse scroll generates a rescaling of the map if it's possible
        """

        if scroll_y < 0:
            next_scaling = self.map_scaling * 0.9
            if constantes.SCALE_MIN < self.map_scaling and constantes.SCALE_MIN < \
                    next_scaling:
                self.rescale_the_map(next_scaling)

            else:
                self.rescale_the_map(constantes.SCALE_MIN)
        else:
            next_scaling = self.map_scaling * 1.1
            if self.map_scaling < constantes.SCALE_MAX and constantes.SCALE_MAX > \
                    next_scaling:
                self.rescale_the_map(next_scaling)

            else:
                self.rescale_the_map(constantes.SCALE_MAX)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
        if symbol == arcade.key.UP:
            self.up_pressed = True
        elif symbol == arcade.key.DOWN:
            self.down_pressed = True
        elif symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol == arcade.key.B:
            self.builder_mode = True
        elif symbol == arcade.key.N:
            self.builder_mode = False

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.UP:
            self.up_pressed = False
        elif _symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif _symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif _symbol == arcade.key.RIGHT:
            self.right_pressed = False

    def move_map_camera_with_keys(self):

        if self.up_pressed and not self.down_pressed:
            self.scroll_to(self.map_camera.position + Vec2(0, 20))
        elif self.down_pressed and not self.up_pressed:
            self.scroll_to(self.map_camera.position + Vec2(0, -20))
        elif self.left_pressed and not self.right_pressed:
            self.scroll_to(self.map_camera.position + Vec2(-20, 0))
        elif self.right_pressed and not self.left_pressed:
            self.scroll_to(self.map_camera.position + Vec2(20, 0))

    def on_resize(self, width: int, height: int):
        self.map_camera.resize(width, height)
        self.center_map()

    def scroll_to(self, position):
        """
        Scroll the window to the given position
        """
        self.map_camera.move_to(position, MAP_CAMERA_SPEED)

    def center_scroll_to(self, position):
        """
        This method instantly centre the map camera around the given position;
        :param position:
        :return:
        """
        self.map_camera.move_to(position - Vec2(self.window.width / 2, self.window.height / 2), 1)

    def center_map(self):
        """
        This method centre the map
        :return:
        """
        self.center_scroll_to(self.get_map_center())

    def rescale_the_map(self, new_scale):
        """
        There is an arcade function that might be useful: arcade.SpriteList().rescale()
        This function rescales all the sprites of a spriteList.
        But the problem is that the rendering is not correct.
        The map is deformed.
        So I did it  other way.
        Empty the map and recreate it with the right scaling.
        :param new_scale:
        :return:
        """
        self.map_scaling = new_scale
        self.clear()
        self.setup()
        self.convert_map_cartesian_to_isometric()
        self.center_map()

    def convert_map_cartesian_to_isometric(self):
        """"
        Convert a cartesian map to an isometric map
        """
        self.convert_layer_cartesian_to_isometric(self.grass_layer)
        self.convert_layer_cartesian_to_isometric(self.hills_layer)
        self.convert_layer_cartesian_to_isometric(self.trees_layer)
        self.convert_layer_cartesian_to_isometric(self.roads_layer)
        self.convert_layer_cartesian_to_isometric(self.buildings_layer)

    def convert_layer_cartesian_to_isometric(self, layer):
        k = 0
        for sprite in layer:
            if sprite is not None:
                cart_x, cart_y = sprite.center_x, sprite.center_y
                sprite.center_x, sprite.center_y = self.convert_cartesian_px_to_isometric_px(cart_x, cart_y, k)
                k += 1
                k = k % constantes.TILE_COUNT

    def convert_cartesian_px_to_isometric_px(self, cartesian_x, cartesian_y, offset):
        isometric_x = (cartesian_x + cartesian_y) - (constantes.TILE_WIDTH * self.map_scaling * offset / 2)
        isometric_y = (-cartesian_x + cartesian_y) / 2 + (constantes.TILE_HEIGHT * self.map_scaling * offset / 2)
        return isometric_x, isometric_y

    def check_sprite_at_screen_coordinates(self, x, y):
        """
        Cette fonction va retourner la position du sprite qui se trouve aux coordonnées x,y en px des
        """
        pass

    def get_map_center(self):
        center_tile = self.grass_layer[int(len(self.grass_layer) // 2 + constantes.TILE_COUNT // 2)]
        return Vec2(center_tile.center_x, center_tile.center_y)

    def get_logic_element_associated(self, _sprite, _sprite_list):
        index = _sprite_list.index(_sprite)
        line = int(index / constantes.TILE_COUNT)
        column = int(index % constantes.TILE_COUNT)
        if _sprite_list == self.grass_layer:
            return self.logic_map.grass_layer.array[line][column]
        elif _sprite_list == self.hills_layer:
            return self.logic_map.hills_layer.array[line][column]
        elif _sprite_list == self.trees_layer:
            return self.logic_map.trees_layer.array[line][column]
        elif _sprite_list == self.roads_layer:
            return self.logic_map.roads_layer.array[line][column]
        elif _sprite_list == self.buildings_layer:
            return self.logic_map.buildings_layer.array[line][column]

    def get_sprite_associated(self, layer, position):
        index = position(0) * 40 + position(1)
        if layer == self.logic_map.grass_layer:
            return self.grass_layer[index]
        elif layer == self.logic_map.hills_layer:
            return self.hills_layer[index]
        elif layer == self.logic_map.trees_layer:
            return self.trees_layer[index]
        elif layer == self.logic_map.roads_layer:
            return self.roads_layer[index]
        elif layer == self.logic_map.buildings_layer:
            return self.buildings_layer[index]
