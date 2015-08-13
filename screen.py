import pygame, sys
from colors import *


class Screenmanager (object):
  def __init__(self):
    self.screens = []


  def update(self):
    for screen in self.screens():
      screen.update()


  def draw(self, display, fontObj = []):
    for screen in self.screens:
      screen.draw(display, fontObj)


class Screen (object):
  def __init__(self):
    self.visible = False
    self.hasinput = False


  def update(self):
    pass


  def draw(self, display, fontObj = []):
    pass


class Menuscreen (Screen):
  def __init__(self):
    pass

  def update(self):
    pass


  def draw(self, display, fontObj = []):
    pass


  class Gamescreen (Screen):
  def __init__(self):
    pass

  def update(self):
    pass


  def draw(self, display, fontObj = []):
    pass

