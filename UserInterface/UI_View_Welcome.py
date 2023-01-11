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
        self.newgame_button.on_click = self.replace_on_click

        self.buttons_manager.add(self.newgame_button)
        self.buttons_manager.add(self.load_button)
        self.buttons_manager.add(self.settings_button)
        self.buttons_manager.add(self.quit_button)
        self.input_field = arcade.gui.UIInputText(
          text_color=arcade.color.WHITE,
          y= constantes.MIDDLE[1],
          x=28+200,
          font_size=12,
          width=200,
          font_name="Arial",
          text='',
          )
        self.input_field.cursor_index = len(self.input_field.text)
        self.label = arcade.gui.UILabel(
            text="Enter Game Name",
            text_color=arcade.color.BLACK,
            y= constantes.MIDDLE[1] + 45,
            x= 20+200,
            width=350,
            height=40,
            font_size=22,
            font_name="Arial")
        self.real_new_game_button = arcade.gui.UITextureButton(x=260+200,y=constantes.MIDDLE[1] - 30 ,texture= arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel40/paneling_00241.png"),
                                                               texture_hovered=arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel40/paneling_00239.png"),
                                                               texture_pressed=arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel40/paneling_00240.png"),scale=1/2)
        self.real_new_game_button.on_click = self.on_create_click
        self.manager = arcade.gui.UIManager()
        self.manager.add(self.real_new_game_button)
        self.manager.add(self.label)
        self.manager.add(self.input_field)

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
        if self.manager._enabled:
            arcade.draw_texture_rectangle(center_x = 180+200, center_y=constantes.MIDDLE[1], width=350,height=200,texture=but.texture_panel1)
            arcade.draw_texture_rectangle(center_x= 180+200,center_y=constantes.MIDDLE[1]+40,width=320,height=20,texture=but.texture_panel46)
            self.manager.draw()
           

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.step == 0:
            self.step = 1
            self.buttons_manager.enable()

    def on_hide_view(self):
        self.clear()
        self.buttons_manager.disable()
    
    def on_create_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.get_window()
        window.update_name(self.input_field.text)
        window.hide_view()
        window.show_view(window.gamescreen)
    
    def replace_on_click(self,event):
        self.manager.enable()