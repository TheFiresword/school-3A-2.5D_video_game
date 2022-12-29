    def add_multiple_dwell(self, start_pos, end_pos):
        """
            Fonction qui permet d'ajouter une série de routes
            Prend en paramètre 2 positions de souris sous forme de tuple
        """
        line1, column1 = self.visualmap.get_sprite_at_screen_coordinates(start_pos)
        line2, column2 = self.visualmap.get_sprite_at_screen_coordinates(end_pos)

        if self.game.add_multiple_buildings((line1, column1), (line2, column2), "dwell"):
            self.visualmap.update_sprite_list(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
            return True
        return False

    def add_dwell(self, pos) -> bool:
    """
            Adding house function
    """
    line, column = self.visualmap.get_sprite_at_screen_coordinates(pos)
    if self.game.add_building(line, column, "dwell"):
       # si la route a été bien ajoutée on update la spritelist en la recréant
       # self.visualmap.update_sprite_list(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
       return True
    return False

 def add_multiple_buildings(self, start_pos, end_pos, version) -> bool:
        # Here we can't precisely calculate the money that will be needed to construct all the roads. we'll estimate
        # that
        estimated_counter_buildings = (abs(start_pos[0] - end_pos[0]) + 1) * (abs(start_pos[1] - end_pos[1]) + 1)
        if self.money < estimated_counter_buildings * building_dico[version].cost:
            print("Not enough money")
            return False
        # building = Building(self.map.buildings_layer, globalVar.LAYER5, version)
        line1, column1 = start_pos[0], start_pos[1]
        line2, column2 = end_pos[0], end_pos[1]

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
        added = False
        # On dessine une ligne verticale de routes de la ligne de départ jusqu'à la ligne de fin

        for i in vrange:
            for j in hrange:
                if self.add_building(i, j, version):
                    added = True
                    count += 1
        if added:
            self.money -= building_dico[version].cost * count
        return added