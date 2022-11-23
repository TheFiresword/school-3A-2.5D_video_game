from CoreModules.MapManagement import mapManagementLayer as overlay

LAYER1 = "grass"
LAYER2 = "hill"
LAYER3 = "tree"
LAYER4 = "building"


class MapLogic:
    def __init__(self):
        # Booléen qui dit si la map est affichée ou pas
        self.active = False

        self.grass_layer = overlay.Layer(LAYER1)
        self.grass_layer.automatic_fill_layer()

        self.hills_layer = overlay.Layer(LAYER2)
        self.trees_layer = overlay.Layer(LAYER3)

        self.building_layer = overlay.Layer(LAYER4)
        # liste de Walker()
        self.walkers_list = []
