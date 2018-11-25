import pygame
MAP_TILE_WIDTH, MAP_TILE_HEIGHT = 32, 32


class Sprite(pygame.sprite.Sprite):
    """Sprite for animated items and base class for Player."""

    is_player = False

    def __init__(self, pos=(0, 0), frames=None):
        super(Sprite, self).__init__()
        if frames:
            self.frames = frames
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.animation = self.stand_animation()
        self.pos = pos

    def _get_pos(self):
        """Check the current position of the sprite on the map."""

        return ((self.rect.midbottom[0] - MAP_TILE_WIDTH / 2) // MAP_TILE_WIDTH,
                (self.rect.midbottom[1] - MAP_TILE_HEIGHT) // MAP_TILE_HEIGHT)

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""

        self.rect.midbottom = pos[0] * MAP_TILE_WIDTH + MAP_TILE_WIDTH / 2, pos[1] * MAP_TILE_HEIGHT + MAP_TILE_HEIGHT
        self.depth = self.rect.midbottom[1]

    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]

    def stand_animation(self):
        """The default animation."""

        while True:
            # Change to next frame every two ticks
            for frame in self.frames[0]:
                self.image = frame
                yield None
                yield None

    def update(self, *args):
        """Run the current animation."""

        next(self.animation)
