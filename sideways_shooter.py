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

13-6. Game Over: In Sideways Shooter, keep track of the number of times
the ship is hit and the number of times an alien is hit by the ship.
Decide on an appropriate condition for ending the game, and stop the game
when this situation occurs. 

14-8. Sideways Shooter, Final Version: Continue developing Sideways Shooter,
using everything we've done in this project. Add a Play button, make the game
speed up at appropriate points, and develop a scoring system. Be sure to 
refactor your code as you work, and look for opportunities to customize
the game beyond what has been shown in this chapter. 
"""

import sys, pygame
from time import sleep
from rocket import Rocket
from bullet import Bullet
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        # create an instance to store game statistics
        # and a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # start Sideways Shooter in an inactive state.
        self.game_active = False

        # make the play button
        self.play_button = Button(self, "Play")
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.rocket.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)
    
    def _rocket_hit(self):
        """Respond to the rocket being hit by an alien."""
        if self.stats.rockets_left > 0:
            # decrement rockets left and update scoreboard
            self.stats.rockets_left -= 1
            self.sb.prep_rockets()

            # get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and center the ship.
            self._create_fleet()
            self.rocket.center_rocket()

            # pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # create an alien and keep adding aliens until there's no room left.
        # spacing between aliens is one alien height and one alien width.
        alien = Alien(self)
        alien_height, alien_width = alien.rect.size

        current_y, current_x = alien_height, (self.settings.screen_width - 2 * alien_width)
        while current_x > (3 * alien_width):
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
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to any bullets and aliens that have collided."""
        # remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.rocket, self.aliens):
            self._rocket_hit()
        
        # look for aliens hitting the left of the screen.
        self._check_aliens_left()

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

        # draw the score information
        self.sb.show_score()

        # draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            # reset the game settings.
            self.settings.initialize_dynamic_settings()
            # reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_rockets()
            self.game_active = True

            # get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and center the ship.
            self._create_fleet()
            self.rocket.center_rocket()

            # hide the mouse cursor
            pygame.mouse.set_visible(False)

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
    
    def _check_aliens_left(self):
        """Check if any aliens have reached the left of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                # treat this the same as if the rocket got hit.
                self._rocket_hit()
                break

if __name__ == '__main__':
    # make a game instance, and run the game.
    ai = SidewaysShooter()
    ai.run_game()