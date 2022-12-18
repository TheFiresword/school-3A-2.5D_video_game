import CoreModules.TileManagement.tileManagementElement as element


class Building(element.Element):
    def __init__(self, buildings_layer, _type, size, version="normal"):
        super().__init__(buildings_layer, _type, size, version)
        self.fire_level = 0
        self.structure_level = 0
        self.isBurnt = False
        self.isDestroyed = False

    def setIsBurnt(self, isBurnt):
        self.isBurnt = isBurnt

    def setIsDestroyed(self, isDestroyed):
        self.isDestroyed = isDestroyed


class Dwelling(Building):
    def __init__(self, buildings_layer, _type, size, init_population, max_population, version="dwelling1"):
        super().__init__(buildings_layer, _type, size, version)
        self.current_population = init_population
        self.max_population = max_population




