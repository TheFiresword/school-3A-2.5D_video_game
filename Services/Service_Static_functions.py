import Services.servicesGlobalVariables as constantes

def convert_sprite_list_index_to_logic_position(sprite_list_index):
        """
        Il faut tenir compte du fait que les spritesList sont inversées pour l'affichage et donc que l'ordre est inversé
        Par exemple, la sprite (0,0) sera la dernière dans une liste et non la première.
        """
        line = constantes.TILE_COUNT - 1 - sprite_list_index // constantes.TILE_COUNT
        column = constantes.TILE_COUNT - 1 - sprite_list_index % constantes.TILE_COUNT
        return line, column