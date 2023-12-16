from sprite_object import *


class Weapon(AnimatedSprite):
    """Base class for all weapon objects, default sprite is a shotgun"""

    def __init__(
        self,
        game,
        path="resources/sprites/weapon/shotgun/0.png",
        scale=0.25,
        animation_time=120,
    ):
        # Derived class constructor
        super().__init__(
            game=game, path=path, scale=scale, animation_time=animation_time
        )
        # Scale the weapon images
        self.images = deque(
            [
                pg.transform.smoothscale(
                    img,
                    (self.image.get_width() * scale, self.image.get_height() * scale),
                )
                for img in self.images
            ]
        )
        # Set the weapon position to the bottom center of the screen
        self.weapon_pos = (
            HALF_WIDTH - self.images[0].get_width() // 2,
            HEIGHT - self.images[0].get_height(),
        )
        # Reloading flag
        self.reloading = False
        # Number of images in the weapon animation
        self.num_images = len(self.images)
        # Frame counter
        self.frame_counter = 0
        # Weapon damage
        self.damage = 75
        self.weapon_types = {
            "shotgun": "resources/sprites/weapon/shotgun/0.png",
            "pistol": "resources/sprites/weapon/pistol/0.png",
        }
        self.current_weapon_type = "shotgun"  # Default to 'pistol' when the game starts

    def change_weapon(self, weapon_type):
        if weapon_type in self.weapon_types:
            self.current_weapon_type = weapon_type
            self.load_images(self.weapon_types[weapon_type])

    def animate_shot(self):
        """Animate the weapon shooting"""
        # If reloading flag set
        if self.reloading:
            self.game.player.shot = False
            # If animation frame is triggered
            if self.animation_trigger:
                # Rotate the weapon images
                self.images.rotate(-1)
                # Update the weapon image
                self.image = self.images[0]
                # Increment the frame counter
                self.frame_counter += 1
                # If the animation is complete
                if self.frame_counter == self.num_images:
                    # Reset reloading flag
                    self.reloading = False
                    # Reset the frame counter
                    self.frame_counter = 0

    def draw(self):
        """Draw the weapon"""
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        """Update the weapon animation"""
        self.check_animation_time()
        self.animate_shot()
