import sys

import pygame as pg

import settings
import utils
from tile import TileSprite

pg.init()


class TicTacToe:
    """Class containing Tic Tac Toe game board and logic."""

    def __init__(self, board_size: tuple[int, int], grid: int) -> None:
        self.window_size = board_size
        self.grid = grid
        self.grid_size = int(board_size[0] / grid), int((board_size[1] - settings.SCREEN_HEIGHT_OFFSET) / grid)
        self.sprite_coords = []
        self.sprite_descriptions = []
        self.sprite_group = pg.sprite.Group()
        self.game_over = False

    def add_turn(self, description: str, grid_coords: tuple[int, int]) -> None:
        """Adds a turn to a certain grid slot."""
        self.sprite_descriptions.append(description)
        self.sprite_coords.append(grid_coords)

    def get_winner(self) -> str | None:
        """Returns a winner if someone has won the board."""
        if self.grid != 3:
            raise NotImplementedError("At the moment only 3x3 grid is supported.")
        if len(self.sprite_coords) < 3:
            return None
        winning_combinations = self.get_possible_win_combinations()
        grid_indices = [self.get_grid_indices(i) for i in self.sprite_coords]
        # Checks through all indices in the winning combinations are in the grid indices list.
        for combination in winning_combinations:
            if all(win_indices in grid_indices for win_indices in combination):  # winning combination is found
                if all(self.sprite_descriptions[grid_indices.index(win_indices)] == "cross" for win_indices in
                       combination):  # all sprites in the win combination are crosses
                    return "cross"
                elif all(self.sprite_descriptions[grid_indices.index(win_indices)] == "circle" for win_indices in
                         combination):  # all sprites in the win combination are circles
                    return "circle"
        return None

    def get_possible_win_combinations(self):
        if self.grid != 3:
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
        if self.grid != 3:
            raise NotImplementedError("At the moment only 3x3 grid is supported.")
        return [
            (0, 0), (0, 1), (0, 2),  # Row 1
            (1, 0), (1, 1), (1, 2),  # Row 2
            (2, 0), (2, 1), (2, 2),  # Row 3
        ]

    # TODO
    def check_winnable(self) -> bool:
        """Checks if there are no more legal moves."""
        pass

    def check_full_board(self) -> bool:
        """Checks if the board is completely full of sprites."""
        if len(self.sprite_descriptions) >= self.grid**2:
            return True
        return False

    def reset(self) -> tuple[pg.Surface, pg.Rect]:
        """Resets the game board."""
        self.sprite_coords = []
        self.sprite_descriptions = []
        self.sprite_group = pg.sprite.Group()
        self.set_turn_sprite("cross")
        self.game_over = False
        text_label = "   First turn:"
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
        ix = utils.section_of_number(x, grid_size, self.grid)
        iy = utils.section_of_number(y, grid_size, self.grid)
        if ix is None or iy is None:
            raise ValueError("Coordinates are not in the game window.")
        return ix - 1, iy - 1

    def add_sprite_to_screen(self,
                             position: tuple[int, int],
                             description: str,
                             image_name: str,
                             scale: tuple[int | float, int | float] = (1, 1),
                             anchor: str = "center") -> None:
        """Adds a GameSprite object to the 'self.all_sprites' pg.sprite.Group."""
        if description != "turn_sprite":  # this is a click on grid: a turn
            self.add_turn(description, position)
        # noinspection PyTypeChecker
        self.sprite_group.add(TileSprite(description=description,
                                         image_file_name=image_name,
                                         position=position,
                                         scale=scale,
                                         anchor=anchor))

    def add_sprite_on_click(self,
                            position: tuple[int, int],
                            description: str,
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
            self.add_sprite_to_screen(description=description,
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
        description = "cross"
        image_name = settings.CROSS_IMAGE
        return self.add_sprite_on_click(position, description, image_name)

    def add_circle_sprite_on_click(self, position: tuple[int, int]) -> int:
        """Adds a circle sprite to the 'all_sprites' pg.sprite.Group
         if the click is inside the grid and the placement is empty.
         """
        description = "circle"
        image_name = settings.CIRCLE_IMAGE
        return self.add_sprite_on_click(position, description, image_name)

    def remove_previous_turn_sprite(self):
        """Removes the previous turn GameSprite from the self.sprite_* lists and the 'all_sprites' pg.sprite.Group."""
        if not bool(self.sprite_descriptions):  # no sprites
            return
        for key, value in self.sprite_group.spritedict.items():
            if value is None:
                continue
            if value.size == (45, 45):
                del self.sprite_group.spritedict[key]
                return

    def set_turn_sprite(self, turn_description: str) -> None:
        """Changes the bottom sprite image to whoevers turn it is."""
        if len(game.sprite_descriptions):  # not first sprite
            self.remove_previous_turn_sprite()
        match turn_description:
            case "cross":
                self.add_sprite_to_screen(settings.BOTTOM_SPRITE_POSITION, "turn_sprite", settings.CROSS_IMAGE,
                                          scale=(settings.BOTTOM_SPRITE_SCALE, settings.BOTTOM_SPRITE_SCALE))
            case "circle":
                self.add_sprite_to_screen(settings.BOTTOM_SPRITE_POSITION, "turn_sprite", settings.CIRCLE_IMAGE,
                                          scale=(settings.BOTTOM_SPRITE_SCALE, settings.BOTTOM_SPRITE_SCALE))

    def run(self):
        """Runs the Tic Tac Toe game loop."""
        # initialize window scren
        screen = pg.display.set_mode(self.window_size)

        # Background, icon,and title
        background_image = pg.image.load(settings.BACKGROUND_IMAGE)
        pg.display.set_caption(settings.WINDOW_TITLE)
        pg.display.set_icon(pg.image.load(settings.ICON_IMAGE))

        # Bottom text saying whose turn it is
        text_label = "   First turn:"
        text_surface, text_rect = utils.get_turn_text_objects(text_label)

        # Bottom image showing whose turn it is, cross begins
        game.set_turn_sprite("cross")

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
                            if len(game.sprite_descriptions) < 1:
                                game.add_cross_sprite_on_click(event.pos)
                                # Replace bottom text:
                                text_label = "   Next turn:"
                                text_surface, text_rect = utils.get_turn_text_objects(text_label)
                                game.set_turn_sprite("circle")
                                continue

                            # Not first click:
                            if self.game_over:
                                continue
                            description = game.sprite_descriptions[-1]  # previous added sprite
                            if description == "turn_sprite":
                                description = game.sprite_descriptions[-2]
                            match description:
                                case "cross":
                                    if not bool(
                                            game.add_circle_sprite_on_click(event.pos)):  # try adding circle sprite
                                        game.set_turn_sprite("cross")  # Change the bottom image sprite to circle

                                case "circle":
                                    if not bool(
                                            game.add_cross_sprite_on_click(event.pos)):  # try adding cross sprite
                                        game.set_turn_sprite("circle")  # Change the bottom image sprite to cross

                        # Click within reset button:
                        reset_left_position = settings.RESET_TEXT_POSITION[0]
                        reset_right_position = reset_left_position + settings.RESET_BUTTON_SIZE[0]
                        reset_top_position = settings.RESET_TEXT_POSITION[1]
                        reset_bottom_position = reset_top_position + settings.RESET_BUTTON_SIZE[1]
                        if reset_left_position <= mouse[0] <= reset_right_position and \
                                reset_top_position <= mouse[1] <= reset_bottom_position:
                            text_surface, text_rect = game.reset()

            if (winner := game.get_winner()) is not None:
                self.game_over = True
                text_surface, text_rect = utils.get_winner_text_objects(winner)
                game.set_turn_sprite(winner)
            if game.check_full_board():
                self.game_over = True
                text_surface, text_rect = utils.get_game_over_text_objects()

            mouse = pg.mouse.get_pos()  # save mouse position for checking where next click is

            # Render reset text if its not already reset
            if text_label != "   First turn:":
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
            game.sprite_group.draw(screen)
            pg.display.update()


if __name__ == "__main__":
    game = TicTacToe(board_size=(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), grid=3)
    game.run()
    # test = [(50,20), (150,150), (20, 250), (70, 150)]
    # game.sprite_coords = test
    # # print([game.get_grid_numbers(i) for i in test])
    # result = game.get_winner()
    # print(result)
