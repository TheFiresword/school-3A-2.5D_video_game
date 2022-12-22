import arcade
from Services import servicesGlobalVariables as const
from UserInterface import UI_Visual_Map 

def hollow_build(x,y,building,visualmap:UI_Visual_Map.VisualMap):
    (a,b) = visualmap.get_visual_sprite((x,y))
    size = building.size
    spritepath = building.spritepath
    sprite = arcade.Sprite(center_x = a, center_y= b)
    sprite.alpha = 180
    sprite.texture = arcade.load_texture(spritepath)
    sprite.scale = visualmap.map_scaling
    return sprite

def hollow(x,y):
    sprite = arcade.Sprite(center_x=x,center_y =y)
    sprite.texture = arcade.load_texture(const.SPRITE_PATH + "PanelsOther\paneling_00333.png")
    sprite.scale = const.SPRITE_SCALING
    return sprite



    