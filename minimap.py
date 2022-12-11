import arcade
# Charger l'image de la mini-carte
mini_map_image = arcade.load_texture("mini_map.png")

# Définir les dimensions de la mini-carte
MINI_MAP_WIDTH = 200
MINI_MAP_HEIGHT = 200

# Définir les coordonnées de l'emplacement de la mini-carte sur l'écran
MINI_MAP_X = 50
MINI_MAP_Y = 50

# Définir les coordonnées de l'emplacement de la vue actuelle sur la mini-carte
VIEW_X = 100
VIEW_Y = 100


# Définir la couleur du contour de la mini-map
MINI_MAP_BORDER_COLOR = arcade.color.BLACK

# Définir la couleur de la ligne qui indique l'emplacement de la vue actuelle sur la mini-cart
VIEW_BORDER_COLOR = arcade.color.RED

#Définir le ratio de la vue actuelle sur la carte par rapport à la mini-carte
VIEW_SCALE = 0.25

#Dessiner la mini-carte
arcade.draw_texture_rectangle(MINI_MAP_X, MINI_MAP_Y, MINI_MAP_WIDTH, MINI_MAP_HEIGHT, mini_map_image)

#Dessiner le contour de la mini-carte
arcade.draw_rectangle_outline(MINI_MAP_X, MINI_MAP_Y, MINI_MAP_WIDTH, MINI_MAP_HEIGHT, MINI_MAP_BORDER_COLOR, 2)

#Calculer la largeur et la hauteur de la vue actuelle sur la mini-carte en utilisant le ratio de l'échelle
view_width = MINI_MAP_WIDTH * VIEW_SCALE
view_height = MINI_MAP_HEIGHT * VIEW_SCALE

#Dessiner le contour de la vue actuelle sur la mini-carte
arcade.draw_rectangle_outline(
MINI_MAP_X + VIEW_X - view_width / 2,
MINI_MAP_Y + VIEW_Y - view_height / 2,
view_width,
view_height,
VIEW_BORDER_COLOR,2)