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


class Layer:

    # Constructeur d'un layer; le _type doit être une valeur parmi "grass", "hill", "tree", "building"
    def __init__(self, _type):
        # Le tableau qui contient les Elements
        self.array = []

        # Un booléen qui dit si layer doit être affiché ou pas
        self.activate = True

        # Le type de layer; ex: pour les herbes, type="grass"
        self.type = _type

        # Le dernier id qui a été utilisé pour pouvoir incrémenter cet id quand on ajoute un nouvel Element
        self.last_id = 0

        # Initialisation du layer; chaque case contient un Element de version null
        self.setup()

    def setup(self):
        # Initialise chaque case du layer à un Element de version null
        self.completely_fill_layer("null", 1)

    def completely_fill_layer(self, version, cells_number):
        """
        Cette fonction remplit le layer d'Elements de même type que le Layer.On set l'id de chaque Element de
        manière incrémentale
        """
        if cells_number == 1:
            # On remplit toutes les cases du layer avec des Elements de taille 1 avec la version passée en paramètre
            self.array = [[Element.Element(self, self.type, 1, version) for i in range(0, globalVar.TILE_COUNT)] for j
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

        else:
            """
            Le type d'Element occupe plus d'une case
            Si cette condition est atteinte, c'est que le layer a été précédemment rempli au moins via setup()
            L'importance de cette information est qu'on a plus besoin de set des id de manière incrémentale
            La fonction set_cell() s'occupe d'ajouter un par un les éléments
            """

            for line in range(0, globalVar.TILE_COUNT):
                for column in range(0, globalVar.TILE_COUNT):
                    status = self.set_cell(line, column, {"version": version, "cells_number": cells_number}, False)
                    if status: self.last_id = self.array[line][column].id

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
                if self.array[i][j]:
                    self.array[i][j].dic = {"version": "null", "cells_number": 1}

    def set_cell(self, column, line, _dic, can_replace=False) -> bool:
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
        if not position_is_valid(line, column) or self.changeable(line, column, 0, can_replace):
            return False
        else:

            cells_number = _dic['cells_number']
            if cells_number == 1:
                self.array[line][column].dic = _dic
                return True

            # Si l'Element occupe plus d'1 case, on vérifie que les cases supplémentaires existent et sont vides
            else:
                for k in range(1, cells_number):
                    if not position_is_valid(line, column + k) or \
                            not position_is_valid(line + k, column + k) or \
                            not position_is_valid(line + k, column) or self.changeable(line, column, k, can_replace):
                        return False

                # Toutes les conditions sont remplies
                # On copie les informations de l'Element dans la case correspondante--On garde l'id de la case
                self.array[line][column].dic = _dic

                # On met les cases supplémentaires à la version occupied
                for k in range(1, cells_number):
                    self.array[line][column + k].dic = {"version": "occupied", "cells_number": 0}
                    self.array[line + k][column + k].dic = {"version": "occupied", "cells_number": 0}
                    self.array[line + k][column].dic = {"version": "occupied", "cells_number": 0}

                    # Les id des cellules supplémentaires sont set à l'id de l'Element ajouté
                    self.array[line][column + k].id = self.array[line + k][column + k].id = self.array[line + k][
                        column].id \
                        = self.array[line][column].id
        return True

    def set_cell_constrained_to_bottom_layer(self, bottom_layers_list, column, line, _dic, can_replace=False) -> bool:
        """
        Cette fonction insère un Element dans un layer à la position (line, column)  si et seulement si les cellules
        (line, column) des layers contenus dans la liste bottom_layers_list, sont "null"
        """
        count = len(bottom_layers_list)
        for i in range(0, count):
            if bottom_layers_list[i].array[line][column].dic["version"] != "null":
                return False
        return self.set_cell(column, line, _dic, can_replace)

    def changeable(self, line, column, k, can_replace):
        """
        Cette fonction permet de rajouter les conditions version!="null" dans la fonction set_cell uniquement quand
        can_replace vaut False
        """
        if can_replace:
            return False
        else:
            return self.array[line][column + k].dic['version'] != "null" or \
                   self.array[line + k][column + k].dic['version'] != "null" or \
                   self.array[line + k][column].dic['version'] != "null"

    def print_content(self):
        """
        Fonction d'aide au debogage qui affiche le contenu de chaque layer
        """
        for line in range(0, globalVar.TILE_COUNT):
            for column in range(0, globalVar.TILE_COUNT):
                print(self.array[line][column].dic, end=" | ")
            print("\n")

    def get_last_id(self):
        print(self.last_id)
