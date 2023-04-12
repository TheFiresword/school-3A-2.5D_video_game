import time

import pyglet

from uuid import uuid4

from CoreModules.WalkersManagement.walkersManagementWalker import Immigrant

from UserInterface import UI_buttons
from UserInterface import UI_HUD_Build as hudb
from UserInterface import UI_Visual_Map as uivm
from UserInterface import UI_Text_Display as text
from UserInterface import UI_PoP_Up as pop

import CoreModules.GameManagement.Game as game
import CoreModules.MapManagement.mapManagementMap as map
from CoreModules.GameManagement import Update as updates

from Services import servicesGlobalVariables as constantes
from Services import Service_Game_Data as gdata
from Services import Service_Static_functions as fct
from Services import Service_Save_and_Load as saveload

import arcade
import arcade.gui

from pyglet.math import Vec2

MAP_CAMERA_SPEED = 0.5

MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color(arcade.color.BLACK)
MINIMAP_WIDTH = 147
MINIMAP_HEIGHT = 110
MAP_WIDTH = 2048
MAP_HEIGHT = 2048


class GameView(arcade.View):

    def __init__(self, _game, name="save_1"):
        super().__init__()
        self.tmp_statistics_sect = None
        self.last_click_time = None
        self.food_qty_text = None
        self.name = name
        self.game = None
        if _game:
            self.game = _game

        # =======================================
        # the game status (played or not)
        # =======================================
        self.is_paused = False
        self.count_pauses = 0
        self.p_key_pressed = False
        # speed in percentage
        self.speed_ratio = 100

        # =======================================
        # Intels about the current player action
        # =======================================
        self.mouse_pos = (0, 0)
        self.real_mouse_pos = (0, 0)
        self.init_mouse_pos = (0, 0)
        self.actual_sprite_limit = (0, 0, 0, 0)
        self.surface_drag = []
        self.mouse_left_pressed, self.mouse_right_pressed = False, False
        self.mouse_left_maintained, self.mouse_right_maintained = False, False
        self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed = False, False, False, False

        self.builder_mode = False
        self.builder_content = ""
        self.remove_mode = None
        # =======================================
        # Arcade stuff
        # =======================================
        arcade.set_background_color(arcade.color.BLACK)
        self.right_panel_manager = arcade.gui.UIManager()
        self.right_panel_manager.enable()
        self.right_panel_manager_depth_one = {"water": arcade.gui.UIManager(),
                                              "health": arcade.gui.UIManager(),
                                              "religion": arcade.gui.UIManager(),
                                              "education": arcade.gui.UIManager(),
                                              "entertainment": arcade.gui.UIManager(),
                                              "roll": arcade.gui.UIManager(),
                                              "hammer": arcade.gui.UIManager(),
                                              "sword": arcade.gui.UIManager(),
                                              "carry": arcade.gui.UIManager()
                                              }
        self.right_panel_manager_depth_two = {
                                              "academy":None,
                                              "actor colony":None,
                                              "architects guild":None,
                                              "aqueduct":None,
                                              "arena":None,
                                              "ares temple":None,
                                              "neptune temple":None,
                                              "mercury temple":None,
                                              "mars temple":None,
                                              "venus temple":None,
                                              "amphitheater":None,
                                              "barber":None,
                                              "baths":None,
                                              "barracks":None,
                                              "clay pit":None,
                                              "colosseum":None,
                                              "dock":None,
                                              "doctor":None,
                                              "dwell":None,
                                              "engineer's post":None,
                                              "forum":None,
                                              "fruit farm":None,
                                              "furniture workshop":None,
                                              "fort":None,
                                              "fountain":None,
                                              "garden":None,
                                              "gatehouse":None,
                                              "gladiator school":None,
                                              "governor housing house":None,
                                              "governor housing villa":None,
                                              "governor housing palace":None,
                                              "granary":None,
                                              "hospital":None,
                                              "iron mine":None,
                                              "library":None,
                                              "lion house":None,
                                              "low bridge":None,
                                              "lararium":None,
                                              "lighthouse":None,
                                              "marble quarry":None,
                                              "market":None,
                                              "oil workshop":None,
                                              "military academi":None,
                                              "olive farm":None,
                                              "palisade":None,
                                              "plaza":None,
                                              "pig farm": None,
                                              "prefecture": None,
                                              "pottery workshop": None,
                                              "reservoir": None,
                                              "senate": None,
                                              "school": None,
                                              "ship bridge": None,
                                              "tavern": None,
                                              "theater": None,
                                              "tower": None,
                                              "timber yard": None,
                                              "vegetable farm": None,
                                              "vine farm": None,
                                              "watchtower": None,
                                              "weapons workshop": None,
                                              "wheat farm": None,
                                              "wine workshop": None,
                                              "warehouse": None,
                                              "work camp": None,
                                              "wall": None,
                                              "well": None
                                             }
        self.manager_state = {"water":False,
                                              "health":False,
                                              "religion":False,
                                              "education":False,
                                              "entertainment":False,
                                              "roll":False,
                                              "hammer":False,
                                              "sword":False,
                                              "carry":False,
}
        self.map_camera = arcade.Camera()
        self.menu_camera = arcade.Camera()
        self.minimap_camera = arcade.Camera()
        # =======================================
        # Visuals elements excepts ones Map related
        # =======================================
        self.tab = arcade.load_texture(constantes.SPRITE_PATH + "PanelsOther/paneling_00017.png")
        self.bar = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel0.png")
        self.money_box = arcade.load_texture(constantes.SPRITE_PATH + "PanelsOther/paneling_00015.png")
        # Creation of objects from PoP_Up class
        # Fire PoP_Up
        self.fire_show = 0
        self.fire_Pop_up = pop.create_PoP_Up(image=constantes.SPRITE_PATH + "Pictures/feu2.png",
                                             title="Fire in the city",
                                             normal_text="tchoupi",
                                             carved_text="Nov 340 BC              To The new governor\n"
                                                         "Inadequate prevention measures have\n"
                                                         "allowed fires to start. Even now, flames are\n"
                                                         "sweeping through parts of the city.",
                                             top_left_corner=(
                                                 0, constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1]),
                                             order=["title_zone", "image_zone", "carved_text_zone", "button_zone"])
        self.collapse_show = 0
        # Collapse PoP_Up
        self.collapse_Pop_up = pop.create_PoP_Up(image=constantes.SPRITE_PATH + "Pictures/effondrement.png",
                                                 title="Building Collapse",
                                                 normal_text="tchoupi",
                                                 carved_text="Nov 340 BC              To The new governor\n"
                                                             "A building has just collapsed.\n"
                                                             "The maintenance provided\n"
                                                             "by the engineers being insufficient,\n"
                                                             "the building has become unstable and \n"
                                                             "has collapsed under its own weight.",
                                                 top_left_corner=(
                                                     0, constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1]),

                                                 order=["title_zone", "image_zone", "carved_text_zone", "button_zone"])
        # City debt PoP_Up
        self.money_already_showed = False
        self.city_debt_Pop_up = pop.create_PoP_Up(image=constantes.SPRITE_PATH + "Pictures/caesar.png",
                                                  title="City debt",
                                                  normal_text="tchoupi",
                                                  carved_text="Nov 340 BC              To The new governor\n"
                                                              "your city's coffers are empty,\n"
                                                              "Caesar has decided to grant you more funds,\n"
                                                              "but he will not be so generous next time.\n"
                                                              "Develop export to raise funds",
                                                  top_left_corner=(
                                                      0, constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1]),
                                                  order=["title_zone", "image_zone", "carved_text_zone", "button_zone"])
        self.automatic_pop_up = self.fire_Pop_up
        self.actual_pop_up = self.fire_Pop_up
        self.money_text = None
        self.fps_text = None
        buttons_render = UI_buttons.buttons
        self.buttons = [arcade.gui.UITextureButton(x=b0, y=(
                3 * constantes.DEFAULT_SCREEN_HEIGHT / 4 - self.bar.image.size[1] / 2 + b1), texture=b2,
                                                   texture_hovered=b3, texture_pressed=b4,
                                                   width=b2.image.size[0] * constantes.SPRITE_SCALING, height=(
                                                                                                                      b2.image.size[
                                                                                                                          1] * constantes.DEFAULT_SCREEN_HEIGHT / 2) / 900)
                        for (b0, b1, b2, b3, b4) in buttons_render]
        self.buttons[5].on_click = self.button_click_house
        self.buttons[6].on_click = self.button_click_shovel
        self.buttons[7].on_click = self.button_click_road
        self.select_all_manager()
        self.attribute_on_click()

        self.minimap_sprite_list = None
        self.minimap_texture = None
        self.minimap_sprite = None

        self.bar_manager = arcade.gui.UIManager()
        self.load_button = UI_buttons.Text_Button_background(x=40,
                                                             y=constantes.DEFAULT_SCREEN_HEIGHT - 3 * self.bar.height / 4,
                                                             width=20, height=self.bar.height, texture=None,
                                                             my_text="Load Game", color="black")
        self.load_button.on_click = self.button_load_on_click
        self.layer_button = UI_buttons.Text_Button_background(x=constantes.DEFAULT_SCREEN_WIDTH - 162 + 3, y=(
                                                                                                                     3 * constantes.DEFAULT_SCREEN_HEIGHT / 4 -
                                                                                                                     self.bar.image.size[
                                                                                                                         1] / 2) + constantes.DEFAULT_SCREEN_HEIGHT / 2 * 0.4444444444,
                                                              width=120, height=25, texture=UI_buttons.texture_panel11,
                                                              my_text="Overlays", color="black")
        self.layer_button.on_click = self.button_layer_on_click
        self.layer_manager = arcade.gui.UIManager()
        self.layer_manager_show = False

        self.normal_layer_button = UI_buttons.Text_Button_background(x=constantes.DEFAULT_SCREEN_WIDTH - 282,
                                                                     y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.height - 1,
                                                                     width=120, height=25,
                                                                     texture=UI_buttons.texture_panel11,
                                                                     my_text="Normal", color="black")
        self.layer_manager.add(self.normal_layer_button)
        self.normal_layer_button.on_click = self.button_normal_layer_on_click
        self.fire_layer_button = UI_buttons.Text_Button_background(x=constantes.DEFAULT_SCREEN_WIDTH - 282,
                                                                   y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.height - 26,
                                                                   width=120, height=25,
                                                                   texture=UI_buttons.texture_panel11, my_text="Fire",
                                                                   color="black")
        self.layer_manager.add(self.fire_layer_button)
        self.fire_layer_button.on_click = self.button_fire_layer_on_click
        self.collapse_layer_button = UI_buttons.Text_Button_background(x=constantes.DEFAULT_SCREEN_WIDTH - 282,
                                                                       y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.height - 51,
                                                                       width=120, height=25,
                                                                       texture=UI_buttons.texture_panel11,
                                                                       my_text="Collapse", color="black")
        self.layer_manager.add(self.collapse_layer_button)
        self.collapse_layer_button.on_click = self.button_collapse_layer_on_click
        self.owner_layer_button = UI_buttons.Text_Button_background(x=constantes.DEFAULT_SCREEN_WIDTH - 282,
                                                                       y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.height - 75,
                                                                       width=120, height=25,
                                                                       texture=UI_buttons.texture_panel11,
                                                                       my_text="owner", color="black")

        self.owner_layer_button.on_click = self.button_owner_layer_on_click
        self.layer_manager.add(self.owner_layer_button)
        self.collapse_layer_button.on_click = self.button_collapse_layer_on_click
        self.bar_manager.add(self.load_button)
        self.bar_manager.enable()

        self.fps_up = arcade.gui.UITextureButton(x=constantes.DEFAULT_SCREEN_WIDTH - 162 + 10,
                                                 y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[
                                                     1] - constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                                 texture=arcade.load_texture(
                                                     constantes.SPRITE_PATH + "Panel/Panel42/paneling_00249.png"),
                                                 width=25, height=15)
        self.fps_down = arcade.gui.UITextureButton(x=constantes.DEFAULT_SCREEN_WIDTH - 162 + 35,
                                                   y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[
                                                       1] - constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                                   texture=arcade.load_texture(
                                                       constantes.SPRITE_PATH + "Panel/Panel43/paneling_00253.png"),
                                                   width=25, height=15)

        self.fps_up.on_click = self.button_fps_up_on_click
        self.fps_down.on_click = self.button_fps_down_on_click
        for k in self.buttons:
            self.right_panel_manager.add(k)
        self.right_panel_manager.add(self.fps_up)
        self.right_panel_manager.add(self.fps_down)
        self.right_panel_manager.add(self.layer_button)

        # =======================================
        # Map related Visuals elements
        # =======================================
        self.visualmap = uivm.VisualMap()
        self.dragged_sprite = arcade.SpriteList()

        # =======================================
        # Preliminary actions
        # =======================================
        self.setup()

    def setup(self):
        if not self.game:
            # Set up the owner id
            ip = fct.get_ip()
            port = fct.get_free_port(ip)
            self.game = game.Game(map.MapLogic((constantes.TILE_COUNT // 2, 0), (0, constantes.TILE_COUNT // 2),
                                               constantes.TILE_COUNT - 7), name=self.name, owner_id=(ip, port), is_online=False)
        else:
            self.name = self.game.name
        self.money_text = text.Sprite_sentence("Dn: " + str(self.game.money), "white",
                                               (205, constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4))
        self.fps_text = text.Sprite_sentence(str(self.speed_ratio) + "%", "black", (
            constantes.DEFAULT_SCREEN_WIDTH - 162 + 85,
            constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] - constantes.DEFAULT_SCREEN_HEIGHT / 2 + 10))
        self.population_text = text.Sprite_sentence("Pop :" + str(constantes.WALKER_UNIT * len(self.game.walkersAll)),
                                                    "white", (
                                                        505,
                                                        constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4))
        self.fps_text2 = text.Sprite_sentence("Pop :" + str(self.game.framerate), "white", (
            605 - (len(self.population_text.sentence)), constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4))

        self.food_qty_text = text.Sprite_sentence(f"Your town has {self.game.update_food_qty()} lots of food", "black",
                                                  (constantes.DEFAULT_SCREEN_WIDTH - len(self.fps_text2.sentence),
                                                   constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4))

        self.visualmap.setup(self.game)
        self.center_map()
        self.minimap_camera.move_to(
            self.visualmap.get_map_center() - Vec2(self.window.width / 2, self.window.height / 2), 1)
        self.visualmap.buildings_layer.visible = True
        self.visualmap.fire_risk_layer_show = False
        self.visualmap.collapse_risk_layer_show = False
        self.visualmap.destroyed_layer_show = True
        self.visualmap.fire_layer_show = True
        self.builder_content = ""

        # Construct the minimap
        size = (MINIMAP_WIDTH, MINIMAP_HEIGHT)
        self.minimap_texture = arcade.Texture.create_empty(str(uuid4()), size)
        self.minimap_sprite = arcade.Sprite(center_x=(constantes.DEFAULT_SCREEN_WIDTH - MINIMAP_WIDTH / 2 - 9),
                                            center_y=(3 * constantes.DEFAULT_SCREEN_HEIGHT / 4 - self.bar.image.size[
                                                1] / 2 + 0.3044444444 * constantes.DEFAULT_SCREEN_HEIGHT / 2),
                                            texture=self.minimap_texture)
        self.minimap_sprite_list = arcade.SpriteList()
        self.minimap_sprite_list.append(self.minimap_sprite)

    def update_minimap(self):
        map_width = constantes.MAP_WIDTH * self.visualmap.map_scaling
        map_height = constantes.MAP_HEIGHT * self.visualmap.map_scaling
        proj = self.minimap_camera.position[0] - (15 * map_width / 100), self.minimap_camera.position[0] + (
                85 * map_width / 100), \
               self.minimap_camera.position[1] - (15 * map_height / 100), self.minimap_camera.position[1] + (
                       85 * map_height / 100)

        with self.minimap_sprite_list.atlas.render_into(self.minimap_texture, projection=proj) as fbo:
            fbo.clear(MINIMAP_BACKGROUND_COLOR)
            self.visualmap.grass_layer.draw()
            self.visualmap.roads_layer.draw()
            self.visualmap.trees_layer.draw()
            self.visualmap.buildings_layer.draw()
            self.visualmap.hills_layer.draw()

    # =======================================
    #  View Related Fuctions
    # =======================================
    def on_show_view(self):
        pass

    def on_hide(self):
        self.bar_manager.disable()
        self.hide_all_manager()
        self.right_panel_manager.disable()

    def on_draw(self):

        self.clear()
        # =======================================
        # Display Map related content
        # =======================================
        self.map_camera.use()  # select camera linked to map
        if self.game.map.active:  # if map displayed
            self.visualmap.draw_layers(self.game)
            self.visualmap.walker_to_render.draw()
            # Test click on map
            if self.visualmap.red_sprite.visible:
                # self.visualmap.red_sprite.draw_hit_box(color=(255, 0, 0), line_thickness=1)
                self.visualmap.red_sprite.alpha = 80
                self.visualmap.red_sprite.color = (255, 0, 0)
                self.visualmap.red_sprite.draw()

            if self.builder_mode:
                if not self.mouse_left_maintained:
                    if self.builder_content != "road":
                        hollow = hudb.hollow_build(self.mouse_pos[0], self.mouse_pos[1], self.visualmap,
                                                   gdata.building_dico[self.builder_content.lower()])
                    else:
                        hollow = hudb.hollow_build(self.mouse_pos[0], self.mouse_pos[1], self.visualmap)
                    hollow.draw()
                else:
                    self.dragged_sprite.draw()

            if self.remove_mode:
                if self.real_mouse_pos[0] < constantes.DEFAULT_SCREEN_WIDTH - 165:
                    arcade.get_window().set_mouse_visible(False)
                    hollow = hudb.hollow(self.mouse_pos[0], self.mouse_pos[1], self.visualmap)
                    hollow.draw()
                    self.dragged_sprite.draw()
                else:
                    fct.draw_normal_cursor()
        # =======================================
        # Display Menu related content
        # =======================================
        self.menu_camera.use()
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH / 2,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4,
                                      width=self.bar.image.size[0] / 2, height=self.bar.image.size[1] / 2,
                                      texture=self.bar)
        arcade.draw_texture_rectangle(center_x=300,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4,
                                      width=(len(self.money_text.sentence) + 5) * constantes.FONT_WIDTH / 2,
                                      height=self.bar.image.size[1] / 2,
                                      texture=self.money_box)
        arcade.draw_texture_rectangle(center_x=500,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4,
                                      width=(len(self.money_text.sentence) + 5) * constantes.FONT_WIDTH / 2,
                                      height=self.bar.image.size[1] / 2,
                                      texture=self.money_box)
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH - 81,
                                      center_y=3 * constantes.DEFAULT_SCREEN_HEIGHT / 4 - self.bar.image.size[1] / 2,
                                      width=162, height=constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                      texture=self.tab
                                      )
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH - 81,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[
                                          1] - constantes.DEFAULT_SCREEN_HEIGHT / 2 - 23 - 50, width=162, height=200,
                                      texture=arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel46.png"))
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH - 81,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[
                                          1] - constantes.DEFAULT_SCREEN_HEIGHT / 2 - 23 - 50 - 200, width=162,
                                      height=200, texture=arcade.load_texture(
                constantes.SPRITE_PATH + "Map_panels/map_panels_00002.png"))
        self.money_text.draw_()
        self.fps_text.draw_()
        self.population_text.draw_()
        self.right_panel_manager.draw()
        self.fps_text2.draw_()
        self.food_qty_text.draw_()
        self.right_panel_manager.children[0][-1].draw_()
        self.bar_manager.draw()
        self.load_button.draw_()
        for manager in self.manager_state.items():
            if manager[1]:
                if manager[0] in self.right_panel_manager_depth_one:
                    real_man = self.right_panel_manager_depth_one[manager[0]]
                    real_man.draw()
                    for k in real_man.children[0]:
                        k.draw_()
                elif manager[0] in self.right_panel_manager_depth_one.keys():
                    real_man = self.right_panel_manager_depth_two[manager[0]]
                    real_man.draw()
                else:
                    print("no manager")
        if self.layer_manager_show:
            self.layer_manager.draw()
            for but in self.layer_manager.children[0]:
                but.draw_()
        # if self.fire_show == 1 and not self.fire_Pop_up.already_closed_once:
        #     self.fire_Pop_up.draw_()
        #     self.is_paused = True
        #     self.count_pauses += 1
        # if self.collapse_show == 1 and not self.collapse_Pop_up.already_closed_once:
        #     self.collapse_Pop_up.draw_()
        #     self.is_paused = True
        #     self.count_pauses += 1
        # if self.game.money <= 10 and not self.city_debt_Pop_up.already_closed_once:
        #     self.city_debt_Pop_up.draw_()
        #     self.is_paused = True
        #     self.count_pauses += 1
        # if self.actual_pop_up and self.actual_pop_up.visible:
        #     self.actual_pop_up.draw_()

        # Testing something cool -- error message when building farm on non yellow grass
        self.draw_message_for_farm_building()

        # Update the minimap
        self.minimap_camera.use()
        self.update_minimap()

        # Draw the minimap
        self.minimap_sprite_list.draw()

        # Statistics
        if self.tmp_statistics_sect:
            self.tmp_statistics_sect.on_draw()

    def on_update(self, delta_time: float):
        if self.is_paused:
            arcade.get_window().set_update_rate(0)
        else:
            arcade.get_window().set_update_rate(1 / self.game.framerate)
            self.p_key_pressed = False

            tmp = self.game.updategame(self.visualmap.map_scaling)
            layer_to_update_from_packet = []
            if  isinstance(tmp, tuple):
                update,layer_to_update_from_packet = tmp
            else:
                update = tmp

            for layer in layer_to_update_from_packet:
                if layer == "buildings":
                    self.visualmap.update_layers(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
                elif layer == "roads":
                    self.visualmap.update_layers(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            if len(update.catchedfire) > 0:
                self.fire_show += 1
            if len(update.collapsed) > 0:
                self.collapse_show += 1
            self.update_treatment(update)
            self.visualmap.fire_count += 1
            for sprite in self.visualmap.fire_layer:
                sprite.set_texture(self.visualmap.fire_count % len(sprite.textures))

            self.move_map_camera_with_keys()
            self.visualmap.update_walker_list(self.game.walkersOut)
            self.money_text = text.Sprite_sentence("Dn: " + str(self.game.money), "white", (
                320 - (len(self.money_text.sentence) + 5) * constantes.FONT_WIDTH / 4,
                constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4))
            self.fps_text = text.Sprite_sentence(str(self.speed_ratio) + "%", "black", (
                constantes.DEFAULT_SCREEN_WIDTH - 162 + 85,
                constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] - constantes.DEFAULT_SCREEN_HEIGHT / 2 + 10))
            self.population_text = text.Sprite_sentence(
                "Pop :" + str(constantes.WALKER_UNIT * len(self.game.walkersAll)), "white", (
                    505 - (len(self.population_text.sentence)),
                    constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4))
            self.fps_text2 = text.Sprite_sentence("Fps:" + str(1 / delta_time), "white", (
                605 - (len(self.population_text.sentence)),
                constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4))
            self.food_qty_text = text.Sprite_sentence(f"Your town has {self.game.update_food_qty()} lots of food",
                                                      "black",
                                                      (800,
                                                       constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1] / 4))

    # =======================================
    #  Mouse Related Fuctions
    # =======================================

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # ===================================
        # Left click Draw red rectangle around closest sprite to mouse
        # ===================================
        (map_pos_x, map_pos_y) = Vec2(x, y) + self.map_camera.position
        self.init_mouse_pos = (map_pos_x, map_pos_y)
        if x < constantes.DEFAULT_SCREEN_WIDTH - 165:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.visualmap.red_sprite = arcade.Sprite(constantes.SPRITE_PATH + "Land/LandOverlay/Land2a_00037.png",
                                                          scale=self.visualmap.map_scaling, center_x=map_pos_x,
                                                          center_y=map_pos_y, hit_box_algorithm="Detailed")
                self.visualmap.red_sprite.visible = True
                if not self.builder_mode and not self.remove_mode and not self.builder_content == "road":
                    (nearest_sprite, d) = arcade.get_closest_sprite(self.visualmap.red_sprite,
                                                                    self.visualmap.buildings_layer)
                    if not nearest_sprite.textures:
                        (nearest_sprite, d) = arcade.get_closest_sprite(self.visualmap.red_sprite,
                                                                        self.visualmap.roads_layer)
                        if not nearest_sprite.textures:
                            (nearest_sprite, d) = arcade.get_closest_sprite(self.visualmap.red_sprite,
                                                                            self.visualmap.trees_layer)
                            if not nearest_sprite.textures:
                                (nearest_sprite, d) = arcade.get_closest_sprite(self.visualmap.red_sprite,
                                                                                self.visualmap.hills_layer)
                                if not nearest_sprite.textures:
                                    (nearest_sprite, d) = arcade.get_closest_sprite(self.visualmap.red_sprite,
                                                                                    self.visualmap.grass_layer)
                    else:
                        (i, j) = self.visualmap.get_sprite_at_screen_coordinates(nearest_sprite.position)
                        bat = self.game.map.buildings_layer.get_cell(i, j)
                        print(bat.dic["version"])
                        k, p = 0, 0
                        #self.actual_pop_up = pop.info_building_pop_up(bat.dic["version"],
                        #                                              bat.current_number_of_employees,
                        #                                              bat.max_number_of_employees)
                        #if self.actual_pop_up:
                        #    self.actual_pop_up.visible = True
                        #    self.is_paused = True
                        #   self.count_pauses += 1
                    # self.visualmap.red_sprite.texture = nearest_sprite.texture
                else:
                    (nearest_sprite, d) = arcade.get_closest_sprite(self.visualmap.red_sprite,
                                                                    self.visualmap.grass_layer)
                self.visualmap.red_sprite.center_x, self.visualmap.red_sprite.center_y = nearest_sprite.center_x, nearest_sprite.center_y
                self.visualmap.red_sprite.texture = nearest_sprite.texture
                self.mouse_left_pressed = True
            # For testing
            if button == arcade.MOUSE_BUTTON_RIGHT:
                # A right clic cancel whatever mode (remove or build) is activated
                current_time = time.monotonic()
                if self.last_click_time is not None and current_time - self.last_click_time < 0.55:
                    # Double click detected
                    line, column = self.visualmap.get_sprite_at_screen_coordinates((map_pos_x, map_pos_y))
                    self.game.attack((line, column))
                else:
                    self.last_click_time = current_time
                    self.mouse_right_pressed = True
                    self.builder_mode = False
                    self.remove_mode = False
                    self.visualmap.red_sprite.visible = False

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if x < constantes.DEFAULT_SCREEN_WIDTH - 165:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if self.remove_mode:
                    if self.mouse_left_maintained:
                        self.remove_elements_serie(self.init_mouse_pos, (Vec2(x, y) + self.map_camera.position))
                        self.dragged_sprite.clear()
                    else:
                        self.remove_sprite(self.mouse_pos)
                else:
                    # If the remove_mode is not set the normal cursor is drawn
                    fct.draw_normal_cursor()
                if self.builder_mode:
                    if self.mouse_left_maintained:
                        if self.builder_content == "dwell":
                            self.add_multiple_one_sized_building()
                            self.dragged_sprite.clear()
                        elif self.builder_content == "road":
                            tmp_end_pos = Vec2(x, y) + self.map_camera.position
                            self.add_roads_serie(self.init_mouse_pos, tmp_end_pos)
                    else:
                        if self.builder_content == "road":
                            self.add_road(self.mouse_pos)
                        else:
                            self.add_one_sized_building(self.mouse_pos)
                self.mouse_left_pressed = False
                self.mouse_left_maintained = False

            if button == arcade.MOUSE_BUTTON_RIGHT:
                self.hide_all_manager()
                self.mouse_right_pressed = False
                self.mouse_right_maintained = False
                # self.red_sprite.visible = False
                # If the remove_mode is not set the normal cursor is drawn
                fct.draw_normal_cursor()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.real_mouse_pos = (x, y)
        self.mouse_pos = Vec2(x, y) + self.map_camera.position
        tmp_end_pos = Vec2(x, y) + self.map_camera.position
        if self.mouse_left_pressed:
            if self.builder_mode:
                if self.builder_content == "road":
                    if self.mouse_left_maintained:
                        self.add_roads_serie(self.init_mouse_pos, tmp_end_pos, True)
                else:
                    self.get_surface_dragged(self.init_mouse_pos, tmp_end_pos)
                    self.dragged_sprite.clear()
                    self.visualmap.fill_temporary_build(self.surface_drag, self.dragged_sprite, self.builder_content,
                                                        "build")
            if self.remove_mode:
                self.get_surface_dragged(self.init_mouse_pos, tmp_end_pos)
                self.dragged_sprite.clear()
                self.visualmap.fill_temporary_build(self.surface_drag, self.dragged_sprite, self.builder_content,
                                                    "remove")

            self.mouse_left_maintained = True
        # self.red_sprite.visible = False

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """
        A mouse scroll generates a rescaling of the map if it's possible
        """
        if scroll_y < 0:
            next_scaling = self.visualmap.map_scaling * 0.9
            if constantes.SCALE_MIN < self.visualmap.map_scaling and constantes.SCALE_MIN < \
                    next_scaling:
                self.clear()
                self.visualmap.rescale_the_map(next_scaling, self.game)
                self.center_map()
            else:
                self.clear()
                self.visualmap.rescale_the_map(constantes.SCALE_MIN, self.game)
                self.center_map()
        else:
            next_scaling = self.visualmap.map_scaling * 1.1
            if self.visualmap.map_scaling < constantes.SCALE_MAX and constantes.SCALE_MAX > \
                    next_scaling:
                self.clear()
                self.visualmap.rescale_the_map(next_scaling, self.game)
                self.center_map()
            else:
                self.clear()
                self.visualmap.rescale_the_map(constantes.SCALE_MAX, self.game)
                self.center_map()

    # =======================================
    #  Key Related Fuctions
    # =======================================

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
            self.actual_pop_up.visible = True

        # Testing
        # press S to save your game
        elif symbol == arcade.key.S:
            self.save_game(self.name)
        # press L to load game1
        elif symbol == arcade.key.L:
            window = arcade.get_window()
            window.show_view(window.loadscreen)
            window.loadscreen.fromview = "game"
        # press D to delete game1
        elif symbol == arcade.key.D:
            self.delete_game('self.name')

        # press P to pause the game
        elif symbol == arcade.key.P:
            self.p_key_pressed = True
            if self.count_pauses % 2 == 0:
                self.is_paused = True
            else:
                self.is_paused = False
            self.count_pauses += 1

        elif symbol == arcade.key.TAB:
            # Print statistics of players
            rows = []
            p = self.game.players

            offset_y = 100
            stats =self.game.generateStat()
            for i in range(len(p)):
                rows.append(arcade.Text(text=f'{p[i][0][0]}:{p[i][0][1]} ====> {stats[f"{p[i][0][0]}:{p[i][0][1]}"]}', start_x=10,
                                        start_y=30 * i + offset_y, color=p[i][1], font_size=15))
            rows.append(arcade.Text(text=f'| ====Players==== | ====Statistics==== |', start_x=10,
                                    start_y=30 * (i+1) + offset_y, color=(255, 255, 255), font_size=20))

            self.tmp_statistics_sect = arcade.Section(left=0, bottom=constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                                      width=300, height=300, name="Statistics",
                                                      accept_keyboard_events=False)

            self.tmp_statistics_sect.on_draw = lambda: [row.draw() for row in rows]

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.UP:
            self.up_pressed = False
        elif _symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif _symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif _symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif _symbol == arcade.key.TAB:
            # destroy the view statistics
            self.tmp_statistics_sect = None

    # =======================================
    #  Camera Related Fuctions
    # =======================================

    def move_map_camera_with_keys(self):
        map_width = constantes.MAP_WIDTH * self.visualmap.map_scaling * 2
        map_height = constantes.MAP_HEIGHT * self.visualmap.map_scaling
        if self.up_pressed and not self.down_pressed:
            self.scroll_to(self.map_camera.position + Vec2(0, 20))
        elif self.down_pressed and not self.up_pressed:
            self.scroll_to(self.map_camera.position + Vec2(0, -20))
        elif self.left_pressed and not self.right_pressed:
            self.scroll_to(self.map_camera.position + Vec2(-20, 0))
        elif self.right_pressed and not self.left_pressed:
            self.scroll_to(self.map_camera.position + Vec2(20, 0))

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
        self.center_scroll_to(self.visualmap.get_map_center())

    def on_resize(self, width: int, height: int):  # Never used game always fullscreen
        self.map_camera.resize(width, height)
        self.center_map()

    # =======================================
    #  Gameplay Related Fuctions
    # =======================================

    def add_road(self, pos) -> bool:
        """
        Fonction d'ajout de route
        va probablement être transformée en fonction plus générale d'ajout d'élément
        """
        line, column = self.visualmap.get_sprite_at_screen_coordinates(pos)

        if self.game.add_road(line, column):
            # si la route a été bien ajoutée on update la spritelist en la recréant
            self.visualmap.update_layers(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            return True
        return False

    def add_roads_serie(self, start_pos, end_pos, dynamically=False) -> bool:
        """
        Fonction qui permet d'ajouter une série de routes
        Prend en paramètre 2 positions de souris sous forme de tuple
        """
        line1, column1 = self.visualmap.get_sprite_at_screen_coordinates(start_pos)
        line2, column2 = self.visualmap.get_sprite_at_screen_coordinates(end_pos)

        if self.game.add_roads_serie((line1, column1), (line2, column2), dynamically):
            self.visualmap.update_layers(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            return True
        return False

    def add_one_sized_building(self, pos):
        # ================================
        #       Add single tile Building
        # ================================
        line, column = self.visualmap.get_sprite_at_screen_coordinates(pos)
        building = gdata.building_dico[self.builder_content].name
        if self.game.add_building(line, column, building):
            self.visualmap.update_layers(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
            return True
        return False

    def add_multiple_one_sized_building(self):
        for (line, column) in self.surface_drag:
            if self.game.add_building(line, column, self.builder_content):
                pass
            else:
                print("Building failed")
        self.visualmap.update_layers(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)

    def remove_sprite(self, pos) -> bool:
        line, column = self.visualmap.get_sprite_at_screen_coordinates(pos)
        what_is_removed = self.game.remove_element((line, column))
        if what_is_removed == constantes.LAYER4:
            self.visualmap.update_layers(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            return True
        elif what_is_removed == constantes.LAYER5:
            # self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer,position=(line,column),update_type="delete")
            self.visualmap.update_layers(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)

            return True
        elif what_is_removed == constantes.LAYER3:
            self.visualmap.update_layers(self.visualmap.trees_layer, self.game.map.trees_layer.array)
            return True
        return False

    def remove_elements_serie(self, start_pos, end_pos) -> bool:
        """
        Pour clean une surface de la carte
        Cette fonction doit être associée au bouton pelle
        """
        line1, column1 = self.visualmap.get_sprite_at_screen_coordinates(start_pos)
        line2, column2 = self.visualmap.get_sprite_at_screen_coordinates(end_pos)
        modified_layers = self.game.remove_elements_serie((line1, column1), (line2, column2))
        ret = False
        if constantes.LAYER5 in modified_layers:
            self.visualmap.update_layers(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
            ret = True
        if constantes.LAYER3 in modified_layers:
            self.visualmap.update_layers(self.visualmap.trees_layer, self.game.map.trees_layer.array)
            ret = True
        if constantes.LAYER4 in modified_layers:
            self.visualmap.update_layers(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            ret = True
        return ret

    # ===============================================
    # Message text
    # ===============================================
    def draw_message_for_farm_building(self):
        start_y = constantes.DEFAULT_SCREEN_HEIGHT - 50
        error_message = arcade.Text(
            "Farms can only be built on yellow grass!!",
            0, 0,
            arcade.color.BLUE_GREEN,
            15,
            font_name=(
                "Lato",
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems
            )
        )
        start_x = (constantes.DEFAULT_SCREEN_WIDTH - error_message.content_width) // 2
        error_message.position = (start_x, start_y)
        error_message.draw()

    # ===============================================
    # Side tab buttons functions (too hard to place anywhere else)
    # ===============================================

    def button_click_house(self, event):
        print("button dwell")
        self.remove_mode = False
        window = arcade.get_window()
        window.set_mouse_visible(True)
        self.builder_mode = True
        self.builder_content = "dwell"
        fct.draw_normal_cursor()

    def button_click_shovel(self, event):
        self.builder_mode = False
        self.dragged_sprite.clear()
        # We replace the cursor with a shovel image
        arcade.get_window().set_mouse_visible(False)
        self.remove_mode = True
        print("shovel")

    def button_click_road(self, event):
        print("button road")
        self.dragged_sprite.clear()
        self.remove_mode = False
        window = arcade.get_window()
        window.set_mouse_visible(True)
        self.builder_mode = True
        self.builder_content = "road"
        fct.draw_normal_cursor()
        pass

    def attribute_on_click(self):
        l = ["", "", "", "", "", "", "", "", "water", "health", "religion", "roll", "entertainment", "education",
             "hammer", "sword", "carry"]
        for i in range(0, len(l)):
            if i > 7:
                self.buttons[i].on_click = UI_buttons.define_on_click_button_manager(self, l[i])

    def fill_manager(self, button_list, manager):
        for button in button_list:
            txt = (button.my_text.split(":"))[0]
            button.on_click = UI_buttons.define_on_click_build(self, txt)
            self.right_panel_manager_depth_one[manager].add(button)

    def select_manager(self, manager):
        match manager:
            case "water":
                self.fill_manager(UI_buttons.button_list(gdata.text_water), manager)
            case "health":
                self.fill_manager(UI_buttons.button_list(gdata.text_health), manager)
            case "religion":
                self.fill_manager(UI_buttons.button_list(gdata.text_religion), manager)
            case "education":
                self.fill_manager(UI_buttons.button_list(gdata.text_education), manager)
            case "roll":
                self.fill_manager(UI_buttons.button_list(gdata.text_roll), manager)
            case "entertainment":
                self.fill_manager(UI_buttons.button_list(gdata.text_entertainment), manager)
            case "hammer":
                self.fill_manager(UI_buttons.button_list(gdata.text_hammer), manager)
            case "sword":
                self.fill_manager(UI_buttons.button_list(gdata.text_sword), manager)
            case "carry":
                self.fill_manager(UI_buttons.button_list(gdata.text_carry), manager)

    def select_all_manager(self):
        for k in self.right_panel_manager_depth_one.keys():
            self.select_manager(k)

    def hide_all_manager(self):
        for manager in self.manager_state.items():
            self.right_panel_manager_depth_one[manager[0]].disable()
            self.manager_state[manager[0]] = False
        self.layer_manager_show = False
        self.layer_manager.disable()

    def button_load_on_click(self, event):
        window = arcade.get_window()
        window.show_view(window.loadscreen)
        window.loadscreen.fromview = "game"
        pass

    def button_layer_on_click(self, event):
        self.layer_manager.enable()
        self.layer_manager_show = True

    def button_fps_up_on_click(self, event):
        self.game.change_game_speed(1)
        self.speed_ratio = self.game.framerate * 100 / constantes.DEFAULT_FPS
        pass

    def button_fps_down_on_click(self, event):
        self.game.change_game_speed(-1)
        self.speed_ratio = self.game.framerate * 100 / constantes.DEFAULT_FPS
        pass

    def button_fire_layer_on_click(self, event):
        self.visualmap.buildings_layer.visible = False
        self.visualmap.fire_risk_layer_show = True
        self.visualmap.collapse_risk_layer_show = False
        self.visualmap.destroyed_layer_show = False
        self.visualmap.fire_layer_show = False
        self.visualmap.ownership_layer_show = False

    def button_collapse_layer_on_click(self, event):
        self.visualmap.buildings_layer.visible = False
        self.visualmap.fire_risk_layer_show = False
        self.visualmap.collapse_risk_layer_show = True
        self.visualmap.destroyed_layer_show = False
        self.visualmap.fire_layer_show = False
        self.visualmap.ownership_layer_show = False

    def button_owner_layer_on_click(self,event):
        self.visualmap.buildings_layer.visible = False
        self.visualmap.fire_risk_layer_show = False
        self.visualmap.collapse_risk_layer_show = False
        self.visualmap.destroyed_layer_show = False
        self.visualmap.fire_layer_show = False
        self.visualmap.ownership_layer_show = True
    
    def button_normal_layer_on_click(self, event):
        self.visualmap.buildings_layer.visible = True
        self.visualmap.fire_risk_layer_show = False
        self.visualmap.collapse_risk_layer_show = False
        self.visualmap.destroyed_layer_show = True
        self.visualmap.fire_layer_show = True
        self.visualmap.ownership_layer_show = False
        self.visualmap.update_layers(self.visualmap.buildings_layer,self.game.map.buildings_layer.array)

    def get_surface_dragged(self, start, end):
        line1, column1 = self.visualmap.get_sprite_at_screen_coordinates(start)
        line2, column2 = self.visualmap.get_sprite_at_screen_coordinates(end)
        self.surface_drag = []
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
                self.surface_drag.append((i, j))

    def mouse_changed_sprite(self):
        x, y = self.mouse_pos
        a, b, c, d = self.actual_sprite_limit

    def save_game(self, game_name):
        saveload.save_game(self.game, game_name)

    def load_game(self, game_name):
        self.game = saveload.load_game(game_name)
        self.visualmap.setup(self.game)

    def delete_game(self, game_name):
        saveload.delete_game(game_name)

    def list_saved_games(self):
        for _game in saveload.list_saved_games():
            # do whatever u want with that
            print(_game)

    def update_treatment(self, update: updates.LogicUpdate):
        """
        This is the function that will really update graphically the sprites of the buildings
        """
        for j in update.catchedfire:
            self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer, position=j,
                                             update_type="building_fire")
        for k in update.collapsed:
            self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer, position=k,
                                             update_type="building_destroy")
        # Devolve before evolved -- order is important
        for m in update.has_devolved:
            self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer, position=m[0],
                                             update_type="stat_dec", special_value=m[1])
        for l in update.has_evolved:
            self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer, position=l[0],
                                             update_type="stat_inc", special_value=l[1])

        for n in update.removed:
            self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer, position=n, update_type="delete")
        for briskfire in update.fire_level_change:
            self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer, position=briskfire[0],
                                             update_type="risk_update", special_value=("fire", briskfire[1]))
        for briskcollapse in update.collapse_level_change:
            self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer, position=briskcollapse[0],
                                             update_type="risk_update", special_value=("collapse", briskcollapse[1]))
