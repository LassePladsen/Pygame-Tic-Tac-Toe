import os

SCREEN_WIDTH = 300
SCREEN_HEIGHT_OFFSET = 50
SCREEN_HEIGHT = SCREEN_WIDTH + SCREEN_HEIGHT_OFFSET
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
DATA_DIR = os.path.join(MAIN_DIR, "data")

# Game window title and icon
WINDOW_TITLE = "Tic Tac Toe"
WINDOW_BG_COLOR = "white"

# Game sprites image filenames
CROSS_IMAGE = os.path.join(DATA_DIR, "red_cross.png")
CIRCLE_IMAGE = os.path.join(DATA_DIR, "blue_circle.png")

# Bottom text
FONT = "arialbold"
FONT_SIZE = 30
FONT_BG_COLOR = "white"
FONT_COLOR = "black"
GAME_OVER_FONT_COLOR = "purple"
TEXT_POSITION = 4, 315  # anchor topleft

# Bottom image sprite
BOTTOM_SPRITE_SCALE = 0.5
BOTTOM_SPRITE_POSITION = 150, 323  # anchor center

# Reset button
RESET_BUTTON_SIZE = 50, 20
RESET_BUTTON_POSITION = 245, 315, RESET_BUTTON_SIZE[0], RESET_BUTTON_SIZE[1]  # anchor center
RESET_BUTTON_BG_COLOR = "red"
RESET_BUTTON_BG_COLOR_LIGHTER = "gray"

# Reset button text
RESET_FONT = FONT
RESET_FONT_SIZE = 18
RESET_FONT_COLOR = "white"
RESET_TEXT_POSITION = RESET_BUTTON_POSITION[0] + RESET_BUTTON_SIZE[0] / 10, \
                      RESET_BUTTON_POSITION[1] + RESET_BUTTON_SIZE[1] / 5  # (anchor center)


