import pygame, sys
from pygame.locals import *
from colors import *

# init pygame, the display surface and set a windowhtitle
pygame.init()
FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('PyBall')

# allowing transparency
alphaSurface = DISPLAYSURF.convert_alpha

# using fonts
fontObj = pygame.font.Font('freesansbold.ttf', 16)

# init
ballx = 50
bally = 50
#direction = 'right'
speed = 5

# main game loop
while True:
  DISPLAYSURF.fill(BGCOLOR)

  # FPS
  textSurfaceObj = fontObj.render('FPS: ' + str(int(fpsClock.get_fps())), True, BLACK, BGCOLOR)
  textRectObj = textSurfaceObj.get_rect()
  #textRectObj.top = 30
  DISPLAYSURF.blit(textSurfaceObj, textRectObj)

  # input handling
  pressed = pygame.key.get_pressed()
  if pressed[K_LEFT]:
    ballx -= speed
  if pressed[K_RIGHT]:
    ballx += speed
  if pressed[K_UP]:
    bally -= speed
  if pressed[K_DOWN]:
    bally += speed

  for event in pygame.event.get(): # tells us what events happened
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
      pygame.quit()
      sys.exit()

  pygame.draw.circle(DISPLAYSURF, RED, (ballx, bally), 20, 0)
  pygame.display.update() # draw the display surface on the screen

  fpsClock.tick(FPS)

