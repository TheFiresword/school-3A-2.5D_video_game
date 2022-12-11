import arcade


# Définir les dimensions de la fenêtre de jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Créez une variable pour savoir si le jeu est en pause
is_paused = False

#Ouvrir la fenetre du jeu
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pause Example")

# Définir la couleur du background
arcade.set_background_color(arcade.color.WHITE)

# Cette fonction sera appelée chaque fois qu'une touche est pressee
def on_key_press(key, modifiers):
    global is_paused
    if key == arcade.key.P:
        # Si le jeu est actuellement en pause, reprenez-le
        if is_paused:
            arcade.unpause()
            is_paused = False
        # Si le jeu est en cours, mettez-le en pause
        else:
            arcade.pause()
            is_paused = True

""" 
def on_draw():
    arcade.start_render()
    # Si le jeu est en pause, affichez un message indiquant que le jeu est en pause
    if game_paused:
        arcade.draw_text("Jeu en pause", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, font_size=20, anchor_x="center")
"""

# Start the game
arcade.run()
