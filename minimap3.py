import arcade

# Load the mini-map image
mini_map_image = arcade.load_texture("mini_map.png")

# Define the dimensions of the mini-map
MINI_MAP_WIDTH = 200
MINI_MAP_HEIGHT = 200

# Define the coordinates of the mini-map on the screen
MINI_MAP_X = 50
MINI_MAP_Y = 50

# Define the color of the mini-map border
MINI_MAP_BORDER_COLOR = arcade.color.BLACK

# Define the color of the line indicating the current view on the mini-map
VIEW_BORDER_COLOR = arcade.color.RED

# Define the scale ratio of the current view on the main map to the mini-map
VIEW_SCALE = 0.25

# Create a function to update the mini-map image
def update_mini_map(main_map, mini_map_image):
  # Clear the mini-map image
  arcade.clear_texture(mini_map_image)

  # Loop through the elements on the main map and draw them onto the mini-map image
  for element in main_map:
    # Calculate the coordinates of the element on the mini-map image
    element_x = element.x * VIEW_SCALE
    element_y = element.y * VIEW_SCALE

    # Draw the element onto the mini-map image
    arcade.draw_rectangle_filled(element_x, element_y, element.width * VIEW_SCALE, element.height * VIEW_SCALE, element.color)

# Update the mini-map image and current view rectangle on the mini-map each time an element is added to the main map
def add_element_to_main_map(element):
  main_map.append(element)
  update_mini_map(main_map, mini_map_image)

  # Update the VIEW_X and VIEW_Y coordinates to reflect the current position of the view on the main map
  VIEW_X = main_map.view_x * VIEW_SCALE
  VIEW_Y = main_map.view_y * VIEW_SCALE

# Draw the mini-map and current view rectangle on the mini-map
def draw():
  # Draw the mini-map image
  arcade.draw_texture_rectangle(MINI_MAP_X, MINI_MAP_Y, MINI_MAP_WIDTH, MINI_MAP_HEIGHT, mini_map_image)

  # Draw the border around the mini-map
  arcade.draw_rectangle_outline(MINI_MAP_X, MINI_MAP_Y, MINI_MAP_WIDTH, MINI_MAP_HEIGHT, MINI_MAP_BORDER_COLOR, 2)

  # Calculate the width and height of the current view rectangle on the mini-map using the scale ratio
  view_width = MINI_MAP_WIDTH * VIEW_SCALE
  view_height = MINI_MAP_HEIGHT * VIEW_SCALE

  # Draw the border around the current view on the mini-map
  arcade.draw_rectangle_outline(
      MINI_MAP_X + VIEW_X - view_width / 2,
      MINI_MAP_Y + VIEW_Y - view_height / 2,
      view_width,
      view_height,
      VIEW_BORDER_COLOR,
      2
  )
