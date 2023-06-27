import pygame as pg


class TileSprite(pg.sprite.Sprite):
    """Sprite class for the cross and circle tiles shown on the board."""

    def __init__(self,
                 sprite_type: str,
                 image_file_name: str,
                 position: tuple[int, int],
                 scale: tuple[int | float, int | float] = (1, 1),
                 anchor: str = "center"):
        pg.sprite.Sprite.__init__(self)
        self.type = sprite_type
        # image = pg.image.load(os.path.join(settings.DATA_DIR, image_file_name))
        image = pg.image.load(image_file_name)
        size = image.get_size()
        new_size = (size[0] * scale[0], size[1] * scale[1])
        self.image = pg.transform.scale(image, new_size)
        match anchor:
            case "topleft":
                self.rect = self.image.get_rect(topleft=position)
            case "topright":
                self.rect = self.image.get_rect(topright=position)
            case "bottomleft":
                self.rect = self.image.get_rect(bottomleft=position)
            case "bottomright":
                self.rect = self.image.get_rect(bottomright=position)
            case "center" | _:
                self.rect = self.image.get_rect(center=position)
