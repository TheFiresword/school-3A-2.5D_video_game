from Services import servicesGlobalVariables as const


def walkers_to_sprite(type_walker):
    sprite_number = 1
    up = []
    left = []
    down = []
    right = []
    match type_walker:
        case "Engineer":
            sprite_number = 1137
            up = [const.SPRITE_PATH + "Citizen1/Type12/Citizen01_{:05d}".format(sprite_number + 2 + k * 8) + ".png" for
                  k in range(0, 12)]
            left = [const.SPRITE_PATH + "Citizen1/Type12/Citizen01_{:05d}".format(sprite_number + 6 + k * 8) + ".png"
                    for k in range(0, 12)]
            down = [const.SPRITE_PATH + "Citizen1/Type12/Citizen01_{:05d}".format(sprite_number + 4 + k * 8) + ".png"
                    for k in range(0, 12)]
            right = [const.SPRITE_PATH + "Citizen1/Type12/Citizen01_{:05d}".format(sprite_number + k * 8) + ".png" for
                     k in range(0, 12)]
        case "Prefect":
            sprite_number = 615
            up = [const.SPRITE_PATH + "Citizen2/Type6/Citizen02_{:05d}".format(sprite_number + 2 + k * 8) + ".png" for
                  k in range(0, 12)]
            left = [const.SPRITE_PATH + "Citizen2/Type6/Citizen02_{:05d}".format(sprite_number + 6 + k * 8) + ".png"
                    for k in range(0, 12)]
            down = [const.SPRITE_PATH + "Citizen2/Type6/Citizen02_{:05d}".format(sprite_number + 4 + k * 8) + ".png"
                    for k in range(0, 12)]
            right = [const.SPRITE_PATH + "Citizen2/Type6/Citizen02_{:05d}".format(sprite_number + k * 8) + ".png" for
                     k in range(0, 12)]
        case "Immigrant":
            sprite_number = 1033
            up = [const.SPRITE_PATH + "Citizen1/Type11/Citizen01_{:05d}".format(sprite_number + 2 + k * 8) + ".png" for
                  k in range(0, 12)]
            left = [const.SPRITE_PATH + "Citizen1/Type11/Citizen01_{:05d}".format(sprite_number + 6 + k * 8) + ".png"
                    for k in range(0, 12)]
            down = [const.SPRITE_PATH + "Citizen1/Type11/Citizen01_{:05d}".format(sprite_number + 4 + k * 8) + ".png"
                    for k in range(0, 12)]
            right = [const.SPRITE_PATH + "Citizen1/Type11/Citizen01_{:05d}".format(sprite_number + k * 8) + ".png" for
                     k in range(0, 12)]
        case "Citizen":
            up = [const.SPRITE_PATH + "Citizen1/Type1/Citizen01_{:05d}".format(sprite_number + 2 + k * 8) + ".png" for k in
                  range(0, 12)]
            left = [const.SPRITE_PATH + "Citizen1/Type1/Citizen01_{:05d}".format(sprite_number + 6 + k * 8) + ".png" for k in
                    range(0, 12)]
            down = [const.SPRITE_PATH + "Citizen1/Type1/Citizen01_{:05d}".format(sprite_number + 4 + k * 8) + ".png" for k in
                    range(0, 12)]
            right = [const.SPRITE_PATH + "Citizen1/Type1/Citizen01_{:05d}".format(sprite_number + k * 8) + ".png" for k in
                     range(0, 12)]

        case "Cart_Pusher_Wheat":
            right = [const.SPRITE_PATH + "Cart_Pusher/wheat" +'0'+str(i)+".png" for i in range(1, 10)] + \
                 [const.SPRITE_PATH + "Cart_Pusher/wheat" +str(i)+".png" for i in range(10, 13)]

            up = [const.SPRITE_PATH + "Cart_Pusher/wheat" +str(i)+".png" for i in range(13, 25)]
            down = [const.SPRITE_PATH + "Cart_Pusher/wheat" +str(i)+".png" for i in range(25, 37)]
            left = [const.SPRITE_PATH + "Cart_Pusher/wheat" +str(i)+".png" for i in range(37, 49)]


    return up, left, down, right
