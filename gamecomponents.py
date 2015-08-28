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
  ammo = -1
  nades = 10
  guntex = pygame.image.load('res/sprite/gun.png')
  guntex = pygame.transform.scale(guntex, (40,30))
  guntex = pygame.transform.flip(guntex, True, False)
  shotdir = LEFT
  canshoot = True
  acclock = False

  def __init__ (self, posx, posy, radius = 0, color = YELLOW, speed = 0, rect = None, gun = None):
    self.position = Vector2(posx, posy)
    self.radius = radius
    self.speed = speed
    self.color = color
    self.collisions = []
    self.direction = Vector2(0, 0)
    self.alive = True
    if rect:
      self.rect = rect
    self.last_ticks = pygame.time.get_ticks()
    self.gun = gun

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
  def __init__ (self, position, rect, direction, alive, speed, player, color = BLACK, tex = None):
    self.rect = rect
    self.color = color
    self.direction = direction
    self.alive = alive
    self.speed = speed
    self.position = Vector2(rect.center)
    self.player = player
    self.tex = tex
    self.number = number
    #self.explosion = pygame.USEREVENT+number
    self.exptex = pygame.image.load('res/sprite/explosion.png')
    self.last_ticks = pygame.time.get_ticks()
    self.expfps = 12
    self.exprounds = 0
    self.explode = False

    if self.tex:
      self.tex = pygame.transform.scale(self.tex, (25,25))
      self.direction = Vector2(0,1)
      self.speed = 0
      pygame.time.set_timer(self.explosion, 3000)

    self.exprects = []
    for i in range(0,4):
      for j in range(0,4):
        self.exprects.append(pygame.Rect(j * 64, i * 64, 64, 64))
    self.exprect = self.exprects[0]


  def update(self, qt):
    if self.tex and self.alive:
      #explosition
      if self.explode and pygame.time.get_ticks() > self.last_ticks + 1000 / self.expfps:
        self.last_ticks = pygame.time.get_ticks()
        self.exprect = self.exprects[self.exprounds - 1]
        self.exprounds += 1
        if self.exprounds > 16:
          self.exprounds = 0
          self.explode = False
          self.alive = False

      #collision
      oldpos = self.get_rect().bottomleft
      self.position += self.direction * self.speed
      self.rect.center = self.position
      if self.speed < 10:
        self.speed += 0.15
      if not self.rect.colliderect(pygame.Rect(0,0,1280,720)):
        self.alive = False
      collisions = qt.get_collisions(self)
      for colobj in collisions:
        if oldpos[1] <= colobj.get_rect().top and (type(colobj) is Block) and self.tex:
          self.position -= self.direction * self.speed
          self.direction = Vector2(0,0)


    elif self.alive:
      #qt.remove_obj(self)
      self.position += Vector2(self.direction.x, 0) * self.speed
      self.rect.center = self.position
      #qt.insert_obj(self)
      if not self.rect.colliderect(pygame.Rect(0,0,1280,720)):
        self.alive = False
      self.rect = pygame.Rect(self.position.x -10, self.position.y -10, 4, 4)
      collisions = qt.get_collisions(self)
      for colobj in collisions:
        if (type(colobj) is Block):
          self.alive = False


  def draw(self, display):
    if self.alive and self.tex:
      if self.explode:
        display.blit(self.exptex, self.rect, self.exprect)
      else:
        display.blit(self.tex, self.rect.center)
    elif self.alive:
        pygame.draw.circle(display, self.color, self.rect.center, 3, 0)
        #pygame.draw.rect(display, RED, self.rect)

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

class Gun (object):
  def __init__(self, tex, sound, mag, speed, spm, impact):
    self.tex = tex
    self.sound = sound
    self.mag = mag
    self.speed = speed
    self.spm = spm
    self.impact = impact
