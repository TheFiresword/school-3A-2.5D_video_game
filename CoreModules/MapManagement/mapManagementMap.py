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
        # Experimentation
        for i in range(20, 39):
            self.grass_layer.set_position(i, i, "yellow")
            self.grass_layer.set_position(40-i, i, "yellow")
            self.grass_layer.set_position(20, i, "buisson")

        self.hills_layer = overlay.Layer(LAYER2)
        # Le tableau de hills initial
        hills_array = [
            [],
            ["null","normal"],
            ["normal", "normal","null","null","normal","normal","normal","normal","normal","normal","normal","normal",
             "normal","normal","normal"]
        ]
        self.hills_layer.custom_fill_layer(hills_array)

        self.trees_layer = overlay.Layer(LAYER3)
        trees_array = [
            ["normal","normal","normal","null","null","normal"],
            ["normal", "normal", "normal", "null", "null", "normal"],
            ["normal", "normal", "normal", "null", "null", "normal"],
            ["normal", "normal", "normal", "null", "null", "normal"],
        ]
        self.trees_layer.custom_fill_layer(trees_array)

        self.building_layer = overlay.Layer(LAYER4)

        # liste de Walker()
        self.walkers_list = []
