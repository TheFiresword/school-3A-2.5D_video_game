import arcade
from Services import servicesGlobalVariables as constantes
from Services import Service_Static_functions as fct
from pyglet.math import Vec2


class VisualMap():
    
    def __init__(self):
        self.grass_layer = None
        self.hills_layer = None
        self.trees_layer = None
        self.roads_layer = None
        self.fire_layer = None
        self.collapse_layer = None
        self.buildings_layer = None
        self.walker_to_render = None
        self.map_scaling = constantes.SPRITE_SCALING
        self.red_sprite = arcade.Sprite()
        self.red_sprite.visible = False
        pass

    def setup(self,game):
        self.grass_layer = arcade.SpriteList(use_spatial_hash=True)
        self.hills_layer = arcade.SpriteList()
        self.trees_layer = arcade.SpriteList()
        self.roads_layer = arcade.SpriteList()
        self.buildings_layer = arcade.SpriteList()
        self.fire_layer = arcade.SpriteList()
        self.collapse_layer = arcade.SpriteList()
        self.walker_to_render = arcade.SpriteList()
        self.update_sprite_list(self.grass_layer, game.map.grass_layer.array)
        self.update_sprite_list(self.hills_layer, game.map.hills_layer.array)
        self.update_sprite_list(self.trees_layer, game.map.trees_layer.array)
        self.update_sprite_list(self.roads_layer, game.map.roads_layer.array)
        self.update_sprite_list(self.buildings_layer, game.map.buildings_layer.array)
        self.update_walker_list(self.walker_to_render,game.walkersOut)     
        pass

    def update_sprite_list(self, layer, array):
        layer.clear()
        k = 0
        for i in range(0, len(array)):  # I=On parcout le tableau logique du bas vers le haut
            line = array[i]
            for j in range(0, len(line)):
                file_name = array[i][j].file_path
                if file_name != "":
                    _sprite = arcade.Sprite(file_name, self.map_scaling)
                else:
                    _sprite = arcade.Sprite()
                # Les coordonnées de départ sont en cartésien
                count = array[i][j].dic['cells_number']

                """
                La taille des sprites peut déborder, donc il faut calculer ce débordement et l'ajouter comme offset
                pour que le coin inférieur gauche soit bien aligné avec sa case
                Ensuite, les coordonnées des sprites sont calculés en cartésien
                Puis transformés en isométriques
                Puis on ajoute l'offset
                """
                overflowing_height = (_sprite.height - constantes.TILE_HEIGHT * self.map_scaling * count) / 2
                overflowing_width = (_sprite.width - constantes.TILE_WIDTH * self.map_scaling * count) / 2

                if _sprite.width != 0:
                    scale_factor = (_sprite.width - 2 * overflowing_width) / _sprite.width
                    _sprite.rescale_relative_to_point((_sprite.center_x, _sprite.center_y),
                                                      scale_factor)

                # Calcul des coordonnées du sprite en cartésien --
                _sprite.center_x = constantes.TILE_WIDTH * self.map_scaling * j - overflowing_width
                _sprite.center_y = (constantes.TILE_HEIGHT * self.map_scaling * (
                        i + (count - 1) / 2)) + 1 * overflowing_height

                # Conversion en isométrique des coordonnées
                _isometric_x = (_sprite.center_x + _sprite.center_y) - (constantes.TILE_WIDTH * self.map_scaling *
                                                                        k / 2)
                _isometric_y = (-_sprite.center_x + _sprite.center_y) / 2 + (
                        constantes.TILE_HEIGHT * self.map_scaling * k / 2)

                _sprite.center_x, _sprite.center_y = _isometric_x, _isometric_y

                k += 1
                k = k % constantes.TILE_COUNT

                # On ajoute le sprite au layer (spriteList)
                layer.append(_sprite)
        layer.reverse()

    def update_walker_list(self,walker_to_render,walkersout):
        for k in walkersout:
            print("walker")
        pass

    def draw_layers(self,game):
        layers = [(self.grass_layer,game.map.grass_layer.activate),(self.roads_layer,game.map.roads_layer.activate),
                  (self.hills_layer,game.map.hills_layer.activate),(self.trees_layer,game.map.trees_layer.activate),
                  (self.buildings_layer,game.map.buildings_layer.activate)]
        for k in layers:
            if k[1]: k[0].draw()
    
    def rescale_the_map(self, new_scale,game):
        """
        There is an arcade function that might be useful: arcade.SpriteList().rescale()
        This function rescales all the sprites of a spriteList.
        But the problem is that the rendering is not correct.
        The map is deformed.
        So I did it  other way.
        Empty the map and recreate it with the right scaling.
        :param new_scale:
        :return:
        """
        self.map_scaling = new_scale
        self.setup(game)
        # self.convert_map_cartesian_to_isometric()
        pass
    
    def convert_map_cartesian_to_isometric(self):
        """"
        Convert a cartesian map to an isometric map
        """
        self.convert_layer_cartesian_to_isometric(self.grass_layer)
        self.convert_layer_cartesian_to_isometric(self.hills_layer)
        self.convert_layer_cartesian_to_isometric(self.trees_layer)
        self.convert_layer_cartesian_to_isometric(self.roads_layer)
        self.convert_layer_cartesian_to_isometric(self.buildings_layer)

    def convert_layer_cartesian_to_isometric(self, layer):
        k = 0
        for sprite in layer:
            if sprite is not None:
                cart_x, cart_y = sprite.center_x, sprite.center_y
                sprite.center_x, sprite.center_y = self.convert_cartesian_px_to_isometric_px(cart_x, cart_y, k)
                k += 1
                k = k % constantes.TILE_COUNT

    def convert_cartesian_px_to_isometric_px(self, cartesian_x, cartesian_y, offset):
        isometric_x = (cartesian_x + cartesian_y) - (constantes.TILE_WIDTH * self.map_scaling * offset / 2)
        isometric_y = (-cartesian_x + cartesian_y) / 2 + (constantes.TILE_HEIGHT * self.map_scaling * offset / 2)
        return isometric_x, isometric_y
    
    def get_map_center(self):
        center_tile = self.grass_layer[int(len(self.grass_layer) // 2 + constantes.TILE_COUNT // 2)]
        return Vec2(center_tile.center_x, center_tile.center_y)
    
    def get_sprite_at_screen_coordinates(self, pos):
        """
        Cette fonction va retourner la position logique (line, column) du sprite qui se trouve aux coordonnées x,y
        en px
        """
        self.red_sprite.center_x, self.red_sprite.center_y = pos
        (nearest_sprite, d) = arcade.get_closest_sprite(self.red_sprite, self.grass_layer)
        self.red_sprite.center_x, self.red_sprite.center_y = nearest_sprite.center_x, nearest_sprite.center_y

        index = self.grass_layer.index(nearest_sprite)

        line, column = fct.convert_sprite_list_index_to_logic_position(index)
        return line, column
