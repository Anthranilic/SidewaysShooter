"""
12-6. Sideways Shooter. Write a game that places a ship on the left side 
of the screen and allows the player to move the ship up and down. Make
the ship fire a bullet that travels right across the screen when the
player presses the space-bar. Make sure bullets are deleted once they
disappear off the screen.

13-5. Sidways Shooter Part 2: We've come a long way since Exercise 12-6,
Sideways Shooter. For this exercise, try to develop Sideways Shooter to the
same point we've brought Alien Invasion to. Add a fleet of aliens, and make 
them move sideways toward the ship. Or, write code that places aliens at
random positions along the right side of the screen and then sends them
toward the ship. Also, write code that makes the aliens disappear when 
they're hit.
"""

import sys, pygame
from rocket import Rocket
from bullet import Bullet
from settings import Settings
from alien import Alien

class SidewaysShooter:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Sideways Shooter")

        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            print(self.settings.fleet_direction)
            self._check_events()
            self.rocket.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
            
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # create an alien and keep adding aliens until there's no room left.
        # spacing between aliens is one alien height and one alien width.
        alien = Alien(self)
        alien_height, alien_width = alien.rect.size

        current_y, current_x = alien_height, (self.settings.screen_width - 2 * alien_width)
        while current_x > (3 * alien_width):
            print(current_x)
            while current_y < (self.settings.screen_height - alien_height):
                self._create_alien(current_y, current_x)
                current_y += 2 * alien_height
            
            # finished a column; reset y value, and increment x value.
            current_y = alien_height
            current_x -= 2 * alien_width
        
    def _create_alien(self, y_position, x_position):
        """Create and alien and place it in the column."""
        new_alien = Alien(self)
        new_alien.y = y_position
        new_alien.x = x_position
        new_alien.rect.y = y_position
        new_alien.rect.x = x_position
        self.aliens.add(new_alien)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # update bullet positions.
        self.bullets.update()
        # get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= 1200:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Shift left the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_shift_left_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.rocket.blitme()
        self.aliens.draw(self.screen)

        for bullet in self.bullets.sprites():
                bullet.draw_bullet()

        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.rocket.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.rocket.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = False   

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

if __name__ == '__main__':
    # make a game instance, and run the game.
    ai = SidewaysShooter()
    ai.run_game()