import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        """Game initialization"""
        # create new map
        self.map = Map(self)
        # create new player
        self.player = Player(self)
        # create new object renderer
        self.object_renderer = ObjectRenderer(self)
        # create new raycaster
        self.raycasting = RayCasting(self)
        # create new object handler
        self.object_handler = ObjectHandler(self)
        # create new weapon
        self.weapon = Weapon(self)
        # create new sound
        self.sound = Sound(self)
        # create new pathfinder
        self.pathfinding = PathFinding(self)
        # play theme music
        pg.mixer.music.play(-1)

    def update(self):
        """Update everything in the game"""
        # update player
        self.player.update()
        # update raycasting
        self.raycasting.update()
        # update object handler
        self.object_handler.update()
        # update weapon
        self.weapon.update()
        pg.display.flip()
        # set delta time
        self.delta_time = self.clock.tick(FPS)
        # Display fps in window title
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        """Draw everything in the game"""
        # draw all objects
        self.object_renderer.draw()
        # draw weapon
        self.weapon.draw()
        # draw minimap
        self.map.draw_minimap()

    def check_events(self):
        """Check for events"""
        # Check if global event is triggered
        self.global_trigger = False
        for event in pg.event.get():
            # Quit game if user presses escape or closes the window
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                # Quit pygame and exit the program
                pg.quit()
                sys.exit()
            # Trigger global event
            elif event.type == self.global_event:
                self.global_trigger = True
            # Trigger player shot event
            self.player.single_fire_event(event)

    def run(self):
        """Main game loop"""
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
