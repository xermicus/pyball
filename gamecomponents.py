import pygame
from colors import *
from pygame.math import *

RIGHT = Vector2(1, 0)
LEFT = Vector2(-1, 0)
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)


class Ball (object):
  rect = None
  inblock = True
  gravity = 0
  score = 0
  ammo = -1
  guntex = pygame.image.load('gun.png')
  guntex = pygame.transform.scale(guntex, (40,30))

  def __init__ (self, posx, posy, radius = 0, color = YELLOW, speed = 0, rect = None):
    self.position = Vector2(posx, posy)
    self.radius = radius
    self.speed = speed
    self.color = color
    self.collisions = []
    self.direction = Vector2(0, 0)
    self.alive = True
    if rect:
      self.rect = rect

  def get_rect(self):
    return pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)


  def move(self, direction = Vector2(0, 0), quadtree = [], gravity = 1.0):
    if quadtree:
      quadtree.remove_obj(self)
      self.position += Vector2(direction.x, direction.y * gravity) * self.speed
      quadtree.insert_obj(self)
    else:
      self.position += Vector2(direction.x, direction.y * gravity) * self.speed

  def get_postuple(self):
    return (int(self.position.x), int(self.position.y))


class Block(object):
  def __init__ (self, rect, color = DARKGREY):
    self.rect = rect
    self.color = color

  def get_rect (self):
    return self.rect

  def get_postuple (self):
    return (int(self.rect.x), int(self.rect.y))


class Shot(object):
  def __init__ (self, position, rect, direction, alive, speed, player, color = BLACK):
    self.rect = rect
    self.color = color
    self.direction = direction
    self.alive = alive
    self.speed = speed
    self.position = Vector2(rect.center)
    self.player = player

  def update(self, qt):
    if self.alive:
      #qt.remove_obj(self)
      self.position += Vector2(self.direction.x, 0) * self.speed
      self.rect.center = self.position
      #qt.insert_obj(self)
      if not self.rect.colliderect(pygame.Rect(0,0,1280,720)):
        self.alive = False

  def draw(self, display):
    if self.alive:
        pygame.draw.circle(display, self.color, self.rect.center, 3, 0)

  def get_rect (self):
    return self.rect

  def get_postuple (self):
    return (int(self.rect.x), int(self.rect.y))

class Button (object):
  focus = False
  label = ""
  position = (0, 0)

  def __init__(self, label, position):
    self.label = label
    self.position = position

  def draw(self, display, fontObj = []):
    if fontObj:
      textObj = fontObj.render(self.label, True, BLACK)
      textObjRect = textObj.get_rect()
      textObjRect.center = self.position
      display.blit(textObj, textObjRect)

