import time
import arcade
import arcade.gui
from Services import servicesGlobalVariables as constantes
from UserInterface import buttons as but
from Infrastructure import settings as sets
from UserInterface import UI_View_Welcome as wv
from UserInterface import  UI_View_Map as gv

from UserInterface import UI_View_Settings as sv
from UserInterface import UI_View_Load as lv
class MainWindow(arcade.Window):

    # intialisation de la fenetre et lancement des premières instances d'affichage
    def __init__(self):
        super().__init__(constantes.DEFAULT_SCREEN_WIDTH, constantes.DEFAULT_SCREEN_HEIGHT, constantes.TITLE, fullscreen=True)
        self.set_update_rate(constantes.DEFAULT_FPS)

        # Différents écrans:
        self.welcomescreen = wv.WelcomeScreen()
        self.settingscreen = sv.SettingScreen()
        self.loadscreen = lv.LoadScreen()
        self.gamescreen = gv.MapView()


    # Lancement
    def setup(self):
        self.show_view(self.welcomescreen)

    # Comportement en cas de minimisation de la fenetre
    def on_hide(self):
        self.set_update_rate(0)

    def on_show(self):
        self.set_update_rate(constantes.DEFAULT_FPS)

    # Fonctions d'acquisition d'action joueur
    # Deplacement de la souris dans la fenetre
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        pass
    # Roulement mollette (affectiation du zoom ou lecture texte
    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        pass

    # Click de Souris
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        pass

    #Appuies de Touches
    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case _: pass












def main():
    window = MainWindow()
    window.setup()
    arcade.run()