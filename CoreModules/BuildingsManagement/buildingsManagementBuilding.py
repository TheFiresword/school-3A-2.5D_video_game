class Building:
    def __init__(self, size, x_pos, y_pos, type):#size est un double (L,l)
        self.size = size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        self.fire_level = 0
        self.structure_level = 0
        self.isBurnt = False
        self.isDestroyed = False

    def setIsBurnt(self, isBurnt):
        self.isBurnt = isBurnt

    def setIsDestroyed(self, isDestroyed):
        self.isDestroyed = isDestroyed


class Dwelling(Building):
    def __init__(self, current_population, max_population, size, x_pos, y_pos, type):
        super().__init__(size, x_pos, y_pos, type)
        self.current_population = current_population
        self.max_population = max_population