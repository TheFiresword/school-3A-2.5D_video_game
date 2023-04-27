import Services.servicesGlobalVariables as constantes
import arcade

import socket
import socketserver
from requests import get


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip


def get_free_port(ip):
    with socketserver.TCPServer((ip, 0), None) as s:
        free_port = s.server_address[1]
        return free_port


def position_is_valid(i, j):
    return (0 <= i < constantes.TILE_COUNT) and (0 <= j < constantes.TILE_COUNT)


def convert_sprite_list_index_to_logic_position(sprite_list_index):
    """
        Il faut tenir compte du fait que les spritesList sont inversées pour l'affichage et donc que l'ordre est inversé
        Par exemple, la sprite (0,0) sera la dernière dans une liste et non la première.
        """
    line = constantes.TILE_COUNT - 1 - sprite_list_index // constantes.TILE_COUNT
    column = constantes.TILE_COUNT - 1 - sprite_list_index % constantes.TILE_COUNT
    return line, column


def get_sprite_list_index(position):
    index = position[0] * 40 + position[1]
    return index


def draw_normal_cursor():
    window = arcade.get_window()
    cursor = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
    window.set_mouse_cursor(cursor)
    window.set_mouse_visible(True)


class IdIterator:
    def __init__(self):
        self.id = 0
        pass

    def __next__(self):
        id = self.id
        self.id += 1
        return id


shared_iterator = IdIterator()


def get_id():
    return next(shared_iterator)
