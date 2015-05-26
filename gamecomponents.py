import pygame
from colors import *

class Drawable_gamecomponent (object):
  def __init__ (self, posx, posy):
    self.posx = posx
    self.posy = posy


class Ball (object):
  def __init__ (self, posx, posy, radius, color, speed):
    self.posx = posx
    self.posy = posy
    self.radius = radius
    self.speed = speed
    self.color = color

  def get_rect(self):
    return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)
