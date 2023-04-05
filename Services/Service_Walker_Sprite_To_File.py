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
        case "Priest":
            sprite_number = 209
            up = [const.SPRITE_PATH + "Citizen1/Type3/Citizen01_{:05d}".format(sprite_number + 2 + k * 8) + ".png" for k in
                  range(0, 12)]
            left = [const.SPRITE_PATH + "Citizen1/Type3/Citizen01_{:05d}".format(sprite_number + 6 + k * 8) + ".png" for k in
                    range(0, 12)]
            down = [const.SPRITE_PATH + "Citizen1/Type3/Citizen01_{:05d}".format(sprite_number + 4 + k * 8) + ".png" for k in
                    range(0, 12)]
            right = [const.SPRITE_PATH + "Citizen1/Type3/Citizen01_{:05d}".format(sprite_number + k * 8) + ".png" for k in
                     range(0, 12)]
        case "Cart_Pusher_Wheat":
            right = [const.SPRITE_PATH + "Cart_Pusher/wheat" +'0'+str(i)+".png" for i in range(1, 10)] + \
                 [const.SPRITE_PATH + "Cart_Pusher/wheat" +str(i)+".png" for i in range(10, 13)]

            up = [const.SPRITE_PATH + "Cart_Pusher/wheat" +str(i)+".png" for i in range(13, 25)]
            down = [const.SPRITE_PATH + "Cart_Pusher/wheat" +str(i)+".png" for i in range(25, 37)]
            left = [const.SPRITE_PATH + "Cart_Pusher/wheat" +str(i)+".png" for i in range(37, 49)]

        case "Market_Trader":
            up = [const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00827.png",
                  const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00851.png",
                  const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00875.png",
                  const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00899.png"
                  ]
            left = [const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00831.png",
                    const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00855.png",
                    const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00879.png",
                    const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00903.png"
                    ]
            down = [const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00845.png",
                    const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00869.png",
                    const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00893.png",
                    const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00917.png"
                    ]
            right = [const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00841.png",
                     const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00865.png",
                     const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00889.png",
                     const.SPRITE_PATH + "Citizen1/Type9/Citizen01_00913.png"
                     ]

        case "Soldier":
            up = [const.SPRITE_PATH + "Citizen4/Type1/citizen04_00003.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00027.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00051.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00075.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00099.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00123.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00011.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00035.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00059.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00083.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00107.png",
                  const.SPRITE_PATH + "Citizen4/Type1/citizen04_00131.png",
                  ]

            right = [const.SPRITE_PATH + "Citizen4/Type1/citizen04_00001.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00025.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00049.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00073.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00041.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00097.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00009.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00033.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00057.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00081.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00105.png",#
                     const.SPRITE_PATH + "Citizen4/Type1/citizen04_00129.png"#
                     ]

            left = [const.SPRITE_PATH + "Citizen4/Type1/citizen04_00007.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00031.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00055.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00079.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00103.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00127.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00023.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00047.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00071.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00095.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00119.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00143.png"
                    ]

            down = [const.SPRITE_PATH + "Citizen4/Type1/citizen04_00005.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00029.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00053.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00077.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00101.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00125.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00021.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00045.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00029.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00069.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00093.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00029.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00117.png",
                    const.SPRITE_PATH + "Citizen4/Type1/citizen04_00141.png"
                    ]

    return up, left, down, right
