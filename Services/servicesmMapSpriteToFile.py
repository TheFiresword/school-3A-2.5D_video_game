from Services import servicesGlobalVariables as const

water_types = \
    [
            ["water"+str(i) for i in range(0, 7+1)],
            ["water_top_right0", "water_top_right1", "water_top_right2", "water_top_right3"],
            ["water_top_left0", "water_top_left1", "water_top_left2", "water_top_left3"],
            ["water_bottom_left0", "water_bottom_left1", "water_bottom_left2", "water_bottom_left3"],
            ["water_bottom_right0", "water_bottom_right1", "water_bottom_right2", "water_bottom_right3"],
            ["water_top0", "water_top1", "water_top2","water_top3"],
            ["other_water"+str(i) for i in range(30)],
            ["water_barrier_line"+str(i) for i in range(2)],
            ["water_barrier_col"+str(i) for i in range(2)],
            ["water_barrier_bot_right", "water_barrier_bot_left", "water_barrier_top_right", "water_barrier_top_left"]
    ]
all_water_types = []
for i in range(len(water_types)):
    all_water_types += water_types[i]

tree_types = ["normal"]+["000"+str(i) for i in range(10, 61+1) if i < 18 or i >=30]

hill_types = \
    [
            ["small-mountain1", "small-mountain2", "small-mountain3", "small-mountain4", "small-mountain5",
             "small-mountain6", "small-mountain7", "small-mountain8"],
            ["big-mountain1", "big-mountain2", "big-mountain3"],
            ["geant-mountain1", "geant-mountain2"]
    ]

grass_types = ["0000"+str(i) for i in range(2, 10)] + ["000"+str(i) for i in range(62, 100)] + \
              ["00"+str(i) for i in range(100, 290) if i < 120 or i >= 230]

yellow_grass_types = [ "yellow"] + ["000" + str(i)for i in range(18, 30)]


water_structures_types = ["well", "fountain", "fountain1", "fountain2", "fountain3", "fountain4", "reservoir", "luxurious_bath", "normal_bath"]
farm_types = ["fruit_farm", "olive_farm", "vegetable_farm", "vine_farm", "wheat_farm", "pig_farm"]
temple_types = ["ares_temple", "mars_temple", "neptune_temple", "venus_temple", "oracle"]

sanitation_types = ["luxurious_bath", "normal_bath",
                  "fountain", "fountain2", "fountain3", "fountain4"]

def mapping_function(element_type, type_version) -> [str, int]:
    """
    Fonction de mapping version d'un élément -> chemin de fichier
    """
    if type_version in ["null", "occupied"]:
        return [("", 0)]

    if element_type == "grass":
        if type_version == "normal":
            return [(const.SPRITE_PATH + "Land/Land1/Land1a_00272.png", 1)]
        elif type_version == "yellow":
            return [(const.SPRITE_PATH + "Land/Land1/Land1a_00029.png", 1)]
        elif type_version == "buisson":
            return [(const.SPRITE_PATH + "Land/Land1/Land1a_00235.png", 1)]

        elif "water" in type_version and len(type_version) < 7:
            number = 120 + int(type_version[5:])
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00"+str(number)+".png", 1)]

        elif "other_water" in type_version:
            number = 168 + int(type_version[11:])
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00" + str(number) + ".png", 1)]


        elif type_version == "water_top_right0":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00128.png", 1)]
        elif type_version == "water_top_right1":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00129.png", 1)]
        elif type_version == "water_top_right2":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00130.png", 1)]
        elif type_version == "water_top_right3":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00131.png", 1)]

        elif type_version == "water_top_left0":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00140.png", 1)]
        elif type_version == "water_top_left1":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00141.png", 1)]
        elif type_version == "water_top_left2":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00142.png", 1)]
        elif type_version == "water_top_left3":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00143.png", 1)]

        elif type_version == "water_bottom_left0":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00136.png", 1)]
        elif type_version == "water_bottom_left1":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00137.png", 1)]
        elif type_version == "water_bottom_left2":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00138.png", 1)]
        elif type_version == "water_bottom_left3":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00139.png", 1)]

        elif type_version == "water_bottom_right0":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00132.png", 1)]
        elif type_version == "water_bottom_right1":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00133.png", 1)]
        elif type_version == "water_bottom_right2":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00134.png", 1)]
        elif type_version == "water_bottom_right3":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00135.png", 1)]

        elif type_version == "water_top0":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00162.png", 1)]
        elif type_version == "water_top1":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00163.png", 1)]
        elif type_version == "water_top2":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00164.png", 1)]
        elif type_version == "water_top3":
            return [(const.SPRITE_PATH + "Land/Land1/Eau/Land1a_00166.png", 1)]

        elif type_version == "water_barrier_line0":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00056.png", 1)]
        elif type_version == "water_barrier_line1":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00057.png", 1)]
        elif type_version == "water_barrier_col0":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00055.png", 1)]
        elif type_version == "water_barrier_col1":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00058.png", 1)]

        elif type_version == "water_barrier_top_left":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00063.png", 1)]
        elif type_version == "water_barrier_top_right":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00066.png", 1)]
        elif type_version == "water_barrier_bot_left":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00065.png", 1)]
        elif type_version == "water_barrier_bot_right":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00064.png", 1)]


        elif int(type_version) >= 0:
            return [(const.SPRITE_PATH + "Land/Land1/Land1a_" + type_version + ".png", 1)]
        else:
            # Valeur par défaut
            return [("", 0)]

    elif element_type == "hills":#ok

        if type_version == "big-mountain1":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00079.png", 2)]
        elif type_version == "big-mountain2":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00080.png", 2)]
        elif type_version == "big-mountain3":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00081.png", 2)]
        elif type_version == "big-mountain4":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00082.png", 2)]

        elif type_version == "geant-mountain1":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00083.png", 3)]
        elif type_version == "geant-mountain2":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00084.png", 3)]

        elif type_version == "small-mountain1":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00071.png", 1)]
        elif type_version == "small-mountain2":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00072.png", 1)]
        elif type_version == "small-mountain3":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00073.png", 1)]
        elif type_version == "small-mountain4":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00074.png", 1)]
        elif type_version == "small-mountain5":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00075.png", 1)]
        elif type_version == "small-mountain6":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00076.png", 1)]
        elif type_version == "small-mountain7":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00077.png", 1)]
        elif type_version == "small-mountain8":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00078.png", 1)]
        else:
            return [("", 0)]

    elif element_type == "trees":#ok
        if type_version == "normal":
            return [(const.SPRITE_PATH + "Land/Land1/Arbres/Land1a_00045.png", 1)]
        elif int(type_version) >= 0:
            return [(const.SPRITE_PATH + "Land/Land1/Arbres/Land1a_" + type_version + ".png", 1)]
        else:
            return [("", 0)]

    elif element_type == "roads":#ok
        if type_version == "normal":
            return [(const.SPRITE_PATH + "Land/LandOverlay/Land2a_00093.png", 1)]

        elif type_version == "entry_bottom":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00087.png", 1)]
        elif type_version == "entry_top":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00085.png", 1)]
        elif type_version == "entry_left":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00086.png", 1)]
        elif type_version == "entry_right":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00088.png", 1)]
        elif type_version == "exit_bottom":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00091.png", 1)]
        elif type_version == "exit_top":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00089.png", 1)]
        elif type_version == "exit_left":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00090.png", 1)]
        elif type_version == "exit_right":
            return [(const.SPRITE_PATH + "Land/Land3/land3a_00092.png", 1)]

        elif int(type_version) >= 0 and type_version < "00111":
            return [(const.SPRITE_PATH + "Land/LandOverlay/Land2a_" + type_version + ".png", 1)]
        else:
            return [("", 0)]

    elif element_type == "buildings":
        if type_version == "dwell":#ok
            my_array = []
            for level in range(7):
                count_digit = len(str(level))
                if count_digit == 1:
                    my_array.append((const.SPRITE_PATH + "Land/housng/Housng1a_0000"+str(level)+".png", 1))
                if count_digit == 2:
                    my_array.append((const.SPRITE_PATH + "Land/housng/Housng1a_000" + str(level) + ".png", 1))
            return my_array

        elif type_version == "forum":#ok
            return [(const.SPRITE_PATH + "Land/Govt/Govt_00010.png", 2)]
        elif type_version == "senate":#ok
            return [(const.SPRITE_PATH + "Land/Govt/Govt_00003.png", 3)]
        elif type_version == "gov_housing_house":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "gov_housing_villa":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "gov_housing_palace":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "academy":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "library":#ok
            return [(const.SPRITE_PATH + "Education/Education_00003.png", 2)]
        elif type_version == "school":#ok
            return [(const.SPRITE_PATH + "Education/Education_00001.png", 2)]
        elif type_version == "university":#ok
            return [(const.SPRITE_PATH + "Education/Education_00002.png", 3)]
        elif type_version == "garden":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "plaza":
            return [(const.SPRITE_PATH + "Entertainment/entertainment_00105.png", 1)]

        elif type_version == "engineer's_post":#ok
            my_array = []
            for level in range(1, 12):
                count_digit = len(str(level))
                if count_digit == 1:
                    my_array.append((const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_0000" + str(level) + ".png", 1))
                if count_digit == 2:
                    my_array.append((const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_000" + str(level) + ".png", 1))
            return my_array

        elif type_version == "quai":  # (same picture reverted 4 times) (from 0 to 4)
            return [(const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_00002.png", 2)]
        elif type_version == "quai2":
            return [(const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_00003.png", 2)]
        elif type_version == "quai3":
            return [(const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_00004.png")]
        elif type_version == "quai4":
            return [(const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_00005.png")]

        elif type_version == "dock":  # (same picture reverted 4 times) (from 5 to 8)
            return [(const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_00006.png", 3)]
        elif type_version == "dock2":
            return [(const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_00007.png", 3)]
        elif type_version == "dock3":
            return [(const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_00008.png", 3)]
        elif type_version == "dock4":
            return [(const.SPRITE_PATH + "EngineeringStructures/EngineeringStructures_00009.png", 3)]

        elif type_version == "theater":
            return [(const.SPRITE_PATH + "Entertainment/entertainment_00013.png", 2)]
        elif type_version == "amphitheater":
            return [(const.SPRITE_PATH + "Entertainment/entertainment_00001.png", 3)]
        elif type_version == "colosseum":
            return [(const.SPRITE_PATH + "Entertainment/entertainment_00036.png", 5)]
        elif type_version == "actor_colony":
            return [(const.SPRITE_PATH + "Entertainment/entertainment_00081.png", 3)]
        elif type_version == "gladiator_school":
            return [(const.SPRITE_PATH + "Entertainment/entertainment_00051.png", 3)]
        elif type_version == "lion_house":
            return [(const.SPRITE_PATH + "Entertainment/entertainment_00062.png", 3)]
        elif type_version == "barber":
            return [(const.SPRITE_PATH + "Hygiene/Hygiene_00001.png", 1)]

        #first model of a bath
        elif type_version == "normal_bath":#ok
            my_array = [(const.SPRITE_PATH + "Hygiene/Hygiene_00004.png", 2)]
            for level in range(8, 17):
                count_digit = len(str(level))
                if count_digit == 1:
                    my_array.append((const.SPRITE_PATH + "Hygiene/Hygiene_0000" + str(
                        level) + ".png", 2))
                if count_digit == 2:
                    my_array.append((const.SPRITE_PATH + "Hygiene/Hygiene_000" + str(level) + ".png", 2))
            return my_array
        #second model
        elif type_version == "luxurious_bath":#ok
            my_array = [(const.SPRITE_PATH + "Hygiene/Hygiene_00006.png", 2)]
            for level in range(18, 27):
                my_array.append((const.SPRITE_PATH + "Hygiene/Hygiene_000" + str(level) + ".png", 2))
            return my_array

        elif type_version == "hospital":#ok
            return [(const.SPRITE_PATH + "Hygiene/Hygiene_00002.png", 3)]
        if type_version == "dispensary":#ok
            return [(const.SPRITE_PATH + "Hygiene/Hygiene_00003.png", 1)]

        elif type_version == "fruit_farm":#ok
            my_array = [(const.SPRITE_PATH + "Farms/farm.png", 3)]
            for i in range(52, 75 + 1):
                my_array.append((const.SPRITE_PATH + "Farms/Commerce_000" + str(i) + ".png", 3))
            return my_array


        elif type_version == "olive_farm":#ok
            my_array = [(const.SPRITE_PATH + "Farms/farm.png", 3)]
            for i in range(76, 100):
                my_array.append((const.SPRITE_PATH + "Farms/Commerce_000" + str(i) + ".png", 3))
            my_array.append((const.SPRITE_PATH + "Farms/Commerce_00100.png", 3))
            return my_array


        elif type_version == "pig_farm":#ok
            my_array = []
            for i in range(126, 146 + 1):
                my_array.append((const.SPRITE_PATH + "Farms/Commerce_00" + str(i) + ".png", 3))
            return my_array


        elif type_version == "vegetable_farm":#ok
            my_array = [(const.SPRITE_PATH + "Farms/farm.png", 3)]
            for i in range(32, 51 + 1):
                my_array.append((const.SPRITE_PATH + "Farms/Commerce_000" + str(i) + ".png", 3))
            return my_array

        elif type_version == "vine_farm":#ok
            my_array = [(const.SPRITE_PATH + "Farms/farm.png", 3)]
            for i in range(101, 125 + 1):
                my_array.append((const.SPRITE_PATH + "Farms/Commerce_00" + str(i) + ".png", 3))
            return my_array


        elif type_version == "wheat_farm":#ok
            my_array = [(const.SPRITE_PATH + "Farms/farm.png", 3)]
            for i in range(12,31+1):
                my_array.append((const.SPRITE_PATH + "Farms/Commerce_000"+str(i)+".png", 3))
            return my_array

        elif type_version == "iron_mine":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "timber_yard":
            return [(const.SPRITE_PATH + "Commerce/Commerce_00072.png", 2)]
        elif type_version == "marble_quarry":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "clay_pit":
            return [(const.SPRITE_PATH + "Commerce/Commerce_00061.png", 2)]
        elif type_version == "furniture_workshop":
            return [(const.SPRITE_PATH + "Commerce/Commerce_00117.png", 2)]
        elif type_version == "oil_workshop":
            return [(const.SPRITE_PATH + "Commerce/Commerce_00099.png", 2)]
        elif type_version == "pottery_workshop":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "weapons_workshop":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "wine_workshop":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "market":
            return [(const.SPRITE_PATH + "Commerce/Commerce_00001.png", 2)]

        elif type_version == "granary":#ok
            my_array = []
            for level in range(141, 150):
                if level != 142:
                    my_array.append((const.SPRITE_PATH + "Commerce/Commerce_00"+str(level)+".png", 3))
            return my_array

        elif type_version == "warehouse":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "wall":
            return [(const.SPRITE_PATH + "", 0)]
        elif type_version == "tower":
            return [(const.SPRITE_PATH + "", 0)]

        # Different aspects of a gatehouse (Same picture reverted)
        elif type_version == "gatehouse_left":
            return [(const.SPRITE_PATH + "Land/LandOverlay/Land2a_00150.png", 2)]
        elif type_version == "gatehouse_right":
            return [(const.SPRITE_PATH + "Land/LandOverlay/Land2a_00151.png", 2)]

        elif type_version == "prefecture":#ok
            my_array = [(const.SPRITE_PATH + "Security/Security_00001.png", 1)]
            for level in range(2, 10):
                my_array.append((const.SPRITE_PATH + "Security/Security_0000" + str(level) + ".png", 1))
            my_array.append((const.SPRITE_PATH + "Security/Security_00010" + ".png", 1))
            my_array.append((const.SPRITE_PATH + "Security/Security_00011" + ".png", 1))
            return my_array

        elif type_version == "fort":
            return [(const.SPRITE_PATH + "Security/Security_00003.png", 3)]
        elif type_version == "military_academy":
            return [(const.SPRITE_PATH + "Security/Security_00020.png", 3)]

        elif type_version == "reservoir":#ok
            return [(const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00002.png", 3),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00003.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00004.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00005.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00006.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00007.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00008.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00009.png", 1)]


        #First type of fountain
        elif type_version == "fountain":#ok
            return [(const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00011.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00012.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00013.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00014.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00015.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00016.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00017.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00018.png", 1)]

        # Second type of fountain
        elif type_version == "fountain2":  #ok
            return [(const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00019.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00020.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00021.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00022.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00023.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00024.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00025.png", 1)]

        # Third type of fountain
        elif type_version == "fountain3":  #ok
            return [(const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00027.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00028.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00029.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00030.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00031.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00032.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00033.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00034.png", 1)]

        # Fourth type of fountain
        elif type_version == "fountain4":  # ok
            return [(const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00035.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00036.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00037.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00038.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00039.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00040.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00041.png", 1),
                    (const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00042.png", 1)]

        elif type_version == "aqueduct":
            return [(const.SPRITE_PATH + "", 1)]
        elif type_version == "well":#ok
            return [(const.SPRITE_PATH + "WaterEquipments/WaterEquipments_00001.png", 1)]
        elif type_version == "barracks":
            return [(const.SPRITE_PATH + "Security/Security_00010.png", 3)]

        # Different aspects of a shipyard (Same picture reverted on 4 positions)
        elif type_version == "shipyard":
            return [(const.SPRITE_PATH + "Security/Security_00006.png", 2)]
        elif type_version == "shipyard2":
            return [(const.SPRITE_PATH + "Security/Security_00007.png", 2)]
        elif type_version == "shipyard3":
            return [(const.SPRITE_PATH + "Security/Security_00008.png", 2)]
        elif type_version == "shipyard4":
            return [(const.SPRITE_PATH + "Security/Security_00009.png", 2)]

        #Temples of gods
        elif type_version == "ares_temple":#ok
            return [(const.SPRITE_PATH + "Temples/Temples_00001.png", 2)]

        elif type_version == "mars_temple":#ok
            return [(const.SPRITE_PATH + "Temples/Temples_00003.png", 2)]

        elif type_version == "mercury_temple":#ok
            return [(const.SPRITE_PATH + "Temples/Temples_00005.png", 2)]

        elif type_version == "neptune_temple":#ok
            return [(const.SPRITE_PATH + "Temples/Temples_00007.png", 2)]

        elif type_version == "venus_temple":#ok
            return [(const.SPRITE_PATH + "Temples/Temples_00009.png", 2)]

        elif type_version == "oracle":#ok
            return [(const.SPRITE_PATH + "Temples/Temples_00011.png", 2)]


def get_structures_range(element_type, type_version) -> int:
    if element_type != "buildings":
        return 0
    else:
        if type_version == "well":
            return 2
        if type_version in sanitation_types:
            return 4
        if type_version == "reservoir":
            return 10
