import pygame
from colors import *
from pygame.math import *

RIGHT = Vector2(1, 0)
LEFT = Vector2(-1, 0)
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)


class Ball (object):
  rect = None

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


  def move(self, direction = Vector2(0, 0), quadtree = []):
    if quadtree:
      quadtree.remove_obj(self)
      self.position += direction * self.speed
      quadtree.insert_obj(self)
    else:
      self.position += direction * self.speed

  def get_postuple(self):
    return (int(self.position.x), int(self.position.y))


class Block:
  def __init__ (self, rect, color = DARKGREY):
    self.rect = rect
    self.color = color

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

  def update(self):
    #check for input?
    pass

  def draw(self, display, fontObj = []):
    if fontObj:
      textObj = fontObj.render(self.label, True, BLACK)
      textObjRect = textObj.get_rect()
      textObjRect.center = self.position
      display.blit(textObj, textObjRect)

