import arcade
from Services import servicesGlobalVariables as constantes
import arcade.gui

class LoadScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.AMAZON)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)
    def on_draw(self):
        self.clear()
        arcade.draw_text("Load Screen - click to advance", constantes.DEFAULT_SCREEN_WIDTH/ 2, constantes.DEFAULT_SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
    def on_key_press(self, symbol: int, modifiers: int):
        print(symbol)
    def on_hide(self):
        self.manager.disable()