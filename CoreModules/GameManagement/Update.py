

class LogicUpdate():

    def __init__(self):
        self.has_evolved = []
        self.has_devolved = []
        self.catchedfire = []
        self.collapsed = []
        self.removed = []
        self.fire_level_change = []
        self.collapse_level_change = []
        pass

    def is_Empty(self):
        return not self.has_evolved and not self.catchedfire and not self.collapsed and not self.removed