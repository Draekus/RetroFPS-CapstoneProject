import pygame as pg

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 3, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 3, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, 3, 4, _, 4, 3, _, 1],
    [1, _, _, 5, _, _, _, _, _, _, 3, _, 3, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, 4, _, _, 4, _, _, _, 1],
    [1, 1, 3, 3, _, _, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1],
    [1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 4, _, _, 4, 3, 3, 3, 3, 3, 3, 3, 3, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


class Map:
    """Class for the map"""

    def __init__(self, game):
        """Initialize the map"""
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()

    def get_map(self):
        """Get the map"""
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        """Draw untextured map"""
        [
            pg.draw.rect(
                self.game.screen, "darkgray", (pos[0] * 100, pos[1] * 100, 100, 100), 2
            )
            for pos in self.world_map
        ]

    # Draw minimap
    def draw_minimap(self):
        # Set scale offset and size
        mini_map_scale = 8  # Adjust the scale as needed
        mini_map_offset = (self.game.screen.get_width() - self.cols * mini_map_scale, 0)
        mini_map_size = (self.cols * mini_map_scale, self.rows * mini_map_scale)

        # Draw the background rectangle
        pg.draw.rect(
            self.game.screen,
            (50, 50, 50),
            (
                mini_map_offset[0],
                mini_map_offset[1],
                mini_map_size[0],
                mini_map_size[1],
            ),
        )

        # Draw the map tiles
        for pos, value in self.world_map.items():
            mini_map_x = pos[0] * mini_map_scale + mini_map_offset[0]
            mini_map_y = pos[1] * mini_map_scale + mini_map_offset[1]
            pg.draw.rect(
                self.game.screen,
                "darkgray",
                (mini_map_x, mini_map_y, mini_map_scale, mini_map_scale),
                2,
            )

        # Draw the player marker on the mini-map
        player = self.game.player
        player_mini_map_x = int(player.x * mini_map_scale) + mini_map_offset[0]
        player_mini_map_y = int(player.y * mini_map_scale) + mini_map_offset[1]
        pg.draw.circle(
            self.game.screen, (255, 0, 0), (player_mini_map_x, player_mini_map_y), 3
        )
