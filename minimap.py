import arcade

# les couleurs à utiliser pour chaque type d'élément
colors = {
    'building': 'brown',
    'road': 'grey',
    'water': 'blue',
    'rocks': 'darkgrey'
}

# une fonction pour dessiner la mini-carte
def draw_mini_map(main_map, mini_map):
    # Effacez la mini-carte
    arcade.start_render()
    # Parcourez chaque élément de la carte principale
    for i in range(main_map.width):
        for j in range(main_map.height):
            # Récupérez le type d'élément à cette position
            element_type = main_map[i][j]
            # Obtenez la couleur associée à ce type d'élément
            color = colors[element_type]
            # Dessinez un carré de cette couleur à la position correspondante sur la mini-carte
            arcade.draw_rectangle_filled(mini_map, i, j, 1, 1, color)

# une fonction pour mettre à jour la mini-carte
def update_mini_map(main_map, mini_map):
    # Redessinez la mini-carte
    draw_mini_map(main_map, mini_map)
    # Affichez la mini-carte
    arcade.finish_render()

# Utilisez la fonction pour dessiner initialement la mini-carte en fonction de la carte principale
update_mini_map(main_map, mini_map)

# Dans notre boucle de jeu, appelez la fonction update_mini_map chaque fois qu'on apporte des modifications à la carte principale
while True:
    # Mettre à jour la carte principale
    update_main_map()
    # Mettre à jour la mini-carte en fonction de la carte principale mise à jour
    update_mini_map(main_map, mini_map)
#############################################################################################################################
""""
import arcade
import math

SIZE = 200
GAP = 13 # distance between border and rect map

def find_closest(pix, tab):
 return min(tab, key=lambda c: (c[0] - pix[0]) ** 2 + (c[1] - pix[1]) ** 2)

class Minimap:
#STATIC ATTRIBUTES
tab = []
def __init__(self, world, screen, camera, width, height, nrplayer):
    self.idplayer = nrplayer
    # SPECS WORLD / CAMERA / SCREEN
    self.world = world
    self.camera = camera
    self.height = height
    self.width = width
    # SPECS BORDURE AUTOUR DE MINIMAP
    self.border = arcade.load_texture('assets/hud/minimapBorder.png')
    self.border_width, self.border_height = SIZE + GAP, SIZE + GAP
    # SPECS MINIMAP
    self.rect = arcade.create_rectangle((GAP - 4, self.height - self.border_height * math.sqrt(2) + GAP - 4), SIZE, SIZE)
    self.bordrect = arcade.create_rectangle((0, self.height - self.border_height * math.sqrt(2)), 1, 1)
    self.mapSurf = arcade.create_surface(self.rect.width, self.rect.height)
    self.newSurf = arcade.create_surface(self.rect.width, self.rect.height)
    # UPDATE DE LA MINIMAP
    self.row = 0
    self.update_mapsurf()  # update de base à la créa de l'objet minimap

    # add
    self.red_crop = (0, 20, self.world.grid_length_x, self.world.grid_length_y)
    self.intermediate = (0, 0, 0, 0)
    self.mpos = (0, 0)
    self.viewArea = (0, 0)
    self.view = [(0, 0), (0, 0), (0, 0), (0, 0)]

    self.draw(screen)

    Minimap.tab_coord_filler()

@staticmethod
def tab_coord_filler():
    for x in range(100):
        for y in range(100):
            Minimap.tab.append((int(70 + (x - y) * 70 / 99), int((y + x) * 70 / 99)))

@staticmethod
def mmap_to_coord(pix):
    return int(Minimap.tab.index(find_closest(pix, Minimap.tab)) / 100), int(
        Minimap.tab.index(find_closest(pix, Minimap.tab)) % 100)

def mmap_to_pos(self, pix):
    x, y = pix
    return self.world.mouse_to_grid(x, y, self.camera.scroll)

def draw(self, screen):
    self.intermediate = arcade.transform_rotate(arcade.transform_scale(self.mapSurf.subsurface(self.red_crop), 2), -45)
    self.mapSurf.set_colorkey((0, 0, 0))
    arcade.draw_texture_rectangle(self.bordrect.center_x, self.bordrect.center_y, self.border_width, self.border_height, self.border, rotation=-45)
    arcade.draw_surface_rectangle(self.rect.center_x, self.rect.center_y, self.intermediate.width, self.intermediate.height, self.intermediate)

def update(self):
    self.update_mapsurf()
    self.update_row_of_surf()
    self.mapSurf.blit(self.mapSurf, (-3 * GAP + 1 / 5 * SIZE - 1, -2 * GAP - 4 + 1 / 4 * SIZE))
    self.update_camera_rect()

def update_mapsurf(self):
    for i in range(30):
        for j in range(30):
            color = self.world.get_color_of_element(i, j)
            if color == self.idplayer:
                color = (255, 255, 255)
            self.mapSurf.set_at((i, j), color)

def update_row_of_surf(self):
    self.row = (self.row + 1) % 30
    for i in range(30):
        color = self.world.get_color_of_element(i, self.row)
        if color == self.idplayer:
            color = (255, 255, 255)
        self.newSurf.set_at((i, 0), color)
    self.mapSurf.blit(self.newSurf, (0, self.row))

def update_camera_rect(self):
    self.viewArea = self.camera.get_view()
    self.view[0] = (self.viewArea[0] * SIZE / self.world.grid_length_x, self.viewArea[1] * SIZE / self.world.grid_length_y)
    self.view[1] = (self.viewArea[0] * SIZE / self.world.grid_length_x, self.viewArea[3] * SIZE / self.world.grid_length_y)
    self.view[2] = (self.viewArea[2] * SIZE / self.world.grid_length_x, self.viewArea[3] * SIZE / self.world.grid_length_y)
    self.view[3] = (self.viewArea[2] * SIZE / self.world.grid_length_x, self.viewArea[1] * SIZE / self.world.grid_length_y)
    self.camera_rect = arcade.create_rectangle(self.view[0], self.view[2])
"""