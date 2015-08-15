# TODO
# - Map
# - Physics
# - 2D Models
# - Shotsh
# - Sounds


import pygame, sys
from pygame.locals import *
from colors import *
from quadtree import *
from gamecomponents import *
from random import randint
from pygame.math import *
from screen import *

# init pygame, the display surface and set a windowhtitle
pygame.init()
FPS = 60 # frames per second  setting
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('PyBall')

# allowing transparency
alphaSurface = DISPLAYSURF.convert_alpha

# using fonts
fontObj = pygame.font.Font('freesansbold.ttf', 15)

# Screenmanager + Inital Menu-Scireen
manager = Screenmanager()
gamescreen = Gamescreen(manager)
manager.add_screen(gamescreen)
menuscreen = Menuscreen(manager)
manager.add_screen(menuscreen)
levelscreen = Levelscreen(manager)
manager.add_screen(levelscreen)
manager.blend_in(menuscreen)


# main game loop
while True:
  DISPLAYSURF.fill(BGCOLOR)

  # Let me know the current FPS-Rate
  pygame.display.set_caption('PyBall - FPS: ' + str(int(fpsClock.get_fps())))
  fpsClock.tick(FPS)

  # Handle Screens
  manager.update()
  manager.draw(DISPLAYSURF, fontObj)
  pygame.display.update()

