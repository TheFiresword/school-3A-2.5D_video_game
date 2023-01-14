import Services.servicesGlobalVariables as globalVar
import Services.servicesmMapSpriteToFile as mapping
import CoreModules.MapManagement.tileManagementElement as Element
from CoreModules.BuildingsManagement.buildingsManagementBuilding import *

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

VOID_CELL_ID = -1

# an id generator
class IdIterator:
    def __init__(self):
        self.id = 0
        pass
    def __next__(self):
        id = self.id
        self.id += 1
        return  id



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
        self.id_iterator = IdIterator()
        self.current_id = None

        # Initialisation du layer; chaque case contient un Element de version null
        self.setup()

    def setup(self):
        # Initialise chaque case du layer à un Element de version null
        self.completely_fill_layer("null")

    def completely_fill_layer(self, version):
        """
        Cette fonction remplit le layer d'Elements de même type que le Layer.On set l'id de chaque Element de
        manière incrémentale
        NB: Vu qu'on remplit le layer avec le même élément ,c'est plus efficace de modifier seulement les éléments déja
        présents que d'en créer de nouveaux
        """
        # on récupère le cells_number directement depuis la fonction mapping Services
        cells_number = (mapping.mapping_function(self.type, version))[0][1]
        element_class = None
        # La classe des elements à créer: Element ou Building pour le moment
        if self.type in [globalVar.LAYER1, globalVar.LAYER2, globalVar.LAYER3, globalVar.LAYER4]:
            element_class = Element.Element
        elif self.type == globalVar.LAYER5:
            element_class = Building

        if cells_number <= 1:
            # On remplit toutes les cases du layer avec des Elements de taille 1 avec la version passée en paramètre
            self.array = [[element_class(self, self.type, version) for j in
                           range(0, globalVar.TILE_COUNT)] for i in range(0, globalVar.TILE_COUNT)]

            # On set l'id de chaque case de manière incrémentale si les éléments sont non nuls
            for i in range(0, globalVar.TILE_COUNT):
                for j in range(0, globalVar.TILE_COUNT):
                    if version == "null":
                        self.array[i][j].id = VOID_CELL_ID
                    else:
                        self.array[i][j].id = next(self.id_iterator)
                    self.array[i][j].position = (i, j)
                    self.current_id = self.array[i][j].id

        else:
            """
            Le type d'Element occupe plus d'une case
            """
            for line in range(0, globalVar.TILE_COUNT):
                for column in range(0, globalVar.TILE_COUNT):
                    self.set_cell(line, column, element_class(self, self.type, version))

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

    def remove_cell(self, line: int, column: int) -> bool:
        """
        Cette fonction enlève l'élément présent à la position (line, column) du layer auquel il appartient.
        En fait, on va remplacer l'élément présent à cette position par un élément null
        Faire attention à récupérer la position de départ d'un élément qui occupe plus d'une case
        Dans le cas où l'Element est un Building il faut pouvoir remplacer ce building par un building null
        """
        if not position_is_valid(line, column):
            return False
        id_for_search = self.array[line][column].id
        (origin_x, origin_y) = self.array[line][column].position
        origin_version = self.array[origin_x][origin_y].dic['version']
        element_class = type(self.array[origin_x][origin_y])

        # I get the indexes and then the positions of all the elements linked to the element we want to remove
        # so that we can remove all of them
        indexes_of_parts_of_the_element = []
        for i in range(globalVar.TILE_COUNT):
            indexes_of_parts_of_the_element += [(i, index) for (index, element_part) in enumerate(self.array[i]) if
                                                element_part.id == id_for_search]
        # if the elements the user wants to remove is the 'entry' signal or the 'exit' signal, then we have to stop it
        # because those elements are not removable
        if origin_version not in ["null", "entry_bottom", "entry_top", "entry_left", "entry_right", "exit_top",
                                  "exit_bottom", "exit_left", "exit_right"]:
            for part_position in indexes_of_parts_of_the_element:
                if issubclass(element_class, Building) :
                    element_class = Building
                e = element_class(self, self.type, "null")
                self.array[part_position[0]][part_position[1]] = e
                self.array[part_position[0]][part_position[1]].position = part_position
                self.array[part_position[0]][part_position[1]].id = VOID_CELL_ID
            return True
        return False

    def get_cell(self, line, column):
        if position_is_valid(line, column):
            (origin_x, origin_y) = self.array[line][column].position
            return self.array[origin_x][origin_y]
        return None

    def cell_is_non_null(self, line, column):
        return self.array[line][column].dic["version"] != "null"

    def cell_is_yellow_grass(self, line, column):
        expected_grass = self.get_cell(line, column) if self.type == globalVar.LAYER1 else None
        if expected_grass:
            return  expected_grass.dic['version'] in mapping.yellow_grass_types
        return False
    def cell_is_water(self, line, column):
        expected_water = self.get_cell(line, column) if self.type == globalVar.LAYER1 else None
        if expected_water:
            return expected_water.dic['version'] in mapping.all_water_types
        return False

    def get_cells_number(self, line, column):
        """
        The implementation of this getter is to return the number of elements in the layer that have the same id as
        the element at position (line, column)
        The benefit of this method is that it works even for elements constitued with multiple parts like farms
        """
        positions = self.get_all_positions_of_element(line, column)
        if positions:
            return len(positions)
        return 0

    def get_all_positions_of_element(self, line, column):
        """
            The benefit of this method is that it works even for elements constitued with multiple parts like farms
        """
        if position_is_valid(line, column):

            id_for_search = self.array[line][column].id

            indexes_of_parts_of_the_element = []
            for i in range(globalVar.TILE_COUNT):
                indexes_of_parts_of_the_element += [(i, index) for (index, element_part) in enumerate(self.array[i]) if
                                                    element_part.id == id_for_search]
            return indexes_of_parts_of_the_element
        return None

    def set_cell(self, line, column, element: Element, can_replace: bool = False, change_id=True,bottom_layers_list =[]) -> bool:
        """
        _dic: Un dictionnaire avec une version et un nombre de cellules
        can_replace: Un booléen qui dit si on peut remplacer une cellule existante
        Cette fonction assigne un Element à la cellule (line,column) du layer.
        Il faut que cette cellule soit vide
        Si l'attribut cells_number de l'Element > 1 alors il faut vérifier que toutes les cellules sur lesquelles il
        empiète sont vides
        """

        # Preconditions: the element has to occupy at least 1 case and the position (line, column) has to be valid
        cells_number = element.dic['cells_number']
        assert cells_number > 0
        # Precondition: the current cell cant be modified
        if not self.changeable(line, column, cells_number, can_replace):
            return False

        for i in range(0, cells_number):
            for j in range(0, cells_number):
                if (i, j) == (0, 0):
                    continue
                else:
                    for layer in bottom_layers_list:
                        if layer.type == globalVar.LAYER1:
                            status = layer.cell_is_water(line, column)
                            if status:
                                return False
                        elif layer.array[line + i][column + j].dic["version"] != "null":
                            return False

        # On copie les informations de l'Element dans la case correspondante--On garde l'id de la case
        self.array[line][column] = element
        if change_id:
            self.array[line][column].id = next(self.id_iterator)
        else:
            self.array[line][column].id = self.current_id

        self.current_id = self.array[line][column].id
        self.array[line][column].position = (line, column)

        # On met les cases supplémentaires à la version occupied
        for i in range(0, cells_number):
            for j in range(0, cells_number):
                if (i, j) == (0, 0):
                    continue
                else:
                    self.array[line + i][column + j].dic['version'] = "occupied"
                    # The id of the additionnal elements are set to the same as the first part because they are
                    # parts of the same logic element
                    self.array[line + i][column + j].id = self.array[line][column].id
                    self.array[line + i][column + j].position = (line, column)
        return True



    def set_cell_constrained_to_bottom_layer(self, bottom_layers_list, line, column, element,
                                             can_replace=False, change_id=True) -> bool:
        """
        Cette fonction insère un Element dans un layer à la position (line, column)  si et seulement si les cellules
        (line, column) des layers contenus dans la liste bottom_layers_list, sont "null"
        """
        count = len(bottom_layers_list)
        for i in range(count):
            if bottom_layers_list[i].type == globalVar.LAYER1:
                status = bottom_layers_list[i].cell_is_water(line, column)
                if status:
                    return False
            elif bottom_layers_list[i].array[line][column].dic["version"] != "null":
                return False
        return self.set_cell(line, column, element, can_replace, change_id,bottom_layers_list)

    def add_elements_serie(self, start_pos, end_pos, element, collision_list) -> (bool, int):
        """
        Fonction qui permet d'ajouter une série de buildings notamment
        Prend en paramètre 2 couples positions d'indexes
        Une liste pour vérifier les collisions
        un booléen qui permet de dire s'il faut mémoriser les buildings actuelles
        Renvoie un booléen qui dit si au moins une route a été ajoutée
        Renvoie le nombre de routes ajoutées
        """

        line1, column1 = start_pos[0], start_pos[1]
        line2, column2 = end_pos[0], end_pos[1]

        # Un range pour l'ajout de la ligne verticale de routes, et un autre pour la ligne horizontale
        vrange, hrange = None, None

        # une variable qui dit si au moins une route a été ajoutée
        added = False

        # une variable qui dit si la série de routes est valide, c'est à dire qu'il n'y a aucun obstacle entre les 2
        valid = True

        if line1 >= line2:
            vrange = range(line1, line2 - 1, -1)
        else:
            vrange = range(line2, line1 - 1, -1)

        if column1 <= column2:
            hrange = range(column2, column1 - 1, -1)
        else:
            hrange = range(column1, column2 - 1, -1)


        # a counter that will be returned as the number of roads added
        count = 0
        # On dessine une ligne verticale de routes de la ligne de départ jusqu'à la ligne de fin
        for i in vrange:
            for j in hrange:
                if self.set_cell_constrained_to_bottom_layer(collision_list, i, j, element):
                    added = True
                    count += 1
                else:
                    valid = False

        if added:
            return True, count
        return False, count

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
                    # Un bout de code pour afficher la classe exacte d'un Element
                    chaine = "".join(reversed(str(type(self.array[line][column]))))
                    start = len(chaine) - chaine.index('.') - 1
                    chaine = ("".join(reversed(chaine)))[start + 1: len(chaine) - 2]

                    print(f"{chaine} --{self.array[line][column].dic} -- {self.array[line][column].id} -- "
                          f"{self.array[line][column].position} ")
                    count += 1
        print(f"{count} elements")
    
    def parse_layer(self,action_on_element):
        for i in range(0, globalVar.TILE_COUNT):
            for j in range(0, globalVar.TILE_COUNT):
                if self.type == globalVar.LAYER5:
                    print(self.array[i][j].dic['version'])    
                    if not (self.array[i][j].dic['version'] in ["occupied", "null"]):
                        action_on_element(self.array[i][j])
        return True
                
                
            



        
        
       
