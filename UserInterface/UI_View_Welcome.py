import arcade
from Services import servicesGlobalVariables as constantes
from UserInterface import UI_buttons as but
import arcade.gui

class WelcomeScreen(arcade.View):

    def __init__(self):
        super().__init__()
        self.step = 0
        self.logo = arcade.load_texture(constantes.SPRITE_PATH +"Screens/C3title_00001.png")
        self.background = arcade.load_texture(constantes.SPRITE_PATH + "Screens/0_fired_00001.png")
        arcade.set_background_color(arcade.color.AMAZON)

        self.buttons_manager = arcade.gui.UIManager()
        self.newgame_button = but.NewGameButton(x=constantes.MIDDLE[0]-100,y=constantes.MIDDLE[1]+40+15+7.5,texture= but.texture_panel11,my_text="New Game", width=200, height=40,color="black")
        self.load_button = but.LoadGameButton(x=constantes.MIDDLE[0]-100,y=constantes.MIDDLE[1]+7.5,texture= but.texture_panel11, my_text="Load Game", width=200, height=40,color="black")
        self.settings_button = but.SettingButton(x=constantes.MIDDLE[0]-100,y=constantes.MIDDLE[1]-40-7.5,texture= but.texture_panel11, my_text="Settings", width=200, height=40,color="black")
        self.quit_button = but.QuitButton(x=constantes.MIDDLE[0]-100,y=constantes.MIDDLE[1]-80-15-7.5,texture= but.texture_panel11, my_text="Leave Game", width=200, height=40,color="black")
        
        self.buttons_manager.add(self.newgame_button)
        self.buttons_manager.add(self.load_button)
        self.buttons_manager.add(self.settings_button)
        self.buttons_manager.add(self.quit_button)

    def on_show_view(self):
        if self.step != 0:
            self.buttons_manager.enable()

    def on_draw(self):
        arcade.start_render()
        self.clear()
        if self.step == 0:
            arcade.draw_texture_rectangle(center_x= constantes.DEFAULT_SCREEN_WIDTH/2, center_y=constantes.DEFAULT_SCREEN_HEIGHT/2,
                                      width=constantes.DEFAULT_SCREEN_WIDTH, height=constantes.DEFAULT_SCREEN_HEIGHT,
                                      texture= self.logo)
        if self.step == 1:
            arcade.draw_texture_rectangle(center_x= constantes.DEFAULT_SCREEN_WIDTH/2, center_y=constantes.DEFAULT_SCREEN_HEIGHT/2,
                                      width=constantes.DEFAULT_SCREEN_WIDTH, height=constantes.DEFAULT_SCREEN_HEIGHT,
                                      texture= self.background)
            self.buttons_manager.draw()
            self.newgame_button.draw_()
            self.load_button.draw_()
            self.settings_button.draw_()
            self.quit_button.draw_()

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.step == 0:
            self.step = 1
            self.buttons_manager.enable()

    def on_hide_view(self):
        self.clear()
        self.buttons_manager.disable()