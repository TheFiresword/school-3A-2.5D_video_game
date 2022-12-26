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
            self.visualmap.update_sprite_list(self.visualmap.buildings_layer, self.game.map.buildings_layer.array)
            return True
        return False