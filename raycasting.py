import pygame as pg
import math
from settings import *


class RayCasting:
    """Ray casting class"""

    def __init__(self, game):
        """Initialize ray caster"""
        self.game = game
        # Initialize ray casting result
        self.ray_casting_result = []
        # Initialize objects to render
        self.objects_to_render = []
        # Get wall textures
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        """Get objects to render based on ray casting result"""
        # Reset objects to render
        self.objects_to_render = []
        # Iterate through ray casting result
        for ray, values in enumerate(self.ray_casting_result):
            # Get ray casting result values
            depth, proj_height, texture, offset = values
            # If projection height is less than screen height
            if proj_height < HEIGHT:
                # Set wall texture
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                # Scale wall texture
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                # Set wall position
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            # If projection height is greater than screen height
            else:
                # Set height of texture
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                # Set wall texture
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),
                    HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE,
                    texture_height,
                )
                # Scale wall texture
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                # Set wall position
                wall_pos = (ray * SCALE, 0)

            # Add wall to objects to render
            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        """Cast rays to create 3D projection"""
        # Reset ray casting result
        self.ray_casting_result = []
        # Set ray origin to player position
        ox, oy = self.game.player.pos
        # Set map position to player map position
        x_map, y_map = self.game.player.map_pos

        # Define grid dimensions
        texture_vert, texture_hor = 1, 1

        # define angle of each ray cast int terms of player angle and FOV
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            ### Horizontals ###
            # Calculate y coordinate of horizontal
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a

            # Calculate x coordinate of horizontal
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            # Check for intersections between rays and horizontal lines
            for i in range(MAX_DEPTH):
                # Check if intersection is a wall
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    # Set texture of wall
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                # Increment intersection coordinates
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            ### Verticals ###
            # Calculate x coordinate of vertical
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            # Calculate y coordinate of vertical
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            # Check for intersections between ray and vertical grid lines
            for i in range(MAX_DEPTH):
                # Check if intersection is a wall
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    # Set texture of wall
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                # Increment intersection coordinates
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Choose the shortest distance & apply texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # fix fish eye effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # 3D projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # draw ray
            pg.draw.line(
                self.game.screen, "yellow", self.game.player.pos, (x_hor, y_hor)
            )

            # increment ray angle
            ray_angle += DELTA_ANGLE

    def update(self):
        """Update ray casting"""
        # Cast rays to create 3D projection
        self.ray_cast()
        # Get objects to render based on ray casting result
        self.get_objects_to_render()
