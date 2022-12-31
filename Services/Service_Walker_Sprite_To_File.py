from Services import servicesGlobalVariables as const


def walkers_to_sprite():
    up = [const.SPRITE_PATH + "Citizen1/Type1/Citizen01_{:05d}".format(3 + k * 8) + ".png" for k in range(0, 12)]
    left = [const.SPRITE_PATH + "Citizen1/Type1/Citizen01_{:05d}".format(7 + k * 8) + ".png" for k in range(0, 12)]
    down = [const.SPRITE_PATH + "Citizen1/Type1/Citizen01_{:05d}".format(5 + k * 8) + ".png" for k in range(0, 12)]
    right = [const.SPRITE_PATH + "Citizen1/Type1/Citizen01_{:05d}".format(1 + k * 8) + ".png" for k in range(0, 12)]

    return (up, left, down, right)
