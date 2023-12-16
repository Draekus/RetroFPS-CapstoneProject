from sprite_object import *
from random import randint, random


class NPC(AnimatedSprite):
    """Base class for all npc objects, default sprite is a soldier"""

    def __init__(
        self,
        game,
        path="resources/sprites/npc/soldier/0.png",
        pos=(10.5, 5.5),
        scale=0.6,
        shift=0.38,
        animation_time=180,
    ):
        # Derived class constructor
        super().__init__(game, path, pos, scale, shift, animation_time)
        # Load attack images
        self.attack_images = self.get_images(self.path + "/attack")
        # Load death images
        self.death_images = self.get_images(self.path + "/death")
        # Load idle images
        self.idle_images = self.get_images(self.path + "/idle")
        # Load pain images
        self.pain_images = self.get_images(self.path + "/pain")
        # Load walk images
        self.walk_images = self.get_images(self.path + "/walk")

        # Set the distance at which the npc will attack the player
        self.attack_dist = randint(3, 6)
        # Set the npc speed
        self.speed = 0.03
        # Set the npc size
        self.size = 20
        # Set the npc health
        self.health = 100
        # Set the npc attack damage
        self.attack_damage = 10
        # Set the npc accuracy
        self.accuracy = 0.15
        # Set the npc alive flag
        self.alive = True
        # Set the npc pain flag
        self.pain = False
        # Initialize the npc ray cast value
        self.ray_cast_value = False
        # Initialize frame counter
        self.frame_counter = 0
        # Set pathfinding trigger flag
        self.player_search_trigger = False

    def update(self):
        """Update the npc"""
        # Check if the animation time has passed
        self.check_animation_time()
        # Get npc sprite
        self.get_sprite()
        # Run npc logic
        self.run_logic()
        # self.draw_ray_cast()

    def check_wall(self, x, y):
        """Check if the specified position is a wall"""
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        """Check if npc is colliding with a wall"""
        # Update npc position if not colliding with a wall
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        """Move the npc"""
        # Get the next position from the pathfinding algorithm
        next_pos = self.game.pathfinding.get_path(
            self.map_pos, self.game.player.map_pos
        )
        # Set next x and y coordinates
        next_x, next_y = next_pos

        # Make sure another npc is not occupying the next position
        if next_pos not in self.game.object_handler.npc_positions:
            # Set the npc movement direction
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            # Calculate the npc's next position based on the npc's speed
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            # Check if the new position will cause a collision with a wall
            self.check_wall_collision(dx, dy)

    def attack(self):
        """Attack the player"""
        # Check if the animation trigger is active
        if self.animation_trigger:
            # Play the npc attack sound
            self.game.sound.npc_shot.play()
            # Apply the npc's accuracy to the attack
            if random() < self.accuracy:
                # Apply damage to player
                self.game.player.get_damage(self.attack_damage)

    def animate_death(self):
        """Animate the npc death"""
        # Check if the npc is dead
        if not self.alive:
            # Only play the animation once
            if (
                self.game.global_trigger
                and self.frame_counter < len(self.death_images) - 1
            ):
                # Rotate the npc death images
                self.death_images.rotate(-1)
                # Update the current npc image
                self.image = self.death_images[0]
                # Increment the frame counter
                self.frame_counter += 1

    def animate_pain(self):
        """Animate the npc being damaged"""
        # Run the npc pain animation
        self.animate(self.pain_images)
        # Check if the animation trigger is active
        if self.animation_trigger:
            # Set the pain flag to false
            self.pain = False

    def check_hit_in_npc(self):
        """Check if the npc has been hit by the player"""
        # If the npc can be hit by the player and the player has shot
        if self.ray_cast_value and self.game.player.shot:
            # Check if the player is facing the npc
            if (
                HALF_WIDTH - self.sprite_half_width
                < self.screen_x
                < HALF_WIDTH + self.sprite_half_width
            ):
                # Play the npc pain sound
                self.game.sound.npc_pain.play()
                # Set player shot flag to false
                self.game.player.shot = False
                # Set the npc pain flag to true
                self.pain = True
                # Apply damage to npc
                self.health -= self.game.weapon.damage
                # Check if npc is dead
                self.check_health()

    def check_health(self):
        """Check if the npc is dead"""
        # Check if npc health is less than 1
        if self.health < 1:
            # Set npc alive flag to false
            self.alive = False
            # Play the npc death sound
            self.game.sound.npc_death.play()

    def run_logic(self):
        """Run the npc's main logic loop"""
        # Check if the npc is alive
        if self.alive:
            # Check if the npc is in the player's FOV
            self.ray_cast_value = self.ray_cast_player_npc()
            # Check if the npc has been hit by the player
            self.check_hit_in_npc()

            # Check if the npc pain flag is set
            if self.pain:
                # Run the npc pain animation
                self.animate_pain()

            # Check if the player is in the npc's FOV
            elif self.ray_cast_value:
                # Set the npc pathfinding trigger flag to true
                self.player_search_trigger = True

                # If the npc is within the attack distance
                if self.dist < self.attack_dist:
                    # Run the npc attack animation
                    self.animate(self.attack_images)
                    # Run the npc attack logic
                    self.attack()
                # If the npc is not within the attack distance
                else:
                    # Run the npc walk animation
                    self.animate(self.walk_images)
                    # Run the npc movement logic
                    self.movement()
            # If the pathfinding trigger flag is set
            elif self.player_search_trigger:
                # Run the npc walk animation
                self.animate(self.walk_images)
                # Run the npc movement logic
                self.movement()
            # Otherwise
            else:
                # Run the npc idle animation
                self.animate(self.idle_images)
        # If the npc is dead
        else:
            # Run the npc death animation
            self.animate_death()

    @property
    def map_pos(self):
        """Return the npc's map position"""
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        """Check if the npc is in the player's FOV"""
        # If the player & npc are in the same map position
        if self.game.player.map_pos == self.map_pos:
            # Return true
            return True

        # Initialize the player & wall verticals and horizontals
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        # Set the ray origin to the player's position
        ox, oy = self.game.player.pos
        # Set the map position to the player's map position
        x_map, y_map = self.game.player.map_pos
        # Set the ray angle to the npc's angle
        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        ### horizontals ###
        # Initialize the horizontal y coordinate and delta y
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        # Calculate the horizontal depth
        depth_hor = (y_hor - oy) / sin_a
        # Calculate the horizontal x coordinate
        x_hor = ox + depth_hor * cos_a
        # Calculate the horizontal delta depth and delta x
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        # Check for intersections between rays and horizontal lines
        for i in range(MAX_DEPTH):
            # Set the horizontal tile
            tile_hor = int(x_hor), int(y_hor)
            # If the horizontal tile is the npc's map position
            if tile_hor == self.map_pos:
                # Set the player distance to the horizontal depth
                player_dist_h = depth_hor
                break
            # If the horizontal tile is a wall
            if tile_hor in self.game.map.world_map:
                # Set the wall distance to the horizontal depth
                wall_dist_h = depth_hor
                break
            # Increment the horizontal intersection coordinates
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        ### verticals ###
        # Initialize the vertical x coordinate and delta x
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        # Calculate the vertical depth
        depth_vert = (x_vert - ox) / cos_a
        # Calculate the vertical y coordinate
        y_vert = oy + depth_vert * sin_a
        # Calculate the vertical delta depth and delta y
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        # Check for intersections between rays and vertical lines
        for i in range(MAX_DEPTH):
            # Set the vertical tile
            tile_vert = int(x_vert), int(y_vert)
            # If the vertical tile is the npc's map position
            if tile_vert == self.map_pos:
                # Set the player distance to the vertical depth
                player_dist_v = depth_vert
                break
            # If the vertical tile is a wall
            if tile_vert in self.game.map.world_map:
                # Set the wall distance to the vertical depth
                wall_dist_v = depth_vert
                break
            # Increment the vertical intersection coordinates
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        # Set the player distance to the max of the vertical and horizontal distances
        player_dist = max(player_dist_v, player_dist_h)
        # Set the wall distance to the max of the vertical and horizontal distances
        wall_dist = max(wall_dist_v, wall_dist_h)

        # Check if the player distance is less than the wall distance
        if 0 < player_dist < wall_dist or not wall_dist:
            # Return True
            return True
        # Otherwise
        # Return False
        return False

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, "red", (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(
                self.game.screen,
                "orange",
                (100 * self.game.player.x, 100 * self.game.player.y),
                (100 * self.x, 100 * self.y),
                2,
            )


class SoldierNPC(NPC):
    """Soldier npc sprite"""

    def __init__(
        self,
        game,
        path="resources/sprites/npc/soldier/0.png",
        pos=(10.5, 5.5),
        scale=0.6,
        shift=0.38,
        animation_time=180,
    ):
        super().__init__(game, path, pos, scale, shift, animation_time)


class CacoDemonNPC(NPC):
    """Caco demon npc sprite"""

    def __init__(
        self,
        game,
        path="resources/sprites/npc/caco_demon/0.png",
        pos=(10.5, 6.5),
        scale=0.7,
        shift=0.27,
        animation_time=250,
    ):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35


class CyberDemonNPC(NPC):
    """Cyber demon npc sprite"""

    def __init__(
        self,
        game,
        path="resources/sprites/npc/cyber_demon/0.png",
        pos=(11.5, 6.0),
        scale=1.0,
        shift=0.04,
        animation_time=210,
    ):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25
