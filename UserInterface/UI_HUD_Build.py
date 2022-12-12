import arcade
from Services import servicesGlobalVariables as const

def hollow_build(x,y,building):
    size = building.size
    spritepath = building.spritepath
    sprite = arcade.Sprite(center_x = x, center_y= y)
    sprite.alpha = 180
    sprite.texture = arcade.load_texture(spritepath)
    return sprite



    