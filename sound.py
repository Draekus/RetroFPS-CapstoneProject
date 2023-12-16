import pygame as pg


class Sound:
    """Class for sound effects and music"""

    def __init__(self, game):
        """Initialize sound class"""
        self.game = game
        pg.mixer.init()
        # Set the path for the sound effects
        self.path = "resources/sound/"
        # Load weapon sound effects
        self.shotgun = pg.mixer.Sound(self.path + "shotgun.wav")
        # Load NPC sound effects
        self.npc_pain = pg.mixer.Sound(self.path + "npc_pain.wav")
        self.npc_death = pg.mixer.Sound(self.path + "npc_death.wav")
        self.npc_shot = pg.mixer.Sound(self.path + "npc_attack.wav")
        # Set volume for npc shot sound effect
        self.npc_shot.set_volume(0.2)
        # Load player damaged sound effect
        self.player_pain = pg.mixer.Sound(self.path + "player_pain.wav")
        # Load theme music
        self.theme = pg.mixer.music.load(self.path + "theme.mp3")
        # Set volume for theme music
        pg.mixer.music.set_volume(0.3)
