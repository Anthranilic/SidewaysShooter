import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a sinlge alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load the alien image and set its rect attribute.
        self.image = pygame.image.load('alien.bmp')
        self.rect = self.image.get_rect()

        # start each new alien near the far right of the screen.
        self.rect.x = self.settings.screen_width + self.rect.width
        self.rect.y = 0 + self.rect.height

        # store the alien's exact vertical position.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0)

    def update(self):
        """Move the alien up or down."""
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y