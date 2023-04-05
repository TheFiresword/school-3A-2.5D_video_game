import arcade
from UserInterface import UI_buttons as but
from Services import servicesGlobalVariables as constantes
import arcade.gui

class ReseauLoginScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.input_field = arcade.gui.UIInputText(
          text_color=arcade.color.RED,
          y= constantes.MIDDLE[1],
          x=28+200,
          font_size=12,
          width=200,
          font_name="Arial",
          text='XD',
          )
        self.input_field_port = arcade.gui.UIInputText(
          text_color=arcade.color.RED,
          y= constantes.MIDDLE[1]-100,
          x=28+200,
          font_size=12,
          width=200,
          font_name="Arial",
          text='',
          )
        self.input_field.cursor_index = len(self.input_field.text)
        self.input_field_port.cursor_index = len(self.input_field_port.text)
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
        self.manager.add(self.input_field_port)
        self.background = arcade.load_texture(constantes.SPRITE_PATH + "Screens/0_fired_00001.png")
        self.manager.enable()

    def on_create_click(self):      
        #IPC
        self.window.show_view(self.window.gamescreen)
        



    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(center_x= constantes.DEFAULT_SCREEN_WIDTH/2, center_y=constantes.DEFAULT_SCREEN_HEIGHT/2,
                                      width=constantes.DEFAULT_SCREEN_WIDTH, height=constantes.DEFAULT_SCREEN_HEIGHT,
                                      texture= self.background)
        arcade.draw_texture_rectangle(center_x = 180+200, center_y=constantes.MIDDLE[1], width=350,height=200,texture=but.texture_panel1)
        arcade.draw_texture_rectangle(center_x= 180+200,center_y=constantes.MIDDLE[1]+40,width=320,height=20,texture=but.texture_panel46)
        self.manager.draw()
        

    def on_hide(self):
        self.manager.disable()
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
        


    