import pygame, sys
from pygame.locals import *
from colors import *
from quadtree import *
from gamecomponents import *
from random import randint

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
qt = Quadtree(0, 6, 1, BLACK, Rect((0,0), (1280,720)), True)
player = Ball(50, 50, 20, RED, 5)
balls = []
for i in range(0, 1000):
  balls.append(Ball(randint(20, 1260), randint(20, 700), randint(5, 20), YELLOW, 0))
qt.set_objects(balls)
qt.add_object(player)
qtupdate = False

# main game loop
while True:
  DISPLAYSURF.fill(BGCOLOR)

  # FPS
  #textSurfaceObj = fontObj.render('FPS: ' + str(int(fpsClock.get_fps())), True, YELLOW, BGCOLOR)
  #textRectObj = textSurfaceObj.get_rect()
  #textRectObj.top = 30
  #DISPLAYSURF.blit(textSurfaceObj, textRectObj

  pygame.display.set_caption('PyBall - FPS: ' + str(int(fpsClock.get_fps())))

  # input handling
  pressed = pygame.key.get_pressed()
  if pressed[K_LEFT]:
    player.posx -= player.speed
    qtupdate = True
  if pressed[K_RIGHT]:
    player.posx += player.speed
    qtupdate = True
  if pressed[K_UP]:
    player.posy -= player.speed
    qtupdate = True
  if pressed[K_DOWN]:
    player.posy += player.speed
    qtupdate = True

  for event in pygame.event.get(): # tells us what events happened
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
      pygame.quit()
      sys.exit()

  if qtupdate:
    qt.update(DISPLAYSURF)
  qt.draw(DISPLAYSURF)
  #qtupdate = False

  pygame.draw.circle(DISPLAYSURF, player.color, (player.posx, player.posy), player.radius, 0)
  for ball in balls:
    pygame.draw.circle(DISPLAYSURF, ball.color, (ball.posx, ball.posy), ball.radius, 0)


  pygame.display.update() # draw the display surface on the screen

  fpsClock.tick(FPS)
