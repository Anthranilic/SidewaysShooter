import pygame
from pygame.sprite import Sprite

class Rocket(Sprite):
    """A class to manage the rocket."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load the ship image and get its rect.
        self.image = pygame.image.load('rocket_resize.png')
        self.rect = self.image.get_rect()

        # start each new ship at the middle left of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # store a float for the ship's exact vertical position.
        self.y = float(self.rect.y)

        # movement flags; start with a ship that's not moving.
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """Update the ship's position based on movement flags."""

        # update the rocket's y value, not the rect.
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.rocket_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.rocket_speed
        
        # update rect object from self.y
        self.rect.y = self.y
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_rocket(self):
        """Center the rocket on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)