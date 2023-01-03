from Services import servicesGlobalVariables as const


def walkers_to_sprite(type_walker):
    citizen_number = "1"
    type_number = "1"
    sprite_number = 0
    match type_walker:
        case "Engineer":
            citizen_number = "1"
            type_number = "12"
            sprite_number = 1137
        case "Prefect":
            citizen_number = "2"
            type_number = "6"
            sprite_number = 615

    up = [const.SPRITE_PATH + "Citizen" + citizen_number + "/Type" + type_number + "/Citizen0" +
          citizen_number + "_{:05d}".format(sprite_number + 2 + k * 8) + ".png" for k in range(0, 12)]
    left = [const.SPRITE_PATH + "Citizen" + citizen_number + "/Type" + type_number + "/Citizen0" +
            citizen_number + "_{:05d}".format(sprite_number + 6 + k * 8) + ".png" for k in range(0, 12)]
    down = [const.SPRITE_PATH + "Citizen" + citizen_number + "/Type" + type_number + "/Citizen0" +
            citizen_number + "_{:05d}".format(sprite_number + 4 + k * 8) + ".png" for k in range(0, 12)]
    right = [const.SPRITE_PATH + "Citizen" + citizen_number + "/Type" + type_number + "/Citizen0" +
             citizen_number + "_{:05d}".format(sprite_number + k * 8) + ".png" for k in range(0, 12)]

    return up, left, down, right
