import CoreModules.TileManagement.tileManagementElement as element
import CoreModules.MapManagement.mapManagementLayer as layer
import Services.servicesGlobalVariables as globalVar


# a macro to test if an index couple (i,j) is correct
def position_is_valid(i, j):
    return (0 <= i < globalVar.TILE_COUNT) and (0 <= j < globalVar.TILE_COUNT)


class BuildingLayer(layer.Layer):
    def __init__(self, _type):
        super().__init__(_type)

    def setup(self):
        # On remplit toutes les cases du layerBuilding avec des Buildings null de taille 1
        self.array = [[Building(self, self.type, 1, "null") for i in range(0, globalVar.TILE_COUNT)] for j
                      in range(0, globalVar.TILE_COUNT)]
        # Incrémenteur d'id
        count = 0
        # On set l'id de chaque case de manière incrémentale
        for i in range(0, globalVar.TILE_COUNT):
            for j in range(0, globalVar.TILE_COUNT):
                self.array[i][j].id = count
                self.array[i][j].position = (i, j)
                count += 1
        self.last_id = self.array[globalVar.TILE_COUNT - 1][globalVar.TILE_COUNT - 1].id

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

    def set_cell(self, column, line, building, can_replace=False) -> bool:
        """
                building: Un building
                can_replace: Un booléen qui dit si on peut remplacer une cellule existante
                Cette fonction assigne un Element à la cellule (line,column) du layer.
                Il faut que cette cellule soit vide
                Si l'attribut cells_number de l'Element > 1 alors il faut vérifier que toutes les cellules sur lesquelles il
                empiète sont vides
                """
        # Pré-conditions: La position doit être valide et la case doit contenir un Element de version "null" si can't
        # replace
        if not position_is_valid(line, column) or self.changeable(line, column, 0, can_replace):
            return False
        else:

            cells_number = building.dic['cells_number']
            if cells_number == 1:
                building.id = self.array[line][column].id
                building.position = (line, column)
                self.array[line][column] = building
                return True

            # Si le building occupe plus d'1 case, on vérifie que les cases supplémentaires existent et sont vides
            else:
                for k in range(1, cells_number):
                    if not position_is_valid(line, column + k) or \
                            not position_is_valid(line + k, column + k) or \
                            not position_is_valid(line + k, column) or self.changeable(line, column, k, can_replace):
                        return False

                # Toutes les conditions sont remplies
                # On copie les informations du building dans la case correspondante--On garde l'id de la case
                building.id = self.array[line][column].id
                building.position = (line, column)
                self.array[line][column] = building

                # On met les cases supplémentaires à la version occupied
                for k in range(1, cells_number):
                    self.array[line][column+k] = building

                    self.array[line+k][column+k] = building

                    self.array[line+k][column] = building

                    # Les id des cellules supplémentaires sont set à l'id du building ajouté
                    self.array[line][column + k].id = self.array[line + k][column + k].id = self.array[line + k][
                        column].id \
                        = self.array[line][column].id

                    # Les positions des cellules supplémentaires sont set à la position  du building ajouté
                    self.array[line][column + k].position = self.array[line + k][column + k].position = \
                        self.array[line + k][column].position = self.array[line][column].position
        return True


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
    def __init__(self, buildings_layer,  _type, size, init_population, max_population, version="dwelling1"):
        super().__init__(buildings_layer, _type, size, version)
        self.current_population = init_population
        self.max_population = max_population
