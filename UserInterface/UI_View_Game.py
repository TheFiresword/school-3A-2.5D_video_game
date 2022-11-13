import arcade
from Services import servicesGlobalVariables as constantes
from UserInterface import buttons as but
import arcade.gui
import arcade.texture as art
from UserInterface import UI_Section as uis
from pyglet.math import Vec2
from CoreModules.MapManagement import mapManagementMap
from CoreModules.MapManagement.mapManagementMap import LAYER1, LAYER2, LAYER3

MAP_CAMERA_SPEED = 0.5

class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.map = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.secmanager = arcade.SectionManager(view=self)
        self.menusect = uis.MenuSect()
        self.secmanager.add_section(self.menusect)
        self.tab = arcade.load_texture(constantes.SPRITE_PATH + "Frames/map_panels_00001.png")
        self.b1 = arcade.gui.UITextureButton(x=constantes.DEFAULT_SCREEN_WIDTH-162+10, y= constantes.DEFAULT_SCREEN_HEIGHT* 4/5 ,texture= arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel13/paneling_00080.png"),
                                             texture_hovered=arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel13/paneling_00081.png"),
                                             texture_pressed=arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel13/paneling_00079.png"))
        self.manager.add(self.b1)
        # positions is an attribute that I used to easily convert coordinates
        self.grass_positions = []
        self.hills_positions = []
        self.trees_positions = []

        # a camera to travel through the map
        self.camera = arcade.Camera()
        # 4 booleans to check the key pressed
        self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed = False, False, False, False

        arcade.set_background_color(arcade.color.BLACK)
        self.manager.add(self.b1)

    def setup(self):
        self.map = mapManagementMap.Map("../Assets/maps/test_map.json")
        self.map.setup()

        layer_grass = self.map.get_sprite_list(LAYER1)
        layer_hills = self.map.get_sprite_list(LAYER2)
        layer_trees = self.map.get_sprite_list(LAYER3)

        self.setup_list_positions(layer_grass, self.grass_positions)
        self.setup_list_positions(layer_hills, self.hills_positions)
        self.setup_list_positions(layer_trees, self.trees_positions)

        # self.convert_map_cartesian_to_isometric()

        # set up the camera and centre it
        self.center_map()

    def setup_list_positions(self, layer, layer_positions):
        width = (self.map.get_sprite_list(LAYER1))[0].width
        height = (self.map.get_sprite_list(LAYER1))[0].height
        for sprite in layer:
            j = int(sprite.center_x / width)
            i = int(sprite.center_y / height)
            layer_positions.append((i, j))


    def on_show_view(self):
        self.setup()
        self.secmanager.enable()



    def on_draw(self):
        self.clear()
        self.camera.use()
        self.map.draw()

        arcade.draw_text("Game Screen - click to advance", constantes.DEFAULT_SCREEN_WIDTH / 2, constantes.DEFAULT_SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH - 81,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - 275 -25,
                                      width=162, height=constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                      texture=self.tab)
        self.manager.draw()

    def on_update(self, delta_time: float):
        self.map.update()
        self.move_map_camera_with_keys()


    def on_hide(self):
        self.manager.disable()
        self.secmanager.disable()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print(x,y)


    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """
        A mouse scroll generates a rescaling of the map if it's possible
        """

        if scroll_y < 0:
            next_scaling = self.map.map_scaling * 0.9
            if constantes.SCALE_MIN < self.map.map_scaling and constantes.SCALE_MIN < \
                    next_scaling:
                self.rescale_the_map(next_scaling)

            else:
                self.rescale_the_map(constantes.SCALE_MIN)
        else:
            next_scaling = self.map.map_scaling * 1.1
            if self.map.map_scaling < constantes.SCALE_MAX and constantes.SCALE_MAX > \
                    next_scaling:
                self.rescale_the_map(next_scaling)

            else:
                self.rescale_the_map(constantes.SCALE_MAX)

    def on_key_press(self, symbol: int, modifiers: int):

        if symbol == arcade.key.UP:
            self.up_pressed = True
        elif symbol == arcade.key.DOWN:
            self.down_pressed = True
        elif symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True

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
            self.scroll_to(self.camera.position + Vec2(0, 20))
        elif self.down_pressed and not self.up_pressed:
            self.scroll_to(self.camera.position + Vec2(0, -20))
        elif self.left_pressed and not self.right_pressed:
            self.scroll_to(self.camera.position + Vec2(-20, 0))
        elif self.right_pressed and not self.left_pressed:
            self.scroll_to(self.camera.position + Vec2(20, 0))

    def on_resize(self, width: int, height: int):
        self.camera.resize(width, height)
        self.center_map()

    def scroll_to(self, position):
        """
        Scroll the window to the given position
        """
        self.camera.move_to(position, MAP_CAMERA_SPEED)

    def center_scroll_to(self, position):
        """
        This method instantly centre the map camera around the given position;
        :param position:
        :return:
        """
        self.camera.move_to(position - Vec2(self.window.width / 2, self.window.height / 2), 1)

    def center_map(self):
        """
        This method centre the map
        :return:
        """
        self.center_scroll_to(self.map.get_map_center())

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
        self.map.map_scaling = new_scale
        self.map.clear()
        self.map.setup()
        self.convert_map_cartesian_to_isometric()
        self.center_map()

    def convert_map_cartesian_to_isometric(self):
        """"
        Convert a cartesian map to an isometric map
        """
        # for layer in self.map.sprite_lists:
        grass_layer = self.map.get_sprite_list(LAYER1)
        hills_layer = self.map.get_sprite_list(LAYER2)
        trees_layer = self.map.get_sprite_list(LAYER3)

        self.convert_layer_cartesian_to_isometric(grass_layer, self.grass_positions)
        self.convert_layer_cartesian_to_isometric(hills_layer, self.hills_positions)
        self.convert_layer_cartesian_to_isometric(trees_layer, self.trees_positions)

    def convert_layer_cartesian_to_isometric(self, layer, positions_list):
        width = (self.map.get_sprite_list(LAYER1))[0].width
        height = (self.map.get_sprite_list(LAYER1))[0].height
        k = 0
        for sprite in layer:
            if sprite is not None:
                cart_x, cart_y = sprite.center_x, sprite.center_y
                (i, j) = positions_list[k]
                sprite.center_x = (cart_x + cart_y) - (width * j / 2)
                sprite.center_y = (-cart_x + cart_y) / 2 + (height * j / 2)
                k += 1
