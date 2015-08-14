import pygame, sys
from pygame.locals import *
from colors import *
from quadtree import *
from gamecomponents import *
from random import randint
from pygame.math import *


class Screenmanager (object):
  def __init__(self):
    self.screens = []


  def init(self, screens = []):
    self.screens = screens


  def add_screen(self, screen):
    self.screens.append(screen)

  def del_screen(self, screen):
    self.screens.remove(screen)


  def update(self):
    for screen in self.screens:
      screen.update()


  def draw(self, display, fontObj = []):
    for screen in self.screens:
      screen.draw(display, fontObj)



class Screen (object):
  def __init__(self, manager):
    self.visible = False
    self.hasinput = False
    self.manager = manager


  def update(self):
    pass


  def draw(self, display, fontObj = []):
    pass


class Menuscreen (Screen):
  def __init__(self, manager):
    pass


  def init(self):
    pass


  def update(self):
    pass


  def draw(self, display, fontObj = []):
    pass


class Gamescreen (Screen):
  def __init__(self, manager):
    pass


  def init(self):
    # init content
    self.player = Ball(50, 50, 15, GREEN, 5)
    self.qt = Quadtree(0, 5, 5, BLACK, Rect((0,0), (1280,720)), True)
    self.qt.insert_obj(self.player)
    self.balls = []

  def update(self):
    # Handle the Input
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
      self.player.move(LEFT, self.qt)
    if pressed[K_RIGHT]:
      self.player.move(RIGHT, self.qt)
    if pressed[K_UP]:
      self.player.move(UP, self.qt)
    if pressed[K_DOWN]:
      self.player.move( DOWN, self.qt)
    if pressed[K_SPACE]:
      self.drawqt = True
    else:
      self.drawqt = False
    if pressed[K_r]:
      if self.balls:
        self.qt.remove_obj(self.balls[len(self.balls) -1])
        self.balls.remove(self.balls[len(self.balls) -1])
    if pressed[K_a]:
      ball = Ball(randint(20, 1260), randint(20, 700), randint(self.player.radius - 14, self.player.radius + 10), YELLOW, 0)
      self.balls.append(ball)
      self.qt.insert_obj(ball)


    # Collision
    self.player.collisions = self.qt.get_collisions(self.player)
    for colobj in self.player.collisions:
      if self.player.radius > colobj.radius:
        self.player.radius += (int)((10 * colobj.radius) / 100)
        colobj.alive = False
        if colobj in self.balls:
          self.qt.remove_obj(colobj)
          self.balls.remove(colobj)
      else:
        self.player.color = RED

  def draw(self, display, fontObj = []):
    if self.drawqt:
      self.qt.draw(display, fontObj)
      for quad in self.qt.get_quads(self.player.get_rect()):
        pygame.draw.rect(display, GREEN, quad.rect, 1)

    # Draw the Player and Balls
    pygame.draw.circle(display, self.player.color, self.player.get_postuple(), self.player.radius, 0)
    for ball in self.balls:
      if ball.alive:
        pygame.draw.circle(display, ball.color, ball.get_postuple(), ball.radius, 0)

    for colobj in self.player.collisions:
      colobj.color = YELLOW



    pygame.display.update()

