import sys

import pygame as pg

import settings
import utils
from tile import TileSprite


class TicTacToe:
    """Class containing Tic Tac Toe game board and logic."""

    def __init__(self, board_size: tuple[int, int], grid_division: int) -> None:
        pg.init()
        self.window_size = board_size
        self.grid_division = grid_division
        self.grid_size = int(board_size[0] / grid_division), int(
            (board_size[1] - settings.SCREEN_HEIGHT_OFFSET) / grid_division)
        self.sprite_coords = []
        self.sprite_types = []
        self.sprite_group = pg.sprite.Group()
        self.grid = [  # grid containing sprite string types on the screen
            [None, None, None],  # row 1
            [None, None, None],  # row 2
            [None, None, None]   # row 3
        ]
        self.game_over = False

    def add_turn(self, sprite_type: str, grid_coords: tuple[int, int]) -> None:
        """Adds a turn to a certain grid slot."""
        self.sprite_types.append(sprite_type)
        self.sprite_coords.append(grid_coords)
        x, y = self.get_grid_indices(grid_coords)
        self.grid[x][y] = sprite_type

    def get_winner(self) -> str | None:
        """Returns a winner if someone has won the board."""
        for combination in self.get_possible_win_combinations():
            cross_count = 0
            circle_count = 0
            for i, row in enumerate(self.grid):
                for j, elem in enumerate(row):
                    if not (i, j) in combination:
                        continue
                    match elem:
                        case "cross":
                            cross_count += 1
                            if cross_count >= 3:
                                return "cross"
                        case "circle":
                            circle_count += 1
                            if circle_count >= 3:
                                return "circle"
        return

    def get_possible_win_combinations(self):
        if self.grid_division != 3:
            raise NotImplementedError("At the moment only 3x3 grid is supported.")
        winning_combinations = [
            [(0, 0), (0, 1), (0, 2)],  # Row 1
            [(1, 0), (1, 1), (1, 2)],  # Row 2
            [(2, 0), (2, 1), (2, 2)],  # Row 3
            [(0, 0), (1, 0), (2, 0)],  # Column 1
            [(0, 1), (1, 1), (2, 1)],  # Column 2
            [(0, 2), (1, 2), (2, 2)],  # Column 3
            [(0, 0), (1, 1), (2, 2)],  # Diagonal from top-left
            [(0, 2), (1, 1), (2, 0)]  # Diagonal from top-right
        ]
        return winning_combinations

    def get_all_grid_indices(self):
        if self.grid_division != 3:
            raise NotImplementedError("At the moment only 3x3 grid is supported.")
        return [
            (0, 0), (0, 1), (0, 2),  # Row 1
            (1, 0), (1, 1), (1, 2),  # Row 2
            (2, 0), (2, 1), (2, 2),  # Row 3
        ]

    def is_winnable(self) -> bool:
        """Checks if there are no more legal moves."""
        if self.is_full_board():
            return False
        for combination in self.get_possible_win_combinations():
            cross_count = 0
            circle_count = 0
            for i, row in enumerate(self.grid):
                for j, elem in enumerate(row):
                    if not (i, j) in combination:
                        continue
                    match elem:
                        case "cross" | None:
                            cross_count += 1
                            if cross_count >= 3:
                                return True
                        case "circle" | None:
                            circle_count += 1
                            if circle_count >= 3:
                                return True
        return False

    def is_full_board(self) -> bool:
        """Checks if the board is completely full of sprites."""
        if len(self.sprite_types) >= self.grid_division**2:
            return True
        return False

    def reset(self) -> tuple[pg.Surface, pg.Rect]:
        """Resets the game board."""
        self.sprite_coords = []
        self.sprite_types = []
        self.grid = [  # grid containing sprite type strings on the screen
            [None, None, None],  # row 1
            [None, None, None],  # row 2
            [None, None, None]  # row 3
        ]
        self.sprite_group = pg.sprite.Group()
        self.set_turn_sprite("cross")
        self.game_over = False
        text_label = "First turn:".center(settings.TEXT_WIDTH)
        return utils.get_turn_text_objects(text_label)

    def get_grid_coords(self, coordinates: tuple[int, int]) -> tuple[int, int]:
        """Returns the board coordinates for the grid center of the given position."""
        grid_size = self.window_size[0]
        ix, iy = self.get_grid_indices(coordinates)
        return int(grid_size / 6 + ix * grid_size / 3), int(grid_size / 6 + iy * grid_size / 3)

    def get_grid_indices(self, coordinates: tuple[int, int]) -> tuple[int, int]:
        """Returns grid x- and y-indexes for whichever grid the given coordinates are in.
        3x3 example:
        (0,0)|(1,0)|(2,0)
        (0,1)|(1,1)|(2,1)
        (0,2)|(1,2)|(2,2)
        """
        x, y = coordinates
        grid_size = self.window_size[0]
        ix = utils.section_of_number(x, grid_size, self.grid_division)
        iy = utils.section_of_number(y, grid_size, self.grid_division)
        if ix is None or iy is None:
            raise ValueError("Coordinates are not in the game window.")
        return ix - 1, iy - 1

    def add_sprite_to_screen(self,
                             position: tuple[int, int],
                             sprite_type: str,
                             image_name: str,
                             scale: tuple[int | float, int | float] = (1, 1),
                             anchor: str = "center") -> None:
        """Adds a GameSprite object to the 'self.all_sprites' pg.sprite.Group."""
        if sprite_type != "turn_sprite":  # this is a click on grid: a turn
            self.add_turn(sprite_type, position)
        # noinspection PyTypeChecker
        self.sprite_group.add(TileSprite(sprite_type=sprite_type,
                                         image_file_name=image_name,
                                         position=position,
                                         scale=scale,
                                         anchor=anchor))

    def add_sprite_on_click(self,
                            position: tuple[int, int],
                            sprite_type: str,
                            image_name: str,
                            scale: tuple[int | float, int | float] = (1, 1),
                            anchor: str = "center") -> int:
        """Adds a GameSprite object to the 'self.all_sprites' pg.sprite.Group
         if its inside the grid and the grid slot is empty.
         """
        try:
            position = self.get_grid_coords(position)
            if position in self.sprite_coords:  # grid position is taken
                return 1
            self.add_sprite_to_screen(sprite_type=sprite_type,
                                      image_name=image_name,
                                      position=position,
                                      scale=scale,
                                      anchor=anchor)
            return 0
        except ValueError:  # Click is outside the grid.
            return 1

    def add_cross_sprite_on_click(self, position: tuple[int, int]) -> int:
        """Adds a cross sprite to the 'all_sprites' pg.sprite.Group
        if the click is inside the grid and the placement is empty.
        """
        sprite_type = "cross"
        image_name = settings.CROSS_IMAGE
        return self.add_sprite_on_click(position, sprite_type, image_name)

    def add_circle_sprite_on_click(self, position: tuple[int, int]) -> int:
        """Adds a circle sprite to the 'all_sprites' pg.sprite.Group
         if the click is inside the grid and the placement is empty.
         """
        sprite_type = "circle"
        image_name = settings.CIRCLE_IMAGE
        return self.add_sprite_on_click(position, sprite_type, image_name)

    def remove_previous_turn_sprite(self):
        """Removes the previous turn GameSprite from the self.sprite_* lists and the 'all_sprites' pg.sprite.Group."""
        if not bool(self.sprite_types):  # no sprites
            return
        for key, value in self.sprite_group.spritedict.items():
            if value is None:
                continue
            if value.size == (45, 45):
                del self.sprite_group.spritedict[key]
                return

    def set_turn_sprite(self, sprite_type: str) -> None:
        """Changes the bottom sprite image to whoevers turn it is."""
        if len(game.sprite_types):  # not first sprite
            self.remove_previous_turn_sprite()
        match sprite_type:
            case "cross":
                self.add_sprite_to_screen(settings.BOTTOM_SPRITE_POSITION, "turn_sprite", settings.CROSS_IMAGE,
                                          scale=(settings.BOTTOM_SPRITE_SCALE, settings.BOTTOM_SPRITE_SCALE))
            case "circle":
                self.add_sprite_to_screen(settings.BOTTOM_SPRITE_POSITION, "turn_sprite", settings.CIRCLE_IMAGE,
                                          scale=(settings.BOTTOM_SPRITE_SCALE, settings.BOTTOM_SPRITE_SCALE))
            case _:
                self.remove_previous_turn_sprite()


    def run(self):
        """Runs the Tic Tac Toe game loop."""
        # initialize window scren
        screen = pg.display.set_mode(self.window_size)

        # Background, icon,and title
        background_image = pg.image.load(settings.BACKGROUND_IMAGE)
        pg.display.set_caption(settings.WINDOW_TITLE)
        pg.display.set_icon(pg.image.load(settings.ICON_IMAGE))

        # Bottom text saying whose turn it is
        text_label = "First turn:".center(settings.TEXT_WIDTH)
        text_surface, text_rect = utils.get_turn_text_objects(text_label)

        # Bottom image showing whose turn it is, cross begins
        self.set_turn_sprite("cross")

        mouse = pg.mouse.get_pos()
        while True:
            screen.fill(settings.WINDOW_BG_COLOR)
            screen.blit(background_image, (0, 0))
            screen.blit(text_surface, text_rect)
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        sys.exit()

                    case pg.MOUSEBUTTONDOWN:
                        # Click within grid:
                        if 0 <= mouse[0] <= settings.SCREEN_WIDTH and 0 <= mouse[1] <= settings.SCREEN_WIDTH:
                            # First click:
                            if len(self.sprite_types) < 1:
                                self.add_cross_sprite_on_click(event.pos)
                                # Replace bottom text:
                                text_label = "Next turn: ".center(settings.TEXT_WIDTH)
                                text_surface, text_rect = utils.get_turn_text_objects(text_label)
                                self.set_turn_sprite("circle")
                                continue

                            # Not first click:
                            if self.game_over:
                                continue
                            sprite_type = self.sprite_types[-1]  # previous added sprite
                            if sprite_type == "turn_sprite":
                                sprite_type = self.sprite_types[-2]
                            match sprite_type:
                                case "cross":
                                    if not bool(
                                            self.add_circle_sprite_on_click(event.pos)):  # try adding circle sprite
                                        self.set_turn_sprite("cross")  # Change the bottom image sprite to circle

                                case "circle":
                                    if not bool(
                                            self.add_cross_sprite_on_click(event.pos)):  # try adding cross sprite
                                        self.set_turn_sprite("circle")  # Change the bottom image sprite to cross

                        # Click within reset button:
                        reset_left_position = settings.RESET_TEXT_POSITION[0]
                        reset_right_position = reset_left_position + settings.RESET_BUTTON_SIZE[0]
                        reset_top_position = settings.RESET_TEXT_POSITION[1]
                        reset_bottom_position = reset_top_position + settings.RESET_BUTTON_SIZE[1]
                        if reset_left_position <= mouse[0] <= reset_right_position and \
                                reset_top_position <= mouse[1] <= reset_bottom_position:
                            text_surface, text_rect = self.reset()

            if (winner := self.get_winner()) is not None:
                self.game_over = True
                text_surface, text_rect = utils.get_winner_text_objects(winner)
                self.set_turn_sprite(winner)
            elif not self.is_winnable() or self.is_full_board():  # no more legal moves
                self.game_over = True
                text_surface, text_rect = utils.get_tie_text_objects()
                self.set_turn_sprite(None)

            mouse = pg.mouse.get_pos()  # save mouse position for checking where next click is

            # Render reset text if its not already reset
            if text_label != "First turn:".center(settings.TEXT_WIDTH):
                # If mouse is hovering within button, make it a lighter color
                reset_left_position = settings.RESET_TEXT_POSITION[0]
                reset_right_position = reset_left_position + settings.RESET_BUTTON_SIZE[0]
                reset_top_position = settings.RESET_TEXT_POSITION[1]
                reset_bottom_position = reset_top_position + settings.RESET_BUTTON_SIZE[1]
                if reset_left_position <= mouse[0] <= reset_right_position and \
                        reset_top_position <= mouse[1] <= reset_bottom_position:
                    pg.draw.rect(screen, settings.RESET_BUTTON_BG_COLOR_LIGHTER, settings.RESET_BUTTON_POSITION)
                else:
                    pg.draw.rect(screen, settings.RESET_BUTTON_BG_COLOR, settings.RESET_BUTTON_POSITION)
                reset_text_surface, reset_text_rect = utils.get_reset_text_objects()
                screen.blit(reset_text_surface, settings.RESET_TEXT_POSITION)

            # Draw sprites and update the window
            self.sprite_group.draw(screen)
            pg.display.update()


if __name__ == "__main__":
    game = TicTacToe(board_size=(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), grid_division=3)
    game.run()
