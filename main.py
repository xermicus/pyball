# TODO
# - Map
# - Physics
# - Menu
# - 2D Models
# - Shots


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
fontObj = pygame.font.Font('freesansbold.ttf', 10)

# Screenmanager + Inital Menu-Screen
manager = Screenmanager()
gamescreen = Gamescreen(manager, "game")
manager.add_screen(gamescreen)
#manager.blend_in(gamescreen)
menuscreen = Menuscreen(manager, "menu")
manager.add_screen(menuscreen)
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


  # Exit Game on ESC
  # Moved to Menuscreen
  #for event in pygame.event.get():

