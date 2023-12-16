import pygame as pg
from settings import *


class ObjectRenderer:
    """Class for rendering game objects"""

    def __init__(self, game):
        """Initialize object renderer"""
        self.game = game
        self.screen = game.screen
        # Load wall textures
        self.wall_textures = self.load_wall_textures()
        # Load sky image
        self.sky_image = self.get_texture(
            "resources/textures/sky.png", (WIDTH, HALF_HEIGHT)
        )
        # Initialize sky offset
        self.sky_offset = 0
        # Load blood screen image
        self.blood_screen = self.get_texture("resources/textures/blood_screen.png", RES)
        # Set digit size
        self.digit_size = 90
        # Load digit images
        self.digit_images = [
            self.get_texture(
                f"resources/textures/digits/{i}.png", [self.digit_size] * 2
            )
            for i in range(11)
        ]
        # Create dictionary of digit images
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        # Load game over and win images
        self.game_over_image = self.get_texture("resources/textures/game_over.png", RES)
        self.win_image = self.get_texture("resources/textures/win.png", RES)

    def draw(self):
        """Draw the game objects"""
        # Draw the background
        self.draw_background()
        # Draw the game objects
        self.render_game_objects()
        # Draw the player health
        self.draw_player_health()

    def win(self):
        """Draw the win screen"""
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        """Draw the game over screen"""
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        """Draw the player health"""
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits["10"], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        """Draw the bloody screen"""
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        """Draw the background"""
        # Set sky offset based on player position & screen width
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        # Draw sky box
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # Draw the floor using solid rectangles
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        """Render game objects to the screen"""
        # Sort objects to render by depth
        list_objects = sorted(
            self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True
        )
        # Draw objects to screen
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """Get a texture from a file"""
        # Load the texture
        texture = pg.image.load(path).convert_alpha()
        # Scale the texture and return it
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        """Load wall textures"""
        # Return a dictionary of wall textures that maps minimap values to textures
        return {
            1: self.get_texture("resources/textures/1.png"),
            2: self.get_texture("resources/textures/2.png"),
            3: self.get_texture("resources/textures/3.png"),
            4: self.get_texture("resources/textures/4.png"),
            5: self.get_texture("resources/textures/5.png"),
        }
