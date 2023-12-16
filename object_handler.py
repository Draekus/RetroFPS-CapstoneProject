from sprite_object import *
from npc import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):
        """Initialize object handler"""
        self.game = game
        # Create lists for sprites and npcs
        self.sprite_list = []
        self.npc_list = []
        # Set the paths for the sprites
        self.npc_sprite_path = "resources/sprites/npc/"
        self.static_sprite_path = "resources/sprites/static_sprites/"
        self.anim_sprite_path = "resources/sprites/animated_sprites/"
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        # Create a dictionary for npc positions
        self.npc_positions = {}

        ### Add NPCs ###
        # Number of enemies to spawn
        self.enemies = 20
        # List of npc types and their spawn weights
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        # Set the restricted area for npc spawning to player spawn area
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        # Spawn npcs
        self.spawn_npc()

        ### Add static sprites ###
        # Add green candlabras
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        # Add red candlabras
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(14.5, 5.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(14.5, 7.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(12.5, 7.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(9.5, 7.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(14.5, 12.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(9.5, 20.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(10.5, 20.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(3.5, 14.5)
            )
        )
        add_sprite(
            AnimatedSprite(
                game, path=self.anim_sprite_path + "red_light/0.png", pos=(3.5, 18.5)
            )
        )
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

    def spawn_npc(self):
        """Spawn npcs"""
        # Spawn enemies
        for i in range(self.enemies):
            # Choose a random npc type based on weights
            npc = choices(self.npc_types, self.weights)[0]
            # Choose a random position for the npc
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            # Make sure the npc is not spawned in the restricted area or outside the map
            while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(
                    self.game.map.rows
                )
            # Add the npc to the npc list
            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        """Check if the player has won"""
        # Check if all npcs are dead
        if not len(self.npc_positions):
            # Draw the win screen
            self.game.object_renderer.win()
            pg.display.flip()
            # Wait 1.5 seconds
            pg.time.delay(1500)
            # Start a new game
            self.game.new_game()

    def update(self):
        """Update all sprites and npcs"""
        # Update the npc positions
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        # Update all sprites and npcs
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        # Check if the player has won
        self.check_win()

    def add_npc(self, npc):
        """Add npc to the npc list"""
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        """Add sprite to the sprite list"""
        self.sprite_list.append(sprite)
