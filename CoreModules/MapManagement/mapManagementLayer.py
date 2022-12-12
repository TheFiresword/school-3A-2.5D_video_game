import Services.servicesGlobalVariables as globalVar
import CoreModules.TileManagement.tileManagementElement as Element

# PROBLEME Les lignes et les colonnes sont inversées je ne sais pas pourquoi
"""
++++Un layer va être un tableau à 2 dimensions d'Elements
Exemple: 
|__|__|__|__|
|__|__|__|__|
|__|__|__|__|
|__|__|__|__|
NB: Logiquement la cellule (0,0) est la cellule en haut à gauche, mais on veut qu'elle soit en bas à gauche
Chaque case contient un Element, instance de la classe Element

++++Lorsque cells_number>1 ie que l'Element occupe plus d'une case, on considère que la cellule courante contient le 
coin inférieur gauche de l'Element.
Ensuite, dans les cellules supplémentaires que l'Element occupe, on met un Element dont l'attribut dic vaut
{version:"occupied", cells_number:1} et qui a le même id que l'Element initial
Il faut vérifier en amont que ces cellules supplémentaires ne sont pas déja occupées.
Le cas échéant, on annule l'insertion de l'Element

++++Les layers possibles sont: grass, hill, tree et building
Les versions de remplissage sont respectivement:
-grass: normal,yellow,buisson ou le numéro d'image associé (ex: 00300)
-hill: normal, double ou le numéro d'image associé (ex: 00300)
-tree: normal ou le numéro d'image associé (ex: 00300)
"""


# a macro to test if an index couple (i,j) is correct
def position_is_valid(i, j):
    return (0 <= i < globalVar.TILE_COUNT) and (0 <= j < globalVar.TILE_COUNT)


MAX_NUMBER_ID = 1000000
VOID_CELL_ID = -1


# an id generator


def get_available_id():
    start = 0
    while start < MAX_NUMBER_ID:
        yield start
        start += 1


class Layer:

    # Constructeur d'un layer; le _type doit être une valeur parmi "grass", "hill", "tree", "building"
    def __init__(self, _type):
        # Le tableau qui contient les Elements
        self.array = []

        # Un booléen qui dit si layer doit être affiché ou pas
        self.activate = True

        # Le type de layer; ex: pour les herbes, type="grass"
        self.type = _type

        # Un générateur d'id
        self.id_iterator = get_available_id()

        # Initialisation du layer; chaque case contient un Element de version null
        self.setup()

    def setup(self):
        # Initialise chaque case du layer à un Element de version null
        self.completely_fill_layer("null", 0)

    def completely_fill_layer(self, version, cells_number):
        """
        Cette fonction remplit le layer d'Elements de même type que le Layer.On set l'id de chaque Element de
        manière incrémentale
        """
        if cells_number <= 1:
            # On remplit toutes les cases du layer avec des Elements de taille 1 avec la version passée en paramètre
            self.array = [[Element.Element(self, self.type, cells_number, version) for j in
                           range(0, globalVar.TILE_COUNT)] for i in range(0, globalVar.TILE_COUNT)]

            # On set l'id de chaque case de manière incrémentale si les éléments sont non nuls
            for i in range(0, globalVar.TILE_COUNT):
                for j in range(0, globalVar.TILE_COUNT):
                    if version == "null":
                        self.array[i][j].id = VOID_CELL_ID
                    else:
                        self.array[i][j].id = next(self.id_iterator)
                    self.array[i][j].position = (i, j)

        else:
            """
            Le type d'Element occupe plus d'une case
            """
            for line in range(0, globalVar.TILE_COUNT):
                for column in range(0, globalVar.TILE_COUNT):
                    self.set_cell(line, column, Element.Element(self, self.type, cells_number, version), False)

    def custom_fill_layer(self, config_list):
        """
        A modifier en fonction de position
        """
        # config_list est un tableau de TILE_COUNT*TILE_COUNT Elements
        # Peut être long à écrire
        # Pour l'instant cette fonction n'est jamais appelée
        for i in range(0, len(self.array)):
            del self.array[i]
        self.array = config_list

    def flush_layer(self):
        """
        Cette fonction vide le layer; ie qu'il set chaque Element du layer à une version "null"
        """
        # self.array = [["null" for i in range(0, globalVar.TILE_COUNT)] for j in range(0, globalVar.TILE_COUNT)]
        for i in range(0, globalVar.TILE_COUNT):
            for j in range(0, globalVar.TILE_COUNT):
                self.remove_cell(i, j)

    def remove_cell(self, line, column):
        (origin_x, origin_y) = self.array[line][column].position
        origin_version = self.array[origin_x][origin_y].dic['version']
        size = self.array[origin_x][origin_y].dic['cells_number']
        if origin_version != "null":
            for i in range(0, size):
                for j in range(0, size):
                    e = Element.Element(self, self.type, 0, "null")
                    self.array[origin_x + i][origin_y + j] = e
                    self.array[origin_x + i][origin_y + j].position = (origin_x + i, origin_y + j)
                    self.array[origin_x + i][origin_y + j].id = VOID_CELL_ID

    def set_cell(self, line, column, element, can_replace=False) -> bool:
        """
        _dic: Un dictionnaire avec une version et un nombre de cellules
        can_replace: Un booléen qui dit si on peut remplacer une cellule existante
        Cette fonction assigne un Element à la cellule (line,column) du layer.
        Il faut que cette cellule soit vide
        Si l'attribut cells_number de l'Element > 1 alors il faut vérifier que toutes les cellules sur lesquelles il
        empiète sont vides
        """
        # Pré-conditions: La position doit être valide et la case doit contenir un Element de version "null" si can't
        # replace

        cells_number = element.dic['cells_number']
        assert cells_number > 0
        if not self.changeable(line, column, cells_number, can_replace):
            return False

        # Toutes les conditions sont remplies
        # On copie les informations de l'Element dans la case correspondante--On garde l'id de la case
        self.array[line][column] = element
        self.array[line][column].id = next(self.id_iterator)
        self.array[line][column].position = (line, column)

        # On met les cases supplémentaires à la version occupied
        for i in range(0, cells_number):
            for j in range(0, cells_number):
                if (i, j) == (0, 0):
                    continue
                else:
                    self.array[line + i][column + j].dic['version'] = "occupied"
                    # Les id des cellules supplémentaires sont set à l'id de l'Element ajouté
                    self.array[line + i][column + j].id = self.array[line][column].id
                    self.array[line + i][column + j].position = (line, column)
        return True

    def set_cell_constrained_to_bottom_layer(self, bottom_layers_list, line, column, element,
                                             can_replace=False) -> bool:
        """
        Cette fonction insère un Element dans un layer à la position (line, column)  si et seulement si les cellules
        (line, column) des layers contenus dans la liste bottom_layers_list, sont "null"
        """
        count = len(bottom_layers_list)
        for i in range(0, count):
            if bottom_layers_list[i].array[line][column].dic["version"] != "null":
                return False
        return self.set_cell(line, column, element, can_replace)

    def changeable(self, line, column, cells_number, can_replace):
        """
        Cette fonction permet de rajouter les conditions version!="null" dans la fonction set_cell uniquement quand
        can_replace vaut False
        """
        valid_positions = all(
            [position_is_valid(line + i, column + j) for j in range(0, cells_number) for i in
             range(0, cells_number)]
        )
        if valid_positions and can_replace:
            return True
        else:
            return valid_positions and all(
                [self.array[line + i][column + j].dic['version'] == "null" for j in range(0, cells_number) for i in
                 range(0, cells_number)]
            )

    def print_content(self, cells_number=int(pow(globalVar.TILE_COUNT, 2))):
        """
        Fonction d'aide au debogage qui affiche le contenu de chaque layer
        """
        i = int(cells_number / globalVar.TILE_COUNT)
        j = int(cells_number % globalVar.TILE_COUNT)

        for line in range(0, globalVar.TILE_COUNT):
            for column in range(0, globalVar.TILE_COUNT):
                if (line, column) == (i, j): return
                print(f"{self.array[line][column].dic} -- {self.array[line][column].id} -- "
                      f"{self.array[line][column].position} ")

    def print_currents_elements(self):
        count = 0
        for line in range(0, globalVar.TILE_COUNT):
            for column in range(0, globalVar.TILE_COUNT):
                if self.array[line][column].dic['version'] != "null" and \
                        self.array[line][column].dic['version'] != "occupied":
                    print(f"{self.array[line][column].dic} -- {self.array[line][column].id} -- "
                          f"{self.array[line][column].position} ")
                    count += 1
        print(f"{count} elements")
