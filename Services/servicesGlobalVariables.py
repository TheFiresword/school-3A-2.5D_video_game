import ctypes
import math
user32 = ctypes.windll.user32

DEFAULT_SCREEN_WIDTH = user32.GetSystemMetrics(0)
DEFAULT_SCREEN_HEIGHT = user32.GetSystemMetrics(1)
TITLE = "Pysar"

SPRITE_PATH = "Assets/sprites/C32/"

DEFAULT_FPS = 1 / 60

SPRITE_SCALING = 1/2
SCALE_MIN = SPRITE_SCALING/2
SCALE_MAX = 1.5 * SPRITE_SCALING
TILE_COUNT = 40


TILE_WIDTH = 58*2
TILE_HEIGHT = 29*2

LAYER1 = "grass"
LAYER2 = "hills"
LAYER3 = "trees"
LAYER4 = "roads"
LAYER5 = "buildings"

