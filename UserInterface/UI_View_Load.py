import arcade
from Services import servicesGlobalVariables as constantes
from UserInterface import UI_buttons as but
import arcade.gui

class LoadScreen(arcade.View):
    def __init__(self):
        super().__init__()
        # =======================================
        # Intels about the current player action
        # =======================================
        self.real_mouse_pos = (0,0)
        self.mouse_left_pressed, self.mouse_right_pressed = False, False
        self.mouse_left_maintained, self.mouse_right_maintained = False, False
        self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed = False, False, False, False
        # =======================================
        # Arcade stuff
        # =======================================
        arcade.set_background_color(arcade.color.BLACK)
        self.right_panel_manager = arcade.gui.UIManager()
        self.right_panel_manager.enable()
        self.map_camera = arcade.Camera()
        self.menu_camera = arcade.Camera()
        # =======================================
        # Visuals elements excepts ones Map related 
        # =======================================
        # =======================================
        # Map related Visuals elements 
        # =======================================
        # =======================================
        # Preliminary actions
        # =======================================
        pass
        arcade.set_background_color(arcade.color.BLACK)

    def on_show_view(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_text("Load Screen - click to advance", constantes.DEFAULT_SCREEN_WIDTH/ 2, constantes.DEFAULT_SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        print(symbol)

    def on_hide(self):
        pass

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_hide_view(self):
        self.clear()