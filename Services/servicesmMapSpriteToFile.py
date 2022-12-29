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

        elif type_version == "foundation_farm":
            return const.SPRITE_PATH + "Commerce\Commerce_00012.png", 2

        elif type_version == "fruit_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00023.png", 1
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00024.png", 1
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00025.png", 1
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00026.png", 1
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00027.png", 1

        elif type_version == "olive_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00028.png", 1
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00029.png", 1
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00030.png", 1
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00031.png", 1
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00032.png", 1
            if building_level == 5:
                return const.SPRITE_PATH + "Commerce\Commerce_00033.png", 1

        elif type_version == "pig_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00038.png", 1
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00039.png", 1
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00040.png", 1
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00041.png", 1
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00042.png", 1

        elif type_version == "vegetable_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00019.png", 1
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00020.png", 1
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00021.png", 1
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00022.png", 1

        elif type_version == "vine_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00033.png", 1
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00034.png", 1
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00035.png", 1
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00036.png", 1
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00037.png", 1

        elif type_version == "wheat_farm":
            if building_level == 0:
                return const.SPRITE_PATH + "Commerce\Commerce_00013.png", 1
            if building_level == 1:
                return const.SPRITE_PATH + "Commerce\Commerce_00014.png", 1
            if building_level == 2:
                return const.SPRITE_PATH + "Commerce\Commerce_00015.png", 1
            if building_level == 3:
                return const.SPRITE_PATH + "Commerce\Commerce_00016.png", 1
            if building_level == 4:
                return const.SPRITE_PATH + "Commerce\Commerce_00017.png", 1

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

    #unknow directory manipulation
    #unKnow/Security

    elif element_type == "security":
        if type_version == "military_academy":
            return const.SPRITE_PATH + "Unknow/Security/Academie_militaire.png"
        if type_version == "barracks":
            return const.SPRITE_PATH + "Unknow/Security/Caserne.png"
        # Different aspects of a shipyard (Same picture reverted on 4 positions)
        if type_version == "shipyard":
            return const.SPRITE_PATH + "Unknow/Security/chantier_naval.png"
        if type_version == "shipyard2":
            return const.SPRITE_PATH + "Unknow/Security/chantier_naval2.png"
        if type_version == "shipyard3":
            return const.SPRITE_PATH + "Unknow/Security/chantier_naval3.png"
        if type_version == "shipyard4":
            return const.SPRITE_PATH + "Unknow/Security/chantier_naval4.png"
        if type_version == "Camp":
            return const.SPRITE_PATH + "Unknow/Security/Fort.png"
        if type_version == "Prefecture":
            return const.SPRITE_PATH + "Unknow/Security/Prefecture.png"
        # Different aspects of a guard house (Same picture reverted)
        if type_version == "guard_house": #left
            return const.SPRITE_PATH + "Unknow/Security/corp_garde.png"
        if type_version == "guard_house2": #right
            return const.SPRITE_PATH + "Unknow/Security/corp_garde2.png"

    #Unknow/EngineeringStructures
    elif element_type == "engineering_structures":
        if type_version == "engineering_studies":
            return const.SPRITE_PATH + "Unknow/EngineeringStructures/Etude_inge.png"

        if type_version == "dock": #first model of a dock (same picture reverted 4 times) (from 0 to 4)
                return const.SPRITE_PATH + "Unknow/EngineeringStructures/Quai.png"
        if type_version == "dock2":
                return const.SPRITE_PATH + "Unknow/EngineeringStructures/Quai2.png"
        if type_version == "dock3":
                return const.SPRITE_PATH + "Unknow/EngineeringStructures/Quai3.png"
        if type_version == "dock4":
                return const.SPRITE_PATH + "Unknow/EngineeringStructures/Quai4.png"

        if type_version == "dock5": #second model of a dock (same picture reverted 4 times) (from 5 to 8)
                return const.SPRITE_PATH + "Unknow/EngineeringStructures/Quai5.png"
        if type_version == "dock6":
                return const.SPRITE_PATH + "Unknow/EngineeringStructures/Quai6.png"
        if type_version == "dock7":
                return const.SPRITE_PATH + "Unknow/EngineeringStructures/Quai7.png"
        if type_version == "dock8":
                return const.SPRITE_PATH + "Unknow/EngineeringStructures/Quai8.png"

    # unKnow/Temples
    # All gods except Panthéon
    elif element_type == "temples":
        if type_version == "ceres":
            if building_level == 0:
                return const.SPRITE_PATH + "Unknow/Temples/Ceres.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Unknow/Temples/Ceres2.png"
        if type_version == "mars":
            if building_level == 0:
                return const.SPRITE_PATH + "Unknow/Temples/Mars.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Unknow/Temples/Mars2.png"
        if type_version == "mercure":
            if building_level == 0:
                return const.SPRITE_PATH + "Unknow/Temples/Mercure.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Unknow/Temples/Mercure2.png"
        if type_version == "neptune":
            if building_level == 0:
                return const.SPRITE_PATH + "Unknow/Temples/Neptune.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Unknow/Temples/Neptune2.png"
        if type_version == "venus":
            if building_level == 0:
                return const.SPRITE_PATH + "Unknow/Temples/Venus.png"
            if building_level == 1:
                return const.SPRITE_PATH + "Unknow/Temples/Venus2.png"
        if type_version == "oracle":
            return const.SPRITE_PATH + "Unknow/Temples/Oracle.png"

    # unKnow/Hygiene
    # Tout ce qui a rapport avec l'hygiene
    elif element_type == "hygiene":
        if type_version == "barber":
            return const.SPRITE_PATH + "Unknow/Hygiene/Barbier.png"
        if type_version == "hospital":
            return const.SPRITE_PATH + "Unknow/Hygiene/Hopital.png"
        if type_version == "Dispensaire":
            return const.SPRITE_PATH + "Unknow/Hygiene/Dispensaire.png"

        #first model of a thermal
        if type_version == "thermal":
            if building_level == 0:
                return const.SPRITE_PATH + "Unknow/Hygiene/thermes3.png"
            if building_level == 1: #a superior building level means that the thermal is full with water
                return const.SPRITE_PATH + "Unknow/Hygiene/thermes4.png"

        #Second model of a thermal
        if type_version == "thermal2":
            if building_level == 0 :
                return const.SPRITE_PATH + "Unknow/Hygiene/thermes.png"
            if building_level == 1 : #a superior building level means that the thermal is full with water
                return const.SPRITE_PATH + "Unknow/Hygiene/thermes2.png"
    #WaterEquipments
    elif element_type == "waterequipments":
        if type_version == "well":
            return const.SPRITE_PATH + "Unknow/WaterEquipments/puit.png"
        if type_version == "reservoir": #empty reservoir
            return const.SPRITE_PATH + "Unknow/WaterEquipments/reservoir.png"
        #reservoir filled with different movements of water
        if type_version == "reservoir1":
            return const.SPRITE_PATH + "Unknow/WaterEquipments/reservoir1.png"
        if type_version == "reservoir2":
            return const.SPRITE_PATH + "Unknow/WaterEquipments/reservoir2.png"
        if type_version == "reservoir3":
            return const.SPRITE_PATH + "Unknow/WaterEquipments/reservoir3.png"
        if type_version == "reservoir4":
            return const.SPRITE_PATH + "Unknow/WaterEquipments/reservoir4.png"
        if type_version == "reservoir5":
            return const.SPRITE_PATH + "Unknow/WaterEquipments/reservoir5.png"
        if type_version == "reservoir6":
            return const.SPRITE_PATH + "Unknow/WaterEquipments/reservoir6.png"











