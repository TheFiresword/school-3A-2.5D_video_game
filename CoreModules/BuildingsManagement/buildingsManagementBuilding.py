import CoreModules.TileManagement.tileManagementElement as element


class Building(element.Element):
    def __init__(self, buildings_layer, _type, version="normal"):
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
    def __init__(self, buildings_layer, _type, version="dwelling1"):
        super().__init__(buildings_layer, _type, version)
        self.current_population = None
        self.max_population = None




