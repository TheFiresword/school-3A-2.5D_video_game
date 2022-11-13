from uuid import uuid4

import arcade
import math
from pyglet.math import Vec2


SPRITE_SCALING = 2
SCALE_MIN = SPRITE_SCALING / 2
SCALE_MAX = 1.5 * SPRITE_SCALING

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Move with Scrolling Screen Example"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 220

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 7
JUMP_SPEED = 10

TILE_COUNT = 40



class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Initializer """
        super().__init__(width, height, title, resizable=True)

        # Sprite lists
        self.player_list = None
        self.grass_list = None

        # Set up the player
        self.player_sprite = None

        # Physics engine so we don't run into walls.

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        # Store our tile map
        self.tile_map = None

        # Store tuples (i,j): logic coordinates of sprites
        self.sprites_positions = []

        # The scaling of the sprites
        self.sprite_scaling = SPRITE_SCALING

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)





    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.grass_list = arcade.SpriteList()



        # --- Load our map with a tile-map
        self.set_map_through_tilemap()
        #self.convert_sprite_cartesian_to_isometric()

        # --- Load our map with a loop
        self.set_map_through_a_loop()
        self.convert_sprite_cartesian_to_isometric()

        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           scale=0.4)
        self.player_sprite.center_x = self.grass_list[int(math.pow(TILE_COUNT, 2)//2)].center_x - self.player_sprite.width/2
        self.player_sprite.center_y = self.grass_list[int(math.pow(TILE_COUNT, 2)//2)].center_y - self.player_sprite.height/2
        self.player_list.append(self.player_sprite)


    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.grass_list.draw()
        k = 0

        for grass in self.grass_list:
            (i, j) = self.sprites_positions[k]
            if k > 40:
                break
            arcade.draw_text(f'({i},{j})', grass.center_x, grass.center_y, arcade.color.BLACK, 8, bold=True)

            k += 1

        self.player_list.draw()


        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()


    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.player_sprite.center_x += self.grass_list[0].width / 2
            self.player_sprite.center_y += self.grass_list[0].height / 2

        elif key == arcade.key.LEFT:
            self.player_sprite.center_x -= self.grass_list[0].width / 2
            self.player_sprite.center_y += self.grass_list[0].height / 2

        elif key == arcade.key.RIGHT:
            self.player_sprite.center_x += self.grass_list[0].width / 2
            self.player_sprite.center_y -= self.grass_list[0].height / 2

        elif key == arcade.key.DOWN:
            self.player_sprite.center_x -= self.grass_list[0].width / 2
            self.player_sprite.center_y -= self.grass_list[0].height / 2

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0


    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """"
        When the user scrolls the mouse we want to zoom/unzoom the camera.
        There is an arcade function that might be useful: arcade.SpriteList().rescale()
        This function rescales all the sprites of a spriteList.
        But the problem is that the rendering is not correct.
        The map is deformed.

        So I did it  other way.
        Empty the spriteList and recreate it with the right scaling.
        """

        if scroll_y < 0:
            next_sprite_scaling = self.sprite_scaling * 0.9
            if SCALE_MIN < self.grass_list[0].scale and SCALE_MIN < next_sprite_scaling:
                self.sprite_scaling = next_sprite_scaling
                self.player_list.rescale(0.9)
            else:
                self.sprite_scaling = SCALE_MIN
        else:
            next_sprite_scaling = self.sprite_scaling * 1.1
            if self.grass_list[0].scale < SCALE_MAX and SCALE_MAX > next_sprite_scaling:
                self.sprite_scaling = next_sprite_scaling
                self.player_list.rescale(1.1)
            else:
                self.sprite_scaling = SCALE_MAX

        self.grass_list.clear()
        self.set_map_through_a_loop()
        self.convert_sprite_cartesian_to_isometric()




    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.grass_list.update()

        self.player_list.update()

        # Scroll the screen to the player
        self.scroll_to_player()

    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a
        smoother pan.
        """

        position = self.player_sprite.center_x - self.width / 2, \
            self.player_sprite.center_y - self.height / 2
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))

    def set_map_through_tilemap(self):
        """"
        Load a tilemap predrawn and setup the sprites_positions list

        """
        map_name = "caeasar_level_1.json"
        self.tile_map = arcade.load_tilemap(map_name, scaling=self.sprite_scaling)

        # set the background color of the window to the tilemap background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Set the grass_list from a tile-map
        self.grass_list = self.tile_map.sprite_lists["grass"]

        # define the logic coordinates of each sprite.
        # NB: THE TILEMAP CONTAINS SPRITES DRAWN FROM THE TOP TO THE BOTTOM SO THE INDEXES ARE NOT IN INCREMENTED ORDER
        for grass in self.grass_list:
            index = self.grass_list.index(grass)
            i = TILE_COUNT - 1 - index // TILE_COUNT
            j = index % TILE_COUNT
            self.sprites_positions.append((i, j))


    def set_map_through_a_loop(self):
        for i in range(TILE_COUNT):
            for j in range(TILE_COUNT):
                grass = arcade.Sprite("Land1a_00002.png", scale=self.sprite_scaling)

                # Set up the isometric coordinates directly with the indices
                # But I did not do it this way

                #grass.center_x = (j + i) * grass.width / 2
                #grass.center_y = (i - j) * grass.height / 2

                # Generate the cartesian map
                grass.center_x = grass.width * (j + 1 / 2)
                grass.center_y = grass.height * (i + 1 / 2)

                self.grass_list.append(grass)
                self.sprites_positions.append((i, j))
        print(self.grass_list[0].scale)


    def convert_sprite_cartesian_to_isometric(self):
        """"
        Convert the sprites center cartesian coordinates to isometric coordinates
        """
        k = 0
        for grass in self.grass_list:
            cart_x, cart_y = grass.center_x, grass.center_y
            (i, j) = self.sprites_positions[k]
            grass.center_x = (cart_x + cart_y) - (grass.width * j / 2)
            grass.center_y = (-cart_x + cart_y)/2 + (grass.height * j / 2)
            k += 1

    def convert_sprite_isometric_to_cartesian(self):
        """"
                Convert the sprites center isometric coordinates to cartesian coordinates
                """
        k = 0
        for grass in self.grass_list:
            iso_x, iso_y = grass.center_x, grass.center_y
            (i, j) = self.sprites_positions[k]
            grass.center_x = iso_x/2 - iso_y + j*(3*grass.height/2 - grass.width / 4)
            grass.center_y = iso_x/2 + iso_y + j*(grass.height/2 - grass.width/4)
            k += 1


    def update_rescaled_sprites_coordinates(self):
        k = 0
        for grass in self.grass_list:
            (i, j) = self.sprites_positions[k]
            if j == 1:
                grass.center_x = grass.center_x - grass.width/4
                grass.center_y = grass.center_y + grass.height/4
            k += 1

    def rescale_sprites(self, _sprite_list: arcade.sprite_list, scale: float):
        """"
        A reimplementation of rescale() function -- as rescale() has an unexpected behavior
        """
        for element in _sprite_list:
            element.width *= scale
            element.height *= scale



def main():
    """ Main function """
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()