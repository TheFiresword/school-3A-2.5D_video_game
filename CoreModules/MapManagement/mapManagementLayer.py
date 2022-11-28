import Services.servicesGlobalVariables as globalVar


# Un layer va être un tableau à 2 dimensions de Sprites
# ex: [[],[]]
# Les layer possibles sont: grass, hill, tree, building
"""" 
Les valeurs de remplissage sont respectivement:
-grass: normal,yellow,buisson
-hill: normal,
-tree: normal,
LA VALEUR null SIGNIFIE QU'IL N'YA RIEN A LA POSITION CONSIDEREE
"""
class Layer:
    # Constructeur d'un layer; le _type doit être une valeur parmi "grass", "hill", "tree", "building"
    def __init__(self, _type):
        # Le tableau qui contient les sprites
        self.array = []
        # Un booléen qui dit si layer doit être affiché ou pas
        self.activate = True
        # Le type de layer; ex: pour les herbes, type="grass"
        self.type = _type

    # Fonction qui remplit layer avec un type par défaut; ex: pour grass, on peut remplir avec un type de grass
    # donné
    def automatic_fill_layer(self):
        default_version = "normal"
        # Tile(self.type, default_version)
        self.array = [[default_version for i in range(0, globalVar.TILE_COUNT)] for j in range(0, globalVar.TILE_COUNT)]

    def custom_fill_layer(self, config_list):
        # config_list est un tableau de TILE_COUNT*TILE_COUNT qui contient la version du type pour chaque tile
        self.array = config_list

    def flush_layer(self):
        self.array = [["null" for i in range(0, globalVar.TILE_COUNT)] for j in range(0, globalVar.TILE_COUNT)]

    def set_position(self, line, column, value):
        self.array[column][line] = value

