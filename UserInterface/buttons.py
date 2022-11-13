import arcade.gui
import arcade


class QuitButton(arcade.gui.UITextureButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class SettingButton(arcade.gui.UITextureButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.get_window()
        window.settingscreen.setup()
        window.show_view(window.settingscreen)



class NewGameButton(arcade.gui.UITextureButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.get_window()
        window.hide_view()
        window.show_view(window.gamescreen)

class LoadGameButton(arcade.gui.UITextureButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.get_window()
        window.show_view(window.loadscreen)
