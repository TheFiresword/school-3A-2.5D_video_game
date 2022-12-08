
def mapping_function(element_type, type_version) -> str:
    if type_version in {"null", "occupied"}:
        return ""

    if element_type == "grass":
        if type_version == "normal":
            return "./Assets/sprites/C3/Land/Land1/Land1a_00272.png"
        elif type_version == "yellow":
            return "./Assets/sprites/C3/Land/Land1/Land1a_00029.png"
        elif type_version == "buisson":
            return "./Assets/sprites/C3/Land/Land1/Land1a_00235.png"
        elif int(type_version) >= 0:
            return "./Assets/sprites/C3/Land/Land1/Land1a_"+type_version+".png"
        else:
            # Valeur par défaut
            return "./Assets/sprites/C3/Land/Land1/Land1a_00272.png"

    elif element_type == "hills":
        if type_version == "normal":
            return "./Assets/sprites/C3/Land/Land1/Cailloux/Land1a_00290.png"
        elif type_version == "double":
            return "./Assets/sprites/C3/Land/Land1/Cailloux/Land1a_00301.png"

        elif type_version == "big-mountain1":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00079.png"
        elif type_version == "big-mountain2":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00080.png"
        elif type_version == "big-mountain3":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00081.png"
        elif type_version == "geant-mountain1":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00082.png"
        elif type_version == "geant-mountain2":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00083.png"

        elif type_version == "small-mountain1":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00071.png"
        elif type_version == "small-mountain2":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00072.png"
        elif type_version == "small-mountain3":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00073.png"
        elif type_version == "small-mountain4":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00074.png"
        elif type_version == "small-mountain5":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00075.png"
        elif type_version == "small-mountain6":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00076.png"
        elif type_version == "small-mountain7":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00077.png"
        elif type_version == "small-mountain8":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00078.png"


        elif int(type_version) >= 0:
            return "./Assets/sprites/C3/Land/Land1/Cailloux/Land1a_"+type_version+".png"
        else:
            return "./Assets/sprites/C3/Land/Land1/Cailloux/Land1a_00290.png"

    elif element_type == "trees":
        if type_version == "normal":
            return "./Assets/sprites/C3/Land/Land1/Arbres/Land1a_00045.png"
        elif int(type_version) >= 0:
            return "./Assets/sprites/C3/Land/Land1/Arbres/Land1a_"+type_version+".png"
        else:
            return "./Assets/sprites/C3/Land/Land1/Arbres/Land1a_00045.png"

    elif element_type == "roads":
        if type_version == "normal":
            return "./Assets/sprites/C3/Land/LandOverlay/Land2a_00093.png"
        elif type_version == "entry":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00089.png"
        elif type_version == "exit":
            return "./Assets/sprites/C3/Land/Land3/Land3a_00087.png"

    elif element_type == "buildings":
        if type_version == "dwelling1":
            return "./Assets/sprites/C3/Land/housng/Housng1a_00001.png"
        elif type_version == "dwelling1":
            return "./Assets/sprites/C3/Land/housng/Housng1a_00001.png"
