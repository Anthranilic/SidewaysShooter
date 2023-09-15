class Settings:
    """A class to store all settings for Sideways Shooter."""

    def __init__(self):
        """Initialize the game's settings."""

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # rocket settings
        self.rocket_speed = 5

        # bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # alien settings
        self.alien_speed = 1.0
        self.fleet_shift_left_speed = 10
        # fleet direction of 1 represents down; -1 represents up.
        self.fleet_direction = 1