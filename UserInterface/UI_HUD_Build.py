import arcade
import pyglet.window

from Services import servicesGlobalVariables as const
from Services import servicesmMapSpriteToFile as mapping
from UserInterface import UI_Visual_Map


def hollow_build(x, y, visualmap: UI_Visual_Map.VisualMap, building=None):
    (a, b) = visualmap.get_visual_sprite((x, y))
    spritepath = None
    if building:
        spritepath = building.spritepath
        size = building.size
    else:
        # If it's not a building then it's a road
        spritepath = mapping.mapping_function(const.LAYER4, "00044")[0][0]
        size=1   
    sprite = arcade.Sprite(center_x=a, center_y=b)
    sprite.texture = arcade.load_texture(spritepath)
    sprite.scale = visualmap.map_scaling
    h= sprite.height - const.TILE_HEIGHT * visualmap.map_scaling * size
    if sprite.texture.height > const.TILE_HEIGHT*visualmap.map_scaling:
        sprite.center_y += h/2
        sprite.center_x += (size-1)*const.TILE_WIDTH/2*visualmap.map_scaling
    sprite.alpha = 180

    return sprite


def hollow(x, y, visualmap: UI_Visual_Map.VisualMap):
    # Le curseur pelle
    sprite = arcade.Sprite()
    sprite.texture = arcade.load_texture(const.SPRITE_PATH + "ColoredCursors/Shovel_150.png")
    sprite.scale = visualmap.map_scaling
    sprite.center_x = x + sprite.width/2
    sprite.center_y = y + sprite.height/2 - 2
    return sprite

