my_array=[]

my_array[2][1] ="raa"
print(my_array)


"""
        # On ajoute une route en fonction de son voisinage
        if left_version in ["normal", "00094"] or right_version in ["normal", "00094"]:
            element = Element.Element(self, self.type, "00094")

            self.array[line][column] = element
            self.array[line][column].id = next(self.id_iterator)
            self.array[line][column].position = (line, column)

            if left_version == "normal":
                element_at_left = Element.Element(self, self.type, "00094")
                left_id = self.array[line][column - 1].id
                element_at_left.id = left_id
                element_at_left.position = (line, column - 1)

                self.array[line][column - 1] = element_at_left

            if right_version == "normal":
                element_at_right = Element.Element(self, self.type, "00094")
                right_id = self.array[line][column + 1].id
                element_at_right.id = right_id
                element_at_right.position = (line, column + 1)

                self.array[line][column + 1] = element_at_right
            return True

        self.array[line][column] = element
        self.array[line][column].id = next(self.id_iterator)
        self.array[line][column].position = (line, column)
        """