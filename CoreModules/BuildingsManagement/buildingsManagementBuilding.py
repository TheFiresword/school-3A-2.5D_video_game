import CoreModules.TileManagement.tileManagementElement as element
import CoreModules.MapManagement.mapManagementLayer as layer
import Services.servicesGlobalVariables as globalVar


# a macro to test if an index couple (i,j) is correct
def position_is_valid(i, j):
    return (0 <= i < globalVar.TILE_COUNT) and (0 <= j < globalVar.TILE_COUNT)


VOID_CELL_ID = -1


class BuildingLayer(layer.Layer):
    def __init__(self, _type):
        super().__init__(_type)

    def setup(self):
        # On remplit toutes les cases du layerBuilding avec des Buildings null de taille 0
        self.array = [[Building(self, self.type, 0, "null") for i in range(0, globalVar.TILE_COUNT)] for j
                      in range(0, globalVar.TILE_COUNT)]
        # On set l'id de chaque case à VOID_CELL_ID
        for i in range(0, globalVar.TILE_COUNT):
            for j in range(0, globalVar.TILE_COUNT):
                self.array[i][j].id = VOID_CELL_ID
                self.array[i][j].position = (i, j)

    def completely_fill_layer(self, version, cells_number):
        """
        Redéfinition de la méthode completely_fill_layer() de Layer pour empêcher l'utilisation de cette méthode au
        niveau d'un BuildingLayer. En effet, on ne voudra jamais complètement remplir la map avec un type de bâtiment.
        """
        pass

    def custom_fill_layer(self, config_list):
        """
        Pareil ici, c'est au joueur de remplir la map avec des bâtiments
        """
        pass

    def remove_cell(self, line, column):
        (origin_x, origin_y) = self.array[line][column].position
        origin_version = self.array[origin_x][origin_y].dic['version']
        size = self.array[origin_x][origin_y].dic['cells_number']
        if origin_version != "null":
            b = Building(self, self.type, 0, "null")
            for k in range(0, size):
                self.array[origin_x][origin_y + k] = self.array[origin_x + k][origin_y + k] = \
                    self.array[origin_x + k][origin_y] = b

                self.array[origin_x][origin_y + k].position = (origin_x, origin_y + k)
                self.array[origin_x + k][origin_y + k].position = (origin_x + k, origin_y + k)
                self.array[origin_x + k][origin_y].position = (origin_x + k, origin_y)

                self.array[origin_x][origin_y + k].id = self.array[origin_x + k][origin_y + k].id = \
                    self.array[origin_x + k][origin_y].id = VOID_CELL_ID




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
