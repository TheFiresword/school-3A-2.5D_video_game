from UserInterface import UI_Section as uis
from UserInterface import UI_buttons
from UserInterface import UI_HUD_Build as hudb
from UserInterface import UI_Visual_Map as uivm

import CoreModules.GameManagement.Game as game
import CoreModules.MapManagement.mapManagementMap as map

from Services import servicesGlobalVariables as constantes
from Services import Service_Game_Data as gdata

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
        #=======================================
        self.mouse_pos = (0,0)
        self.init_mouse_pos = (0,0)
        self.mouse_left_pressed, self.mouse_right_pressed = False, False
        self.mouse_left_maintained ,self.mouse_right_maintained = False ,False
        self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed = False, False, False, False
        
        self.builder_mode = False
        self.builder_content = ""
        self.remove_mode = None
        #=======================================
        # Arcade stuff
        # =======================================
        arcade.set_background_color(arcade.color.BLACK)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.menusect = uis.MenuSect()
        self.map_camera = arcade.Camera()
        self.menu_camera = arcade.Camera()
        # =======================================
        # Visuals elements excepts ones Map related 
        # =======================================
        self.tab = arcade.load_texture(constantes.SPRITE_PATH + "PanelsOther/paneling_00017.png")
        self.bar = arcade.load_texture(constantes.SPRITE_PATH + "Panel\Panel2\paneling_00010.png")
        buttons_render = UI_buttons.buttons
        self.buttons = [arcade.gui.UITextureButton(x=b0, y=b1, texture=b2, texture_hovered=b3, texture_pressed=b4,scale= constantes.SPRITE_SCALING) for
                        (b0, b1, b2, b3, b4) in buttons_render]
        self.buttons[6].on_click = self.button_click_shovel
        self.buttons[7].on_click = self.button_click_road
        
        for k in self.buttons:
            self.manager.add(k)
        
        #=======================================
        # Map related Visuals elements 
        # =======================================
        self.visualmap = uivm.VisualMap()

        # =======================================
        # Preliminary actions
        # =======================================
        self.setup()
        pass

    def setup(self):
        if not self.game:
            self.game = game.Game(map.MapLogic())
        self.visualmap.setup(self.game)
        self.center_map()
        self.builder_content = "Dwell"

    # =======================================
    #  View Related Fuctions
    # =======================================
    def on_show_view(self):
        pass

    def on_hide(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        # =======================================
        # Display Map related content
        # =======================================
        self.map_camera.use()  # select camera linked to map
        if self.game.map.active:  # if map displayed
            self.visualmap.draw_layers(self.game)
            #Test click on map
            if self.visualmap.red_sprite.visible: 
                #self.visualmap.red_sprite.draw_hit_box(color=(255, 0, 0), line_thickness=1)
                self.visualmap.red_sprite.alpha = 80
                self.visualmap.red_sprite.color= (255, 0, 0)
                self.visualmap.red_sprite.draw()

            if self.builder_mode and self.builder_content != "road":
                hollow = hudb.hollow_build(self.mouse_pos[0], self.mouse_pos[1], gdata.building_dico[self.builder_content],self.visualmap)
                hollow.draw()
            
            if self.remove_mode:
                hollow = hudb.hollow(self.mouse_pos[0], self.mouse_pos[1])
                hollow.draw()
        # =======================================
        # Display Menu related content
        # =======================================
        self.menu_camera.use()
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH/2,center_y=constantes.DEFAULT_SCREEN_HEIGHT-20,
                                     width=constantes.DEFAULT_SCREEN_WIDTH,height=40,texture=self.bar)
        arcade.draw_texture_rectangle(center_x=constantes.DEFAULT_SCREEN_WIDTH - 81,
                                      center_y=constantes.DEFAULT_SCREEN_HEIGHT - 285 +28,
                                      width=162, height=constantes.DEFAULT_SCREEN_HEIGHT / 2,
                                      texture=self.tab
                                      )
        self.manager.draw()

    def on_update(self, delta_time: float):
        self.move_map_camera_with_keys()

    # =======================================
    #  Mouse Related Fuctions
    # =======================================

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        #===================================
        #Left click Draw red rectangle around closest sprite to mouse
        #===================================
        
        (map_pos_x,map_pos_y) = Vec2(x, y) + self.map_camera.position
        self.init_mouse_pos = (map_pos_x,map_pos_y)
        if x < constantes.DEFAULT_SCREEN_WIDTH -165:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.visualmap.red_sprite = arcade.Sprite(constantes.SPRITE_PATH + "Land/LandOverlay/Land2a_00037.png",
                                        scale=self.visualmap.map_scaling, center_x=map_pos_x,
                                        center_y=map_pos_y, hit_box_algorithm="Detailed")
                self.visualmap.red_sprite.visible = True
                if not self.builder_mode and not self.builder_content == "road":
                    (nearest_sprite, d) = arcade.get_closest_sprite(self.visualmap.red_sprite, self.visualmap.buildings_layer)
                    self.visualmap.red_sprite.texture = nearest_sprite.texture
                else:
                    (nearest_sprite, d) = arcade.get_closest_sprite(self.visualmap.red_sprite, self.visualmap.grass_layer)
                self.visualmap.red_sprite.center_x, self.visualmap.red_sprite.center_y = nearest_sprite.center_x, nearest_sprite.center_y
                self.mouse_left_pressed = True
            # For testing
            if button == arcade.MOUSE_BUTTON_RIGHT:
                # Add a road
                self.mouse_right_pressed = True
                self.mouse_right_maintained = False
                self.visualmap.red_sprite.visible = False

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if x < constantes.DEFAULT_SCREEN_WIDTH -165:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if self.remove_mode:
                    print("remove")
                    if self.mouse_left_maintained:
                        self.remove_elements_serie(self.init_mouse_pos,(Vec2(x,y)+ self.map_camera.position))
                    else:
                        self.remove_sprite(self.mouse_pos)               
                if self.builder_mode:
                    if self.builder_content != "road":
                        print("add building")
                    else:
                        if not self.mouse_left_maintained:
                            self.add_road(self.mouse_pos)
                self.mouse_left_pressed = False
                self.mouse_left_maintained = False
       
            if button == arcade.MOUSE_BUTTON_RIGHT:
                self.mouse_right_pressed = False
                self.mouse_right_maintained = False
                # self.red_sprite.visible = False

        
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pos = Vec2(x, y) + self.map_camera.position
        tmp_end_pos = Vec2(x, y) + self.map_camera.position
        if self.mouse_left_pressed:
            if self.builder_mode and self.builder_content == "road":
                if self.mouse_left_maintained:
                    self.add_roads_serie(self.init_mouse_pos, tmp_end_pos, True)
                else:
                    self.add_roads_serie(self.init_mouse_pos, tmp_end_pos)
            self.mouse_left_maintained = True
        if self.mouse_right_pressed:
            self.mouse_right_maintained = True
    
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
            self.visualmap.red_sprite.visible = False
        elif symbol == arcade.key.N:
            self.builder_mode = False
        # ## Testing removing
        elif symbol == arcade.key.D:
            self.pre_remove = True

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.UP:
            self.up_pressed = False
        elif _symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif _symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif _symbol == arcade.key.RIGHT:
            self.right_pressed = False
        # ## Testing removing
        elif _symbol == arcade.key.D:
            self.pre_remove = False

    def move_map_camera_with_keys(self):

        if self.up_pressed and not self.down_pressed:
            self.scroll_to(self.map_camera.position + Vec2(0, 20))
        elif self.down_pressed and not self.up_pressed:
            self.scroll_to(self.map_camera.position + Vec2(0, -20))
        elif self.left_pressed and not self.right_pressed:
            self.scroll_to(self.map_camera.position + Vec2(-20, 0))
        elif self.right_pressed and not self.left_pressed:
            self.scroll_to(self.map_camera.position + Vec2(20, 0))

    # =======================================
    #  Camera Related Fuctions
    # =======================================
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

    def get_logic_element_associated(self, _sprite, _sprite_list):
        index = _sprite_list.index(_sprite)
        line = int(index / constantes.TILE_COUNT)
        column = int(index % constantes.TILE_COUNT)
        if _sprite_list == self.visualmap.grass_layer:
            return self.game.map.grass_layer.array[line][column]
        elif _sprite_list == self.visualmap.hills_layer:
            return self.game.map.hills_layer.array[line][column]
        elif _sprite_list == self.visualmap.trees_layer:
            return self.game.map.trees_layer.array[line][column]
        elif _sprite_list == self.visualmap.roads_layer:
            return self.game.map.roads_layer.array[line][column]
        elif _sprite_list == self.visualmap.buildings_layer:
            return self.game.map.buildings_layer.array[line][column]

    def get_sprite_associated(self, layer, position):
        index = position(0) * 40 + position(1)
        if layer == self.game.map.grass_layer:
            return self.visualmap.grass_layer[index]
        elif layer == self.game.map.hills_layer:
            return self.visualmap.hills_layer[index]
        elif layer == self.game.map.trees_layer:
            return self.visualmap.trees_layer[index]
        elif layer == self.game.map.roads_layer:
            return self.visualmap.roads_layer[index]
        elif layer == self.game.map.buildings_layer:
            return self.visualmap.buildings_layer[index]

    def add_road(self, pos) -> bool:
        """
        Fonction d'ajout de route
        va probablement être transformée en fonction plus générale d'ajout d'élément
        """
        line, column = self.visualmap.get_sprite_at_screen_coordinates(pos)

        if self.game.map.roads_layer.set_cell_constrained_to_bottom_layer([self.game.map.buildings_layer,
                                                                           self.game.map.hills_layer,
                                                                           self.game.map.trees_layer,
                                                                           self.game.map.roads_layer], line,
                                                                          column):
            # si la route a été bien ajoutée on update la spritelist en la recréant
            self.visualmap.update_sprite_list(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            return True

    def add_roads_serie(self, start_pos, end_pos, dynamically=False) -> bool:
        """
        Fonction qui permet d'ajouter une série de routes
        Prend en paramètre 2 positions de souris sous forme de tuple
        """
        line1, column1 = self.visualmap.get_sprite_at_screen_coordinates(start_pos)
        line2, column2 = self.visualmap.get_sprite_at_screen_coordinates(end_pos)

        if self.game.map.roads_layer.add_roads_serie((line1, column1), (line2, column2),
                                                     [self.game.map.buildings_layer, self.game.map.trees_layer,
                                                      self.game.map.hills_layer, self.game.map.roads_layer],
                                                     memorize=dynamically):
            self.visualmap.update_sprite_list(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            return True
        return False

    def remove_sprite(self, pos) -> bool:
        line, column = self.visualmap.get_sprite_at_screen_coordinates(pos)
        what_is_removed = self.game.map.remove_element((line, column))
        if what_is_removed == constantes.LAYER4:
            self.visualmap.update_sprite_list(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            return True
        elif what_is_removed == constantes.LAYER5:
            self.visualmap.update_sprite_list(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
            return True
        elif what_is_removed == constantes.LAYER3:
            self.visualmap.update_sprite_list(self.visualmap.trees_layer, self.game.map.trees_layer.array)
            return True
        return False

    def remove_elements_serie(self, start_pos, end_pos) -> bool:
        """
        Pour clean une surface de la carte
        Cette fonction doit être associée au bouton pelle
        """
        line1, column1 = self.visualmap.get_sprite_at_screen_coordinates(start_pos)
        line2, column2 = self.visualmap.get_sprite_at_screen_coordinates(end_pos)
        modified_layers = self.game.map.remove_elements_serie((line1, column1), (line2, column2))
        if constantes.LAYER5 in modified_layers:
            self.visualmap.update_sprite_list(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
            return True
        if constantes.LAYER3 in modified_layers:
            self.visualmap.update_sprite_list(self.visualmap.trees_layer, self.game.map.trees_layer.array)
            return True
        if constantes.LAYER4 in modified_layers:
            self.visualmap.update_sprite_list(self.visualmap.roads_layer, self.game.map.roads_layer.array)
            return True
        return False
    
    #===============================================
    # Side tab buttons functions (too hard to place anywhere else)
    #===============================================

    def button_click_house(self):
        pass
    
    def button_click_shovel(self,event):
        self.builder_mode = False
        window = arcade.get_window()
        #window.set_mouse_visible(False)
        self.remove_mode = True
        print("shovel")
        pass    

    def button_click_road(self,event):
        print("button road")
        self.remove_mode = False
        window = arcade.get_window()
        #window.set_mouse_visible(True)
        self.builder_mode = True
        self.builder_content = "road"
        pass
    
    def button_click_water():
        pass

    def button_click_health():
        pass

    def button_click_lightning():
        pass

    def button_click_paper():
        pass

    def button_click_entertainement():
        pass

    def button_click_education():
        pass

    def button_click_hammer():
        pass

    def button_click_sword():
        pass

    def button_click_supply():
        pass

    def button_click_cross():
        pass

    def button_click_list():
        pass

    def button_click_bell():
        pass

