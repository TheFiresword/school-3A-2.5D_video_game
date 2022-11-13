import arcade
from Services import servicesGlobalVariables as constantes
from UserInterface import buttons as but
import arcade.gui

class WelcomeScreen(arcade.View):

    def __init__(self):
        super().__init__()
        self.step = 0
        self.logo = arcade.load_texture(constantes.SPRITE_PATH +"Screens/C3title_00001.png")
        self.background = arcade.load_texture(constantes.SPRITE_PATH + "Screens/0_fired_00001.png")
        arcade.set_background_color(arcade.color.AMAZON)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        newgame_button = but.NewGameButton(text="Nouvelle Partie", width=200, height=28)
        self.v_box.add(newgame_button.with_space_around(bottom=15))
        load_button = but.LoadGameButton(text="Charger Partie", width=200, height=28)
        self.v_box.add(load_button.with_space_around(bottom=15))
        settings_button = but.SettingButton(text="Parametres", width=200, height=28)
        self.v_box.add(settings_button.with_space_around(bottom=15))
        quit_button = but.QuitButton(text="Quitter", width=200, height=28)
        self.v_box.add(quit_button.with_space_around(bottom=15))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        arcade.start_render()
        self.clear()
        arcade.draw_texture_rectangle(center_x= constantes.DEFAULT_SCREEN_WIDTH/2, center_y=constantes.DEFAULT_SCREEN_HEIGHT/2,
                                      width=constantes.DEFAULT_SCREEN_WIDTH, height=constantes.DEFAULT_SCREEN_HEIGHT,
                                      texture= self.logo if self.step == 0 else self.background)
        if self.step == 1:
            for i in range(0,12):
                for j in range(0,12):
                    arcade.draw_texture_rectangle(center_x= constantes.DEFAULT_SCREEN_WIDTH/2 + (j-5.5)*32,
                                              center_y=constantes.DEFAULT_SCREEN_HEIGHT/1.7 + (4-i)*32,
                                              width=32, height=32,
                                              texture= arcade.load_texture(constantes.SPRITE_PATH + "Panel/Panel1/paneling_00" + str(335+i*12+j) + ".png"))
            self.manager.draw()
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.step == 0:
            self.step = 1

    def on_hide_view(self):
        self.clear()
        self.manager.disable()