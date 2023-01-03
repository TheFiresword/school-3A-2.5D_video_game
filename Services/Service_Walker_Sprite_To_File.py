from Services import servicesGlobalVariables as const


def walkers_to_sprite(type_walker):
    citizen_number = "1"
    type_number = "1"
    sprite_number = 0
    match type_walker:
        case "Engineer":
            type_number = "2"
            sprite_number = 1
        case "Prefect":
            type_number = "3"
            sprite_number = 2

    up = [const.SPRITE_PATH + "Citizen" + citizen_number + "/Type" + type_number + "/Citizen0" +
          citizen_number + "_{:05d}".format(sprite_number * 104 + 3 + k * 8) + ".png" for k in range(0, 12)]
    left = [const.SPRITE_PATH + "Citizen" + citizen_number + "/Type" + type_number + "/Citizen0" +
            citizen_number + "_{:05d}".format(sprite_number * 104 + 7 + k * 8) + ".png" for k in range(0, 12)]
    down = [const.SPRITE_PATH + "Citizen" + citizen_number + "/Type" + type_number + "/Citizen0" +
            citizen_number + "_{:05d}".format(sprite_number * 104 + 5 + k * 8) + ".png" for k in range(0, 12)]
    right = [const.SPRITE_PATH + "Citizen" + citizen_number + "/Type" + type_number + "/Citizen0" +
             citizen_number + "_{:05d}".format(sprite_number * 104 + +1 + k * 8) + ".png" for k in range(0, 12)]

    return up, left, down, right
