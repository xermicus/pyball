import pygame, sys
from pygame.locals import *
from colors import *
from quadtree import *
from gamecomponents import *
from random import randint
from pygame.math import *

# init pygame, the display surface and set a windowhtitle
pygame.init()
FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('PyBall')

# allowing transparency
alphaSurface = DISPLAYSURF.convert_alpha

# using fonts
fontObj = pygame.font.Font('freesansbold.ttf', 10)

# initi content
player = Ball(50, 50, 20, RED, 5)
qt = Quadtree(0, 5, 5, BLACK, Rect((0,0), (1280,720)), True)
qt.insert_obj(player)
balls = []


# main game loop
while True:
  DISPLAYSURF.fill(BGCOLOR)

  # Let me know the current FPS-Rate
  pygame.display.set_caption('PyBall - FPS: ' + str(int(fpsClock.get_fps())))

  # Handle the Input
  pressed = pygame.key.get_pressed()
  if pressed[K_LEFT]:
    player.move(LEFT, qt)
  if pressed[K_RIGHT]:
    player.move(RIGHT, qt)
  if pressed[K_UP]:
    player.move(UP, qt)
  if pressed[K_DOWN]:
    player.move(DOWN, qt)
  if pressed[K_SPACE]:
    qt.draw(DISPLAYSURF, fontObj)
    for quad in qt.get_quads(player.get_rect()):
      pygame.draw.rect(DISPLAYSURF, GREEN, quad.rect, 1)
  if pressed[K_r]:
    if balls:
      qt.remove_obj(balls[len(balls) -1])
      balls.remove(balls[len(balls) -1])
  if pressed[K_a]:
    ball = Ball(randint(20, 1260), randint(20, 700), randint(5, 15), YELLOW, 0)
    balls.append(ball)
    qt.insert_obj(ball)
  for event in pygame.event.get():
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
      pygame.quit()
      sys.exit()


  # Collision
  player.collisions = qt.get_collisions(player)
  for colobj in player.collisions:
    colobj.color = BLUE


  # Draw the Player and Balls
  pygame.draw.circle(DISPLAYSURF, player.color, player.get_postuple(), player.radius, 0)
  for ball in balls:
    pygame.draw.circle(DISPLAYSURF, ball.color, ball.get_postuple(), ball.radius, 0)

  for colobj in player.collisions:
    colobj.color = YELLOW


  pygame.display.update()

  fpsClock.tick(FPS)
