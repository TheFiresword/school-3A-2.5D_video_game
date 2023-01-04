import pyglet

from UserInterface import UI_Section as uis
from UserInterface import UI_buttons
from UserInterface import UI_HUD_Build as hudb
from UserInterface import UI_Visual_Map as uivm
from UserInterface import UI_Text_Display as text
from UserInterface import UI_PoP_Up as pop

import CoreModules.GameManagement.Game as game
import CoreModules.MapManagement.mapManagementMap as map
from CoreModules.UpdateManagement import Update as updates

from Services import servicesGlobalVariables as constantes
from Services import Service_Game_Data as gdata
from Services import Service_Static_functions as fct
from Services import Service_Save_and_Load as saveload

import arcade
import arcade.gui

from pyglet.math import Vec2

MAP_CAMERA_SPEED = 0.5

class GameView(arcade.View):

    def __init__(self, _game):
        super().__init__()
        self.game = None
        if _game:
            self.game = _game
        # =======================================
        # Intels about the current player action
        # =======================================
        self.mouse_pos = (0, 0)
        self.real_mouse_pos = (0,0)
        self.init_mouse_pos = (0, 0)
        self.actual_sprite_limit = (0,0,0,0)
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
        self.right_panel_manager_depth_one = {"water":arcade.gui.UIManager(),
                                              "health":arcade.gui.UIManager(),
                                              "religion":arcade.gui.UIManager(),
                                              "education":arcade.gui.UIManager(),
                                              "entertainment":arcade.gui.UIManager(),
                                              "roll":arcade.gui.UIManager(),
                                              "hammer":arcade.gui.UIManager(),
                                              "sword":arcade.gui.UIManager(),
                                              "carry":arcade.gui.UIManager()
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
        self.menusect = uis.MenuSect()
        self.map_camera = arcade.Camera()
        self.menu_camera = arcade.Camera()

        # =======================================
        # Visuals elements excepts ones Map related 
        # =======================================
        self.tab = arcade.load_texture(constantes.SPRITE_PATH + "PanelsOther/paneling_00017.png")
        self.bar = arcade.load_texture(constantes.SPRITE_PATH + "Panel\panel0.png")
        self.money_box = arcade.load_texture(constantes.SPRITE_PATH + "PanelsOther/paneling_00015.png")
        self.actual_pop_up = pop.create_PoP_Up(image= constantes.SPRITE_PATH + "Pictures/panelwindows_00021.png" ,title="AU FEU",normal_text="tchoupi",carved_text="Y'a le feu quelque part allez éteindre ça\n je suis sur ca marche",top_left_corner=(0,constantes.DEFAULT_SCREEN_HEIGHT - self.bar.image.size[1]),order=["title_zone","image_zone","carved_text_zone","button_zone"])
        self.money_text = None
        buttons_render = UI_buttons.buttons
        self.buttons = [arcade.gui.UITextureButton(x=b0, y=b1, texture=b2, texture_hovered=b3, texture_pressed=b4,
                                                   scale=constantes.SPRITE_SCALING) for
                        (b0, b1, b2, b3, b4) in buttons_render]
        self.buttons[5].on_click = self.button_click_house
        self.buttons[6].on_click = self.button_click_shovel
        self.buttons[7].on_click = self.button_click_road
        self.select_all_manager()
        self.attribute_on_click()
        #self.buttons[8].on_click = UI_buttons.define_on_click_button_manager(self,"water")
        #self.buttons[9].on_click = UI_buttons.define_on_click_button_manager(self,"health")
        #self.buttons[10].
        
        
        for k in self.buttons:
            self.right_panel_manager.add(k)

        # =======================================
        # Map related Visuals elements 
        # =======================================
        self.visualmap = uivm.VisualMap()
        self.dragged_sprite = arcade.SpriteList()

        # =======================================
        # Preliminary actions
        # =======================================
        self.setup()
        pass

    def setup(self):
        if not self.game:
            self.game = game.Game(map.MapLogic())
        self.game.create_walker()
        self.game.walkersGetOut()
        self.money_text=text.Sprite_sentence("Dn: " +str(self.game.money),"white",(205,constantes.DEFAULT_SCREEN_HEIGHT-self.bar.image.size[1]/4))
        self.visualmap.setup(self.game)
        self.center_map()
        self.builder_content = ""
        

    # =======================================
    #  View Related Fuctions
    # =======================================
    def on_show_view(self):
        pass

    def on_hide(self):
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
                        hollow = hudb.hollow_build(self.mouse_pos[0], self.mouse_pos[1],self.visualmap,gdata.building_dico[self.builder_content.lower()])
                    else:
                        hollow = hudb.hollow_build(self.mouse_pos[0], self.mouse_pos[1],self.visualmap)
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
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT-self.bar.image.size[1]/4,
                                      width=self.bar.image.size[0]/2, height=self.bar.image.size[1]/2,
                                      texture=self.bar)
        arcade.draw_texture_rectangle(center_x=300,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT-self.bar.image.size[1]/4,
                                      width=(len(self.money_text.sentence)+5) * constantes.FONT_WIDTH/2, height=self.bar.image.size[1]/2,
                                      texture=self.money_box)
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH - 81,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - 285 + 47,
                                      width=162, height=constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                      texture=self.tab
                                      )
        self.money_text.draw_()
        self.right_panel_manager.draw()
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
        if self.actual_pop_up.visible:
            self.actual_pop_up.draw_()

            

    def on_update(self, delta_time: float):
        update = self.game.updategame()
        self.update_treatment(update)
        self.visualmap.fire_count += 1
        for sprite in self.visualmap.fire_layer:
            sprite.set_texture(self.visualmap.fire_count % len(sprite.textures))

        self.move_map_camera_with_keys()
        for walker in self.game.walkersOut:
            walker.walk(self.visualmap.map_scaling)
        self.visualmap.update_walker_list(self.game.walkersOut)
        self.money_text = text.Sprite_sentence("Dn: " +str(self.game.money),"white",(320-(len(self.money_text.sentence)+5) * constantes.FONT_WIDTH/4,constantes.DEFAULT_SCREEN_HEIGHT-self.bar.image.size[1]/4))
        

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
            if button == arcade.MOUSE_BUTTON_LEFT and not self.actual_pop_up.visible:
                self.visualmap.red_sprite = arcade.Sprite(constantes.SPRITE_PATH + "Land/LandOverlay/Land2a_00037.png",
                                                          scale=self.visualmap.map_scaling, center_x=map_pos_x,
                                                          center_y=map_pos_y, hit_box_algorithm="Detailed")
                self.visualmap.red_sprite.visible = True
                if not self.builder_mode and not self.builder_content == "road":
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
        self.real_mouse_pos= (x,y)
        self.mouse_pos = Vec2(x, y) + self.map_camera.position
        tmp_end_pos = Vec2(x, y) + self.map_camera.position
        if self.mouse_left_pressed:
            if self.builder_mode:
                if self.builder_content == "road":
                    if self.mouse_left_maintained:
                        self.add_roads_serie(self.init_mouse_pos, tmp_end_pos, True)
                    else:
                        self.add_roads_serie(self.init_mouse_pos, tmp_end_pos)
                else:
                    self.get_surface_dragged(self.init_mouse_pos,tmp_end_pos)
                    self.dragged_sprite.clear()
                    self.visualmap.fill_temporary_build(self.surface_drag,self.dragged_sprite,self.builder_content,"build")
            if self.remove_mode:
                self.get_surface_dragged(self.init_mouse_pos,tmp_end_pos)
                self.dragged_sprite.clear()
                self.visualmap.fill_temporary_build(self.surface_drag,self.dragged_sprite,self.builder_content,"remove")


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
            self.save_game('game1')
        # press L to load game1
        elif symbol == arcade.key.L:
            self.load_game('game1')
        # press D to delete game1
        elif symbol == arcade.key.D:
            self.delete_game('game1')
        elif symbol == arcade.key.P:
            self.game.walkersOutUpdates()

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.UP:
            self.up_pressed = False
        elif _symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif _symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif _symbol == arcade.key.RIGHT:
            self.right_pressed = False

    # =======================================
    #  Camera Related Fuctions
    # =======================================

    def move_map_camera_with_keys(self):

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
   
    def add_one_sized_building(self,pos):
        # ================================
        #       Add single tile Building
        # ================================
        line, column = self.visualmap.get_sprite_at_screen_coordinates(pos)
        if self.game.add_building(line, column, gdata.building_dico[self.builder_content].name):
            # si la route a été bien ajoutée on update la spritelist en la recréant
            building = self.game.map.buildings_layer.array[line][column]
            #self.visualmap.update_one_sprite(layer = self.visualmap.buildings_layer, position = (line,column),
            #        update_type="change_content", new_texture_path=[path[0] for path in building.file_paths])
            self.visualmap.update_layers(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
            return True
        return False

    def add_multiple_one_sized_building(self):
        for (line,column) in self.surface_drag:
            if self.game.add_building(line,column,self.builder_content):
                building = self.game.map.buildings_layer.array[line][column]
                self.visualmap.update_one_sprite(layer = self.visualmap.buildings_layer, position = (line,column),
                        update_type="change_content", new_texture_path=[path[0] for path in building.file_paths])
            else:
                print("Building failed")

        #self.visualmap.update_layers(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)

    def remove_sprite(self, pos) -> bool:
        line, column = self.visualmap.get_sprite_at_screen_coordinates(pos)
        what_is_removed = self.game.remove_element((line, column))
        if what_is_removed == constantes.LAYER4:
            self.visualmap.update_layers(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            return True
        elif what_is_removed == constantes.LAYER5:
            #self.visualmap.update_one_sprite(layer=self.visualmap.buildings_layer,position=(line,column),update_type="delete")
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
        # We replace the cursor with a shovel image
        arcade.get_window().set_mouse_visible(False)
        self.remove_mode = True
        print("shovel")

    def button_click_road(self, event):
        print("button road")
        self.remove_mode = False
        window = arcade.get_window()
        window.set_mouse_visible(True)
        self.builder_mode = True
        self.builder_content = "road"
        fct.draw_normal_cursor()
        pass

    def attribute_on_click(self):
        l = ["","","","","","","","","water","health","religion","roll","entertainment","education","hammer","sword","carry"]
        for i in range(0,len(l)):
            if i > 7:
                self.buttons[i].on_click = UI_buttons.define_on_click_button_manager(self,l[i])
        
    def fill_manager(self,button_list,manager):
            for button in button_list:
                txt =  (button.my_text.split(":"))[0]
                button.on_click = UI_buttons.define_on_click_build(self,txt)
                self.right_panel_manager_depth_one[manager].add(button)

    def select_manager(self,manager):
        match manager:
            case "water": self.fill_manager(UI_buttons.button_list(gdata.text_water),manager)
            case "health": self.fill_manager(UI_buttons.button_list(gdata.text_health),manager)
            case "religion": self.fill_manager(UI_buttons.button_list(gdata.text_religion),manager)
            case "education": self.fill_manager(UI_buttons.button_list(gdata.text_education),manager)
            case "roll": self.fill_manager(UI_buttons.button_list(gdata.text_roll),manager)
            case "entertainment": self.fill_manager(UI_buttons.button_list(gdata.text_entertainment),manager)
            case "hammer": self.fill_manager(UI_buttons.button_list(gdata.text_hammer),manager)
            case "sword": self.fill_manager(UI_buttons.button_list(gdata.text_sword),manager)
            case "carry": self.fill_manager(UI_buttons.button_list(gdata.text_carry),manager)

    def select_all_manager(self):
        for k in self.right_panel_manager_depth_one.keys():
            self.select_manager(k)

    def hide_all_manager(self):
        for manager in self.manager_state.items():
            self.right_panel_manager_depth_one[manager[0]].disable()
            self.manager_state[manager[0]] = False

    def button_click_depht(self, event , button):
        pass
    
    def get_surface_dragged(self,start,end):
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
                self.surface_drag.append((i,j))
    
    def mouse_changed_sprite(self):
        x,y = self.mouse_pos
        a,b,c,d = self.actual_sprite_limit

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

    def update_treatment(self,update:updates.LogicUpdate):
        for k in update.catchedfire:
            self.visualmap.update_one_sprite(layer = self.visualmap.buildings_layer,position = k ,update_type="building_fire",new_texture_path=[])
        for j in update.collapsed:
            self.visualmap.update_one_sprite(layer = self.visualmap.buildings_layer,position = j ,update_type="building_destroy",new_texture_path=[])

