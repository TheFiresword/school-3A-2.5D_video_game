from Services import servicesGlobalVariables as const

def mapping_function(element_type, type_version, building_level=0) -> (str,int):
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
            if building_level == 0:
                return const.SPRITE_PATH + "Land/housng/Housng1a_00045.png", 1

        elif type_version == "dwelling5":
            return const.SPRITE_PATH + "Land/housng/Housng1a_00034.png", 2

        elif int(type_version) >= 0 and ("00001" <= type_version <= "00004" or "00007" <= type_version <= "00010" or
                                         "00013" <= type_version <= "00016" or "00019" <= type_version <= "00022" or
                                         "00025" <= type_version <= "00028 "
                                         or type_version in ["00045", "00049", "00050"]):
            return const.SPRITE_PATH + "Land/housng/Housng1a_" + type_version + ".png", 1

        elif int(type_version) >= 0 and ("00005" <= type_version <= "00006" or "00011" <= type_version <= "00012" or
                                         "00017" <= type_version <= "00018" or "00023" <= type_version <= "00024" or
                                         "00029" <= type_version <= "00038" or type_version == "00051"):
            return const.SPRITE_PATH + "/Land/housng/Housng1a_" + type_version + ".png", 2

        elif int(type_version) >= 0 and ("00039" <= type_version <= "00042" or type_version == "00046"):
            return const.SPRITE_PATH + "Land/housng/Housng1a_" + type_version + ".png", 3

        elif int(type_version) >= 0 and type_version in ["00043", "00044", "00047"]:
            return const.SPRITE_PATH + "Land/housng/Housng1a_" + type_version + ".png", 4

        elif int(type_version) >= 0 and type_version == "00048":
            return const.SPRITE_PATH + "Land/housng/Housng1a_" + type_version + ".png", 5

        if type_version == "wheat_farm":
            return ""
        else:
            return "", 0
