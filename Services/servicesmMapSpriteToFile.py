
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



