import pygame as pg
from settings import *
import os
from collections import deque


class SpriteObject:
    """Base class for all sprite objects, default sprite is a candlebra"""

    def __init__(
        self,
        game,
        path="resources/sprites/static_sprites/candlebra.png",
        pos=(10.5, 3.5),
        scale=0.7,
        shift=0.27,
    ):
        # Initialize the sprite object
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        # Load the sprite image
        self.image = pg.image.load(path).convert_alpha()
        # Set the sprite image attributes
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        # Initialize the sprite projection attributes
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = (
            0,
            0,
            0,
            0,
            1,
            1,
        )
        # Initialize the sprite projection constants
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        """Create a 3D projection of the sprite"""
        # Calculate the sprite projection
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # Scale the sprite image
        image = pg.transform.scale(self.image, (proj_width, proj_height))

        # Calculate the sprite position
        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = (
            self.screen_x - self.sprite_half_width,
            HALF_HEIGHT - proj_height // 2 + height_shift,
        )

        # Add the sprite projection to the list of objects to render
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        """Get the sprite projection attributes"""
        # Calculate the sprite projection attributes based on distance to player
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy

        # Calculate the sprite projection based on angle to player
        self.theta = math.atan2(dy, dx)

        # Calculate difference between player angle and sprite angle
        delta = self.theta - self.player.angle
        # Normalize the difference between player angle and sprite angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        # Calculate the sprite projection based on normalized angle difference
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        # Calculate distance based on angle difference
        self.dist = math.hypot(dx, dy)
        # Calculate normalized distance based on angle difference
        self.norm_dist = self.dist * math.cos(delta)

        # Check if sprite is within the player's FOV
        if (
            -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH)
            and self.norm_dist > 0.5
        ):
            # Get the sprite projection
            self.get_sprite_projection()

    def update(self):
        """Update the sprite projection"""
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    """Base class for all animated sprite objects, default sprite is a green light"""

    def __init__(
        self,
        game,
        path="resources/sprites/animated_sprites/green_light/0.png",
        pos=(11.5, 3.5),
        scale=0.8,
        shift=0.16,
        animation_time=120,
    ):
        # Derived class constructor
        super().__init__(game, path, pos, scale, shift)
        # Initialize the sprite animation attributes
        self.animation_time = animation_time
        self.path = path.rsplit("/", 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        """Update the sprite animation"""
        # Update derived sprite animations
        super().update()
        # Update sprite animation
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        """Animate the sprite"""
        # If an animation frame is triggered, rotate the sprite image
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        """Check if it is time to animate the sprite"""
        self.animation_trigger = False
        # Get the current time
        time_now = pg.time.get_ticks()
        # Check if the animation time has elapsed
        if time_now - self.animation_time_prev > self.animation_time:
            # Update the animation time
            self.animation_time_prev = time_now
            # Trigger the animation frame
            self.animation_trigger = True

    def get_images(self, path):
        """Get the sprite animation images"""
        # Create a deque of sprite animation images
        images = deque()
        # Get the sprite animation image paths
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                # Load the sprite animation image
                img = pg.image.load(path + "/" + file_name).convert_alpha()
                # Add image to the deque
                images.append(img)
        return images
