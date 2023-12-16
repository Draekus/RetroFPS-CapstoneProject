from settings import *
import pygame as pg
import math


class Player:
    """Player class"""

    def __init__(self, game):
        """Initialize player"""
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 500
        self.time_prev = pg.time.get_ticks()

        # diagonal movement correction
        self.diag_move_corr = 1 / math.sqrt(2)

    def recover_health(self):
        """Recover player health"""
        # Check if health recovery delay has passed and player health is less than max health
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            # Increase player health by 1
            self.health += 1

    def check_health_recovery_delay(self):
        """Check if health recovery delay has passed"""
        # Get current time
        time_now = pg.time.get_ticks()
        # Check if health recovery delay has passed
        if time_now - self.time_prev > self.health_recovery_delay:
            # Set previous time to current time
            self.time_prev = time_now
            return True

    def check_game_over(self):
        """End game if player health is 0"""
        # Check if player health is 0
        if self.health < 1:
            # Show game over screen
            self.game.object_renderer.game_over()
            pg.display.flip()
            # Wait 1.5 seconds
            pg.time.delay(1500)
            # Start new game
            self.game.new_game()

    def get_damage(self, damage):
        """Player takes damage"""
        # Subtract damage from player health
        self.health -= damage
        # Draw player damaged animation
        self.game.object_renderer.player_damage()
        # Play player pain sound
        self.game.sound.player_pain.play()
        # Check if player health is 0
        self.check_game_over()

    def single_fire_event(self, event):
        """Fire weapon on mouse click"""
        # Check if left mouse button is pressed
        if event.type == pg.MOUSEBUTTONDOWN:
            # Check if left mouse button is pressed and weapon is not reloading
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                # Play shotgun sound
                self.game.sound.shotgun.play()
                # Set shot flag
                self.shot = True
                # Set weapon reloading flag
                self.game.weapon.reloading = True

    def movement(self):
        """Player movement"""
        # calculate sin and cos of angle between player and x axis
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        # change in x position and y position
        dx, dy = 0, 0
        # speed is decoupled from fps
        speed = PLAYER_SPEED * self.game.delta_time
        # calculate speed components
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        # get key pressed events
        keys = pg.key.get_pressed()
        # keep track of how many keys are pressed
        num_key_pressed = -1

        # forward movement
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        # backward movement
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        # left movement
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        # right movement
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # diag move correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        # check for wall collision
        self.check_wall_collision(dx, dy)

        # Rotate player left if left arrow key is pressed
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # Rotate player right if right arrow key is pressed
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        # Normalize angle
        self.angle %= math.tau

    def check_wall(self, x, y):
        """Check if position is a wall"""
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        """Check if player is colliding with a wall"""
        # Set scale to decouple speed from fps
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        # Update player position if not colliding with a wall
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        """Draw 2D representation of player"""
        # Draw line representing player angle
        pg.draw.line(
            self.game.screen,
            "yellow",
            (self.x * 100, self.y * 100),
            (
                self.x * 100 + WIDTH * math.cos(self.angle),
                self.y * 100 + WIDTH * math.sin(self.angle),
            ),
            2,
        )
        # Draw circle representing player position
        pg.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        """Control player rotation with mouse"""
        # Get mouse position
        mx, my = pg.mouse.get_pos()
        # Check if mouse is outside of game window
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            # Set mouse position to center of game window
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        # Set relative mouse position
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        # Set player angle based on relative mouse position
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        """Update player"""
        # Move player
        self.movement()
        # Control player rotation with mouse
        self.mouse_control()
        # Recover player health
        self.recover_health()

    @property
    def pos(self):
        """Players 3D position"""
        return (self.x, self.y)

    @property
    def map_pos(self):
        """Players 2D map position"""
        return (int(self.x), int(self.y))
