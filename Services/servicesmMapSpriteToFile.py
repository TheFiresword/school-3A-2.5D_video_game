from Services import servicesGlobalVariables as const


def mapping_function(element_type, type_version, building_level=0) -> (str, int):
    """
    Fonction de mapping version d'un élément -> chemin de fichier
    """
    if type_version in {"null", "occupied"}:
        return "", 0

    if element_type == "grass":
        if type_version == "normal":
            return const.SPRITE_PATH + "Land/Land1/Land1a_00272.png", 1
        elif type_version == "yellow":
            return const.SPRITE_PATH + "Land/Land1/Land1a_00029.png", 1
        elif type_version == "buisson":
            return const.SPRITE_PATH + "Land/Land1/Land1a_00235.png", 1
        elif int(type_version) >= 0:
            return const.SPRITE_PATH + "Land/Land1/Land1a_" + type_version + ".png", 1
        else:
            # Valeur par défaut
            return "", 0

    elif element_type == "hills":

        if type_version == "big-mountain1":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00079.png", 2
        elif type_version == "big-mountain2":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00080.png", 2
        elif type_version == "big-mountain3":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00081.png", 2
        elif type_version == "big-mountain4":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00082.png", 2

        elif type_version == "geant-mountain1":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00083.png", 3
        elif type_version == "geant-mountain2":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00084.png", 3

        elif type_version == "small-mountain1":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00071.png", 1
        elif type_version == "small-mountain2":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00072.png", 1
        elif type_version == "small-mountain3":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00073.png", 1
        elif type_version == "small-mountain4":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00074.png", 1
        elif type_version == "small-mountain5":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00075.png", 1
        elif type_version == "small-mountain6":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00076.png", 1
        elif type_version == "small-mountain7":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00077.png", 1
        elif type_version == "small-mountain8":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00078.png", 1
        else:
            return "", 0

    elif element_type == "trees":
        if type_version == "normal":
            return const.SPRITE_PATH + "Land/Land1/Arbres/Land1a_00045.png", 1
        elif int(type_version) >= 0 and type_version != "00010" and type_version != "00011":
            return const.SPRITE_PATH + "Land/Land1/Arbres/Land1a_" + type_version + ".png", 1
        else:
            return "", 0

    elif element_type == "roads":
        if type_version == "normal":
            return const.SPRITE_PATH + "Land/LandOverlay/Land2a_00093.png", 1
        elif type_version == "entry":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00089.png", 1
        elif type_version == "exit":
            return const.SPRITE_PATH + "Land/Land3/Land3a_00087.png", 1
        elif int(type_version) >= 0 and type_version < "00111":
            return const.SPRITE_PATH + "Land/LandOverlay/Land2a_" + type_version + ".png", 1
        else:
            return "", 0

    elif element_type == "buildings":
        if type_version == "dwell":
            count_digit = len(str(building_level))
            if count_digit == 1:
                return const.SPRITE_PATH + "Land/housng/Housng1a_0000"+str(building_level)+".png", 1
            if count_digit == 2:
                return const.SPRITE_PATH + "Land/housng/Housng1a_000" + str(building_level) + ".png", 1

        elif type_version == "forum":
            return const.SPRITE_PATH + "Land\Govt\Govt_00010.png"
        elif type_version == "senate":
            return const.SPRITE_PATH + "Land\Govt\Govt_00003.png"
        elif type_version == "gov_housing_house":
            return const.SPRITE_PATH + ""
        elif type_version == "gov_housing_villa":
            return const.SPRITE_PATH + ""
        elif type_version == "gov_housing_palace":
            return const.SPRITE_PATH + ""
        elif type_version == "academy":
            return const.SPRITE_PATH + ""
        elif type_version == "library":
            return const.SPRITE_PATH + ""
        elif type_version == "school":
            return const.SPRITE_PATH + ""
        elif type_version == "garden":
            return const.SPRITE_PATH + ""
        elif type_version == "plaza":
            return const.SPRITE_PATH + "Entertainment\entertainment_00105.png"
        elif type_version == "engineer's_post":
            return const.SPRITE_PATH + ""
        elif type_version == "dock":
            return const.SPRITE_PATH + ""
        elif type_version == "theatre":
            return const.SPRITE_PATH + "Entertainment\entertainment_00013.png"
        elif type_version == "amphitheatre":
            return const.SPRITE_PATH + "Entertainment\entertainment_00001.png"
        elif type_version == "colosseum":
            return const.SPRITE_PATH + ""
        elif type_version == "actor_colony":
            return const.SPRITE_PATH + "Entertainment\entertainment_00081.png"
        elif type_version == "gladiator_school":
            return const.SPRITE_PATH + "Entertainment\entertainment_00051.png"
        elif type_version == "lion_house":
            return const.SPRITE_PATH + "Entertainment\entertainment_00062.png"
        elif type_version == "barber":
            return const.SPRITE_PATH + ""
        elif type_version == "baths":
            return const.SPRITE_PATH + ""
        elif type_version == "doctor":
            return const.SPRITE_PATH + ""
        elif type_version == "hospital":
            return const.SPRITE_PATH + ""

        elif type_version == "fruit_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00023.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00024.png"
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00025.png"
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00026.png"
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00027.png"

        elif type_version == "olive_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00028.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00029.png"
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00030.png"
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00031.png"
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00032.png"
            if building_level == 5:
                return const.SPRITE_PATH + "Commerce\Commerce_00033.png"

        elif type_version == "pig_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00038.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00039.png"
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00040.png"
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00041.png"
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00042.png"

        elif type_version == "vegetable_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00019.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00020.png"
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00021.png"
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00022.png"

        elif type_version == "vine_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00033.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00034.png"
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00035.png"
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00036.png"
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00037.png"

        elif type_version == "wheat_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00013.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00014.png"
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00015.png"
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00016.png"
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00017.png"

        elif type_version == "iron_mine":
            return const.SPRITE_PATH + ""
        elif type_version == "timber_yard":
            return const.SPRITE_PATH + "Commerce\Commerce_00072.png"
        elif type_version == "marble_quarry":
            return const.SPRITE_PATH + ""
        elif type_version == "clay_pit":
            return const.SPRITE_PATH + "Commerce\Commerce_00061.png"
        elif type_version == "furniture_workshop":
            return const.SPRITE_PATH + "Commerce\Commerce_00117.png"
        elif type_version == "oil_workshop":
            return const.SPRITE_PATH + "Commerce\Commerce_00099.png"
        elif type_version == "pottery_workshop":
            return const.SPRITE_PATH + ""
        elif type_version == "weapons_workshop":
            return const.SPRITE_PATH + ""
        elif type_version == "wine_workshop":
            return const.SPRITE_PATH + ""
        elif type_version == "market":
            return const.SPRITE_PATH + "Commerce\Commerce_00001.png"
        elif type_version == "granary":
            return const.SPRITE_PATH + ""
        elif type_version == "warehouse":
            return const.SPRITE_PATH + ""
        elif type_version == "wall":
            return const.SPRITE_PATH + ""
        elif type_version == "tower":
            return const.SPRITE_PATH + ""
        elif type_version == "gatehouse":
            return const.SPRITE_PATH + ""
        elif type_version == "prefecture":
            return const.SPRITE_PATH + ""
        elif type_version == "fort":
            return const.SPRITE_PATH + ""
        elif type_version == "military_academy":
            return const.SPRITE_PATH + ""
        elif type_version == "reservoir":
            return const.SPRITE_PATH + ""
        elif type_version == "aqueduct":
            return const.SPRITE_PATH + ""
        elif type_version == "well":
            return const.SPRITE_PATH + ""
        else:
            return "", 0
