# RetroFPS-CapstoneProject
This is my capstone project for my Object Oriented Programming course. It is written in Python3 and uses the PyGame library for rendering graphics. The game is pseudo-3D and utilizes raycasting along with some trigonometry in order to project the 3D game world onto the 2D space of the screen. Only the 2D engine of PyGame with tiles and sprites are used to generate what looks like a 3D world. The game is still in development, and currently only has one level, but I plan on adding more weapons, enemies, and levels.

## Running The Game
#### Prerequisites: 

In order to run the game you must have [python3](https://www.python.org/downloads/) installed as well as the [PyGame](https://www.pygame.org/wiki/GettingStarted) library which can be installed using the command 

```python3 -m pip install -U pygame --user```

To start the game just navigate to the source code directory and run the main.py file

```python3 main.py```

## Changing The Settings
You can change the resolution the game runs at as well as the mouse sensitivity by modifying the settings.py file. There are three provided resolutions and two are commented out. To use one of the other provided resolutions simply comment out the active one by putting a comment character "#" in front of it and removing the comment character from the resolution you'd like to use. You can also change the height and width to any values you like but 4:3 aspect ratios will work best. As far as changing the mouse sensitivity you will just have to play around with the value until it feels right for you. How much you have to change it will depend on your mouse's dpi. Increasing the value will make you turn faster while decreasing the value will make you turn slower.
