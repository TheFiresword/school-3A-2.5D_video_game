import arcade
from Services import servicesGlobalVariables as constantes

class MapSect(arcade.Section):
    def __init__(self):
        super().__init__(left=0,bottom=0,width=constantes.DEFAULT_SCREEN_WIDTH-162,height=constantes.DEFAULT_SCREEN_HEIGHT,name="map_sect")





class MenuSect(arcade.Section):
    def __init__(self):
        super().__init__(left=constantes.DEFAULT_SCREEN_WIDTH-162,bottom=0,width=162,height=constantes.DEFAULT_SCREEN_HEIGHT,name="menu_sect")





