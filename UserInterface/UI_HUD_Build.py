import arcade
import pyglet.window

from Services import servicesGlobalVariables as const
from UserInterface import UI_Visual_Map


def hollow_build(x, y, building, visualmap: UI_Visual_Map.VisualMap):
    (a, b) = visualmap.get_visual_sprite((x, y))
    size = building.size
    spritepath = building.spritepath
    sprite = arcade.Sprite(center_x=a, center_y=b)
    sprite.alpha = 180
    sprite.texture = arcade.load_texture(spritepath)
    sprite.scale = visualmap.map_scaling
    return sprite


def hollow(x, y, visualmap: UI_Visual_Map.VisualMap):
    # Le curseur pelle
    sprite = arcade.Sprite()
    sprite.texture = arcade.load_texture(const.SPRITE_PATH + "ColoredCursors\Shovel_150.png")
    sprite.scale = visualmap.map_scaling
    sprite.center_x = x + sprite.width/2
    sprite.center_y = y + sprite.height/2 - 2
    return sprite

