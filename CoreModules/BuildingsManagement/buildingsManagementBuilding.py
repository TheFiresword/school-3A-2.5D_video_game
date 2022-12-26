import CoreModules.TileManagement.tileManagementElement as element


class Building(element.Element):
    def __init__(self, buildings_layer, _type, version="dwell"):
        super().__init__(buildings_layer, _type, version)
        self.fire_level = 0
        self.structure_level = 0
        self.isBurnt = False
        self.isDestroyed = False

    def setIsBurnt(self, isBurnt):
        self.isBurnt = isBurnt

    def setIsDestroyed(self, isDestroyed):
        self.isDestroyed = isDestroyed


class Dwelling(Building):
    def __init__(self, buildings_layer, _type):
        super().__init__(buildings_layer, _type, "dwell")
        self.current_population = None
        self.max_population = None

class Farm(Building):
    def __init__(self, buildings_layer, _type, production="wheat_farm"):
        foundation = super().__init__(buildings_layer, _type, "foundation_farm")
        farm_at_00 = super().__init__(buildings_layer, _type, production)
        farm_at_01 = super().__init__(buildings_layer, _type, production)
        farm_at_02 = super().__init__(buildings_layer, _type, production)
        farm_at_12 = super().__init__(buildings_layer, _type, production)
        farm_at_22 = super().__init__(buildings_layer, _type, production)


