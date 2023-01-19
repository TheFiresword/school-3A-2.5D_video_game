import arcade
import pyglet.media as media

# Charger le fichier audio pour la bande sonore de fond
bg_music = media.load("bg_music.mp3")
bg_music.play()

# Charger les fichiers audio pour les effets sonores
build_sound = media.load("build.wav")

# Fonction pour activer la répétition de la musique de fond
def repeat_bg_music():
    bg_music.loop = True
    bg_music.play()

# Fonction pour jouer un effet sonore de construction
def play_build_sound():
    build_sound.play()

# Utilisez les fonctions ci-dessus dans votre code pour jouer les effets sonores lorsque les événements appropriés se produisent
# Par exemple :

def on_build_button_clicked():
    play_build_sound()
    # autres actions pour la construction



# Appelez la fonction repeat_bg_music() pour activer la répétition de la musique de fond
repeat_bg_music()
