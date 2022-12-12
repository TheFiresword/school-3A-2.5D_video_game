
class Building_info():

    def __init__(self,cost,size,employs,sprite,road_dependency,water_dependency):
        self.cost = cost
        self.size = size
        self.employs = employs
        self.spritepath = sprite
        self.road_dependency = road_dependency
        self.water_dependency = water_dependency
        pass

#Some data are not accurate, only copy paste name and fill some building
building_dico = {
        "Forum" : Building_info(75,4,6,"",False,False),
        "Senate" : Building_info(400,20,30,"",False,False),
        "Gov Housing house" : Building_info(150,-1,0,"",False,False),
        "Gov Housing villa" : Building_info(400,-1,0,"",False,False),
        "Gov Housing palace" : Building_info(700,-1,0,"",False,False),
        "Academy" : Building_info(100,-1,30,"",False,False),
        "Library" : Building_info(75,-1,20,"",False,False),
        "School" : Building_info(50,-1,10,"",False,False),
        "Garden" : Building_info(12,-1,0,"",False,False),
        "Plaza" : Building_info(15,-1,0,"",False,False),
        "Engineer's Post" : Building_info(30,1,6,"",False,False),
        "Dock" : Building_info(100,-1,12,"",False,False),
        "Theatre" : Building_info(50,-1,8,"",False,False),
        "Amphitheatre" : Building_info(100,-1,12,"",False,False),
        "Colosseum" : Building_info(500,-1,25,"",False,False),
        "Actor Colony" : Building_info(50,-1,5,"",False,False),
        "Gladiator School" : Building_info(75,-1,8,"",False,False),
        "Lion House" : Building_info(75,-1,8,"",False,False),
        "Barber" : Building_info(25,-1,2,"",True,False),
        "Baths" : Building_info(50,-1,10,"",False,True),
        "Doctor" : Building_info(30,-1,5,"",True,False),
        "Hospital" : Building_info(300,-1,30,"",True,False),
        "Fruit Farm" : Building_info(40,-1,10,"",True,False),
        "Olive Farm" : Building_info(40,-1,10,"",True,False),
        "Pig Farm" : Building_info(40,-1,10,"",True,False),
        "Vegetable Farm" : Building_info(40,-1,10,"",True,False),
        "Vine Farm" : Building_info(40,-1,10,"",True,False),
        "Wheat Farm" : Building_info(40,-1,10,"",True,False),
        "Iron Mine" : Building_info(40,-1,10,"",True,False),
        "Timber Yard" : Building_info(40,-1,10,"",True,False),
        "Marble Quarry" : Building_info(40,-1,10,"",True,False),
        "Clay Pit" : Building_info(40,-1,10,"",True,False),
        "Furniture Workshop" : Building_info(40,-1,10,"",True,False),
        "Oil Workshop" : Building_info(40,-1,10,"",True,False),
        "Pottery Workshop" : Building_info(40,-1,10,"",True,False),
        "Weapons Workshop" : Building_info(40,-1,10,"",True,False),
        "Wine Workshop" : Building_info(40,-1,10,"",True,False),
        "Market" : Building_info(40,-1,10,"",True,False),
        "Granary" : Building_info(40,-1,10,"",True,False),
        "Warehouse" : Building_info(40,-1,10,"",True,False),
        "Wall" : Building_info(40,-1,10,"",True,False),
        "Tower" : Building_info(40,-1,10,"",True,False),
        "Gatehouse" : Building_info(40,-1,10,"",True,False),
        "Prefecture" : Building_info(40,-1,10,"",True,False),
        "Fort" : Building_info(40,-1,10,"",True,False),
        "Military Academy" : Building_info(40,-1,10,"",True,False),
        "Reservoir" : Building_info(40,-1,10,"",True,False),
        "Aqueduct" : Building_info(40,-1,10,"",True,False),
        "Well" : Building_info(40,-1,10,"",True,False),
        "Dwell" : Building_info(0,1,0,".\Assets\sprites\C3\Land\housng\Housng1a_00001.png",False,False)
    }