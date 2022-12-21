import CoreModules.MapManagement.mapManagementLayer as layer
import Services.servicesGlobalVariables as globalVar
import CoreModules.TileManagement.tileManagementElement as Element


def position_is_valid(i, j):
    return (0 <= i < globalVar.TILE_COUNT) and (0 <= j < globalVar.TILE_COUNT)


class RoadLayer(layer.Layer):
    def __init__(self):
        super().__init__(globalVar.LAYER4)
        # une variable qui sera passée à la fonction cancel_roads_serie() et qui sera remplie dans la fonction
        # add_roads_serie()
        self.original_roads = {'versions': [], 'positions': []}

    def setup(self):
        super().setup()
        self.add_entry_and_exit()

    def add_entry_and_exit(self):
        entry_road = Element.Element(self, self.type, "entry")
        exit_road = Element.Element(self, self.type, "exit")
        middle = int(globalVar.TILE_COUNT * 1 / 2)

        self.array[2 * middle - 1][middle - 1] = entry_road
        self.array[2 * middle - 1][middle - 1].id = next(self.id_iterator)
        self.array[2 * middle - 1][middle - 1].position = (2 * middle - 1, middle - 1)

        self.array[0][middle - 1] = exit_road
        self.array[0][middle - 1].id = next(self.id_iterator)
        self.array[0][middle - 1].position = (0, middle - 1)

    def set_cell(self, line, column, recursively=True, can_replace=False, memorize=False) -> bool:
        """
        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        ;                                                                                    ;;;;
        ; Redéfinition de la fonction d'ajout de route                                          ;;;;;;;;;
        ;                                                                                    ;;;;
        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        """

        if not self.changeable(line, column, 1, can_replace):
            return False

        current_version = self.array[line][column].dic['version']
        # Si la route (line, column) est la route d'entrée ou de sortie ou que la route est vide mais que ce n'est pas
        # la position de départ à laquelle on voulait ajouter on ne fait rien
        if current_version == "null" and not recursively or current_version in ["entry", "exit"]: return False

        # Initialisation des 2 variables nécéssaires
        road = None
        values = {'raw_value': -1, 'column_value': -1, 'hside': None, 'vside': None}

        if memorize:
            self.original_roads['versions'].append(self.get_cell(line, column).dic['version'])
            self.original_roads['positions'].append((line, column))

        # On appelle la fonction d'évaluation
        self.evaluate_order(line, column, values)

        if values == {'raw_value': -1, 'column_value': -1, 'hside': None, 'vside': None}:
            # ça veut dire que l'évaluation ne s'est pas faite et donc que la case actuelle est vide et est voisine de
            # la case qu'on veut ajouter
            return False

        if values['column_value'] < values['raw_value']:
            road = Element.Element(self, self.type, "00094")

        if values['column_value'] == 0 and values['raw_value'] == 1:
            # ça veut dire qu'il y a une route à gauche, 1 route à droite et une route en hauteur
            # ou grossièrement 2 routes horizontales et une verticales
            if values['vside'] == 'TOP':
                road = Element.Element(self, self.type, "00107")
            elif values['vside'] == 'BOTTOM':
                road = Element.Element(self, self.type, "00109")

        if values['column_value'] == 1 and values['raw_value'] == 1:
            # ça veut dire qu'il y a une route de chaque côté
            # ou grossierement 2 routes horizontales et 2 verticales
            road = Element.Element(self, self.type, "00110")

        if values['column_value'] == 1 and values['raw_value'] == 0:
            # ça veut dire qu'il y a une route en haut, 1 route en bas et une route de côté
            # ou grossièrement 2 routes verticales et une horizontale
            if values['hside'] == 'RIGHT':
                road = Element.Element(self, self.type, "00106")
            elif values['hside'] == 'LEFT':
                road = Element.Element(self, self.type, "00108")

        elif values['column_value'] > values['raw_value']:
            road = Element.Element(self, self.type, "normal")

        elif values['column_value'] == values['raw_value'] == 0:
            # ça veut dire qu'il y a une route verticale et une route horizontale autour
            # cette route va donc être arrondie
            if values['hside'] == 'RIGHT':
                if values['vside'] == 'TOP':
                    road = Element.Element(self, self.type, "00098")
                elif values['vside'] == 'BOTTOM':
                    road = Element.Element(self, self.type, "00097")

            elif values['hside'] == 'LEFT':
                if values['vside'] == 'TOP':
                    road = Element.Element(self, self.type, "00099")
                elif values['vside'] == 'BOTTOM':
                    road = Element.Element(self, self.type, "00100")

        self.array[line][column] = road
        self.array[line][column].id = next(self.id_iterator)
        self.array[line][column].position = (line, column)

        if recursively:
            self.set_cell(line, column - 1, can_replace=True, recursively=False, memorize=False)
            self.set_cell(line, column + 1, can_replace=True, recursively=False, memorize=False)
            self.set_cell(line-1, column,  can_replace=True, recursively=False, memorize=False)
            self.set_cell(line+1, column, can_replace=True, recursively=False, memorize=False)

        return True


    def set_cell_constrained_to_bottom_layer(self, bottom_layers_list, line, column, can_replace=False,
                                             memorize = False) -> bool:
        """
        Cette fonction insère une route dans un layer à la position (line, column)  si et seulement si les cellules
        (line, column) des layers contenus dans la liste bottom_layers_list, sont "null"
        """
        count = len(bottom_layers_list)
        for i in range(count):
            if bottom_layers_list[i].array[line][column].dic["version"] != "null":
                return False
        return self.set_cell(line, column, can_replace= can_replace, memorize=memorize, recursively=True)

    def forced_set_cell(self, line, column, road):
        # On peut forcer l'ajout d'une route précise
        if  position_is_valid(line, column):
            self.array[line][column] = road
            self.array[line][column].id = next(self.id_iterator)
            self.array[line][column].position = (line, column)
            return True
        return False

    def evaluate_order(self, line, column, values):

        left_version = right_version = top_version = bottom_version = None

        if position_is_valid(line, column - 1):
            left_version = self.array[line][column - 1].dic['version']
        if position_is_valid(line, column + 1):
            right_version = self.array[line][column + 1].dic['version']
        if position_is_valid(line + 1, column):
            top_version = self.array[line + 1][column].dic['version']
        if position_is_valid(line - 1, column):
            bottom_version = self.array[line - 1][column].dic['version']

        # Les effets de bord, cases dans les coins ou sur les bordures
        # Si c'est le premier ajout, on met une route verticale normale
        border_effects = not bottom_version and top_version == left_version == right_version == "null" or \
                         not top_version and bottom_version == left_version == right_version == "null" or \
                         \
                         not bottom_version and not left_version and top_version == right_version == "null" or \
                         not top_version and not left_version and bottom_version == right_version == "null" or \
                         not top_version and not right_version and bottom_version == left_version == "null" or \
                         not bottom_version and not right_version and top_version == left_version == "null" or \
                         \
                         not left_version and top_version == bottom_version == right_version == "null" or \
                         not right_version and top_version == bottom_version == left_version == "null"

        # s'il n'y a aucune route à côté
        no_neighboor = left_version == right_version == top_version == bottom_version == "null"

        if border_effects or no_neighboor:
            # on met une route normale
            values['column_value'] += 1
            return

        if left_version not in ["null", "entry", "exit", None]:
            values['hside'] = 'LEFT'
            if left_version == "00106":
                # on priorise l'alignement sur les intersections
                values['raw_value'] += 5
            else:
                values['raw_value'] += 1

        if right_version not in ["null", "entry", "exit", None]:
            values['hside'] = 'RIGHT'
            if left_version == "00108":
                # on priorise l'alignement sur les intersections
                values['raw_value'] += 5
            else:
                values['raw_value'] += 1

        if top_version not in ["null", "entry", "exit", None]:
            values['vside'] = 'BOTTOM'
            values['column_value'] += 1

        if bottom_version not in ["null", "entry", "exit", None]:
            values['vside'] = 'TOP'
            values['column_value'] += 1

    def reinitialize_buffer(self):
        self.original_roads['versions'].clear()
        self.original_roads['positions'].clear()

    def cancel_roads_serie(self):
        """
        cette fonction annule l'ajout d'une série de routes précédente
        original_roads est un dictionnaire contenant un tableau des routes avant l'ajout
        et un tableau de leurs positions dans l'ordre
        """
        count = 0
        for position in self.original_roads['positions']:
            self.remove_cell(position[0], position[1])
            previous_road = Element.Element(self, self.type, (self.original_roads['versions'])[count])
            assert self.forced_set_cell(position[0], position[1], previous_road), "A problem occured"
            count += 1
        self.reinitialize_buffer()

    def add_roads_serie(self, start_pos, end_pos, collision_list, memorize=False) -> bool:
        """
        Fonction qui permet d'ajouter une série de routes
        Prend en paramètre 2 couples positions d'indexes
        """

        line1, column1 = start_pos[0], start_pos[1]
        line2, column2 = end_pos[0], end_pos[1]

        # Un range pour l'ajout de la ligne verticale de routes, et un autre pour la ligne horizontale
        vrange, hrange = None, None

        # une variable qui dit si au moins une route a été ajoutée
        added = False

        if line1 >= line2:
            vrange = range(line1, line2 - 1, -1)
        else:
            vrange = range(line2, line1 - 1, -1)

        if column1 <= column2:
            hrange = range(column2, column1 - 1, -1)
        else:
            hrange = range(column1, column2 - 1, -1)

        if memorize:
            self.cancel_roads_serie()
        else:
            self.reinitialize_buffer()

        # On dessine une ligne verticale de routes de la ligne de départ jusqu'à la ligne de fin
        for i in vrange:
            if self.set_cell_constrained_to_bottom_layer(collision_list, i, column1, memorize=memorize):
                added = True

        # On dessine une ligne horizontale de routes de la colonne de départ jusqu'à celle de fin à partir de la fin de
        # la ligne de routes précédente.
        for j in hrange:
            if self.set_cell_constrained_to_bottom_layer(collision_list, line2, j, memorize=memorize):
                added = True

        if added:
            return True
        return False
