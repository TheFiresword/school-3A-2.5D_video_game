import arcade
import arcade.gui

from Services import servicesGlobalVariables as constantes
from Services import Service_Save_and_Load as sal

from UserInterface import UI_buttons as but
from UserInterface import UI_View_Game as rgv
from UserInterface import UI_Text_Display as texts

class LoadScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.fromview = ""
        # =======================================
        # Intels about the current player action
        # =======================================
        self.real_mouse_pos = (0,0)
        self.mouse_left_pressed, self.mouse_right_pressed = False, False
        self.mouse_left_maintained, self.mouse_right_maintained = False, False
        self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed = False, False, False, False
        self.selected_game = ""
        # =======================================
        # Arcade stuff
        # =======================================
        arcade.set_background_color(arcade.color.BLACK)
        self.background = arcade.load_texture(constantes.SPRITE_PATH + "Screens/0_fired_00001.png")
        self.manager = arcade.gui.UIManager()
        self.selec_manager = arcade.gui.UIManager()
        # =======================================
        # Visuals elements  
        # =======================================
        self.box = arcade.load_texture(constantes.SPRITE_PATH + "Panel/panel1.png")
        self.input = arcade.gui.UIInputText(x=constantes.DEFAULT_SCREEN_WIDTH/2 - (self.box.image.size[0]/2) + 10,
                                            y= constantes.DEFAULT_SCREEN_HEIGHT/2 - (self.box.image.size[1]/2) + 10)
        self.leave_button = arcade.gui.UITextureButton(x=constantes.DEFAULT_SCREEN_WIDTH/2 + (self.box.image.size[0]/2) - 95,
                                                       y= constantes.DEFAULT_SCREEN_HEIGHT/2 - (self.box.image.size[1]/2) + 20,
                                                       texture= arcade.load_texture(constantes.SPRITE_PATH + "Pictures/Picture2_00009.png")
                                                       ,scale=3/4 )
        self.validate_button = arcade.gui.UITextureButton(x=constantes.DEFAULT_SCREEN_WIDTH/2 + (self.box.image.size[0]/2) - 160,
                                                       y= constantes.DEFAULT_SCREEN_HEIGHT/2 - (self.box.image.size[1]/2) + 20,
                                                       texture= arcade.load_texture(constantes.SPRITE_PATH + "Panel\Panel40\paneling_00239.png")
                                                       ,scale=3/4 )                                               
        self.leave_button.on_click = self.leave_button_on_click
        self.validate_button.on_click = self.validate_button_on_click
        self.saved_game = sal.list_saved_games()
        for k in range(0,len(self.saved_game)):
            button = but.Text_Button_background(x=constantes.MIDDLE[0]-150,y=constantes.MIDDLE[1]+(self.box.image.size[1]/2)-80 - k*24 ,texture= but.texture_panel46,my_text=self.saved_game[k], width=150, height=24,color="black")
            button.on_click = but.define_on_click_button_selected(self,button)
            self.selec_manager.add(button)
        self.text = texts.Sprite_sentence("Selected game :  " + self.selected_game,"black",(constantes.DEFAULT_SCREEN_WIDTH/2 - (self.box.image.size[0]/2)+30,constantes.MIDDLE[1]+(self.box.image.size[1]/2)-30))


        # =======================================
        # Preliminary actions
        # =======================================
        arcade.set_background_color(arcade.color.BLACK)
        self.setup()
        
    
    def setup(self):
        self.manager.add(self.input)
        self.manager.add(self.validate_button)
        self.manager.add(self.leave_button)
        
    def on_show_view(self):
        self.manager.enable()
        self.selec_manager.enable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(center_x= constantes.DEFAULT_SCREEN_WIDTH/2, center_y=constantes.DEFAULT_SCREEN_HEIGHT/2,
                                      width=constantes.DEFAULT_SCREEN_WIDTH, height=constantes.DEFAULT_SCREEN_HEIGHT,
                                      texture= self.background)
        arcade.draw_texture_rectangle(center_x= constantes.DEFAULT_SCREEN_WIDTH/2, center_y=constantes.DEFAULT_SCREEN_HEIGHT/2,
                                      width=self.box.image.size[0], height=self.box.image.size[1],
                                      texture= self.box)
        self.manager.draw()
        self.selec_manager.draw()
        for k in self.selec_manager.children[0]:
                        k.draw_()
        self.text.draw_()
    
    def on_update(self, delta_time: float):
        self.text =texts.Sprite_sentence("Selected game :  " + self.selected_game,"black",(constantes.DEFAULT_SCREEN_WIDTH/2 - (self.box.image.size[0]/2)+30,constantes.MIDDLE[1]+(self.box.image.size[1]/2)-30))


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.leave_button_on_click(None)
        if symbol == arcade.key.SPACE:
            print(self.selected_game)
        

    def on_hide(self):
        pass

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_hide_view(self):
        self.clear()
        self.manager.disable()
        self.selec_manager.disable()
    
    def leave_button_on_click(self,event):
        window = arcade.get_window()
        window.settingscreen.setup()
        if self.fromview == "welcome":
            window.show_view(window.welcomescreen)
        if self.fromview == "game":
            window.show_view(window.gamescreen)
    
    def validate_button_on_click(self,event):
        window = arcade.get_window()
        window.settingscreen.setup()
        if self.selected_game != "":
            window.gamescreen = rgv.GameView(_game=sal.load_game(self.selected_game.split(".")[0]))
            window.show_view(window.gamescreen)