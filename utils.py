import pygame as pg

import settings


def section_of_number(number: int,
                      total_width: int | float,
                      no_sections: int) -> int | None:
    """Returns whichever integer section a number is between for a total window width."""
    for i in range(no_sections):
        section_width = total_width / no_sections
        if (section_width * i) < number <= (section_width * (i + 1)):
            return i + 1


def get_turn_text_objects(text: str) -> tuple[pg.Surface, pg.Rect]:
    """Returns pg.Surface and pg.Rect for the given text positioned at the bottom of the window."""
    font = pg.font.SysFont(settings.FONT, settings.FONT_SIZE)
    text_surface = font.render(text, True, settings.FONT_COLOR, settings.FONT_BG_COLOR)
    text_rect = text_surface.get_rect(topleft=settings.TEXT_POSITION)
    return text_surface, text_rect


def get_winner_text_objects(winner_string: str) -> tuple[pg.Surface, pg.Rect]:
    """Returns pg.Surface and pg.Rect for the reset button text."""
    match winner_string:
        case "circle":
            winner_font_color = "blue"
        case "cross" | _:
            winner_font_color = "red"
    winner_font = pg.font.SysFont(settings.FONT, settings.FONT_SIZE)
    text_surface = winner_font.render(f"{winner_string.capitalize()} wins!", True, winner_font_color)
    text_rect = text_surface.get_rect(topleft=settings.TEXT_POSITION)
    return text_surface, text_rect

def get_game_over_text_objects() -> tuple[pg.Surface, pg.Rect]:
    """Returns pg.Surface and pg.Rect for the bottom text for when there is no more legal moves."""
    game_over_font = pg.font.SysFont(settings.FONT, settings.FONT_SIZE)
    text_surface = game_over_font.render("Game over!", True, settings.GAME_OVER_FONT_COLOR)
    text_rect = text_surface.get_rect(topleft=settings.TEXT_POSITION)
    return text_surface, text_rect


def get_reset_text_objects() -> tuple[pg.Surface, pg.Rect]:
    """Returns pg.Surface and pg.Rect for the reset button text."""
    reset_font = pg.font.SysFont(settings.RESET_FONT, settings.RESET_FONT_SIZE)
    text_surface = reset_font.render("RESET", True, settings.RESET_FONT_COLOR)
    text_rect = text_surface.get_rect(center=settings.RESET_TEXT_POSITION)
    return text_surface, text_rect

