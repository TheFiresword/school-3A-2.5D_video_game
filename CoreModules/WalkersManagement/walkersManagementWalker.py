import CoreModules.TileManagement.tileManagementElement as element

"""
Un walker va être un Element qui en plus possède certaines propriétés.
Notamment un walker doit être lié à un building.
Il doit pouvoir se déplacer sur la map
"""


class Walker(element.Element):
    def __init__(self, id, x_pos, y_pos, house):
        super().__init__()
        self.id = id
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.house = house

    def walk(self):
        pass

    def work(self):
        pass


class Engineer(Walker):
    def work(self):
        pass


class Prefect(Walker):
    def work(self):
        pass


class Immigrant(Walker):
    def find_house(self):
        # Parcourir la liste des maisons, trouver celle dans lesquelle peut s'installer(nombre d'habitant, niveau d'habitaion)
        pass


class Cart_Pusher(Walker):
    def work(self):
        pass


class Delivery_Boy(Walker):
    def work(self):
        pass


class Market_Trader(Walker):
    def work(self):
        pass
