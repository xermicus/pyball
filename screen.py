import pygame, sys
from pygame.locals import *
from colors import *
from quadtree import *
from gamecomponents import *
from random import randint
from pygame.math import *


class Screenmanager (object):
  screens = []

  def __init__(self, screens = []):
    self.screens = screens


  def add_screen(self, screen):
    self.screens.append(screen)


  def del_screen(self, screen):
    self.screens.remove(screen)


  def blend_in(self, newscreen):
    if self.screens[0].visible:
      self.screens[0] = Gamescreen(self)
    if self.screens[1].visible:
      self.screens[1].visible = False
      self.screens[1].hasinput = False

    newscreen.visible = True
    newscreen.hasinput = True


  #def blend_out(self, screen):
  #  screen.visible = False
  #  screen.hasinput = False


  def update(self):
    for screen in self.screens:
      if screen.hasinput:
        screen.update()


  def draw(self, display, fontObj = []):
    for screen in self.screens:
      if screen.visible:
        screen.draw(display, fontObj)



class Screen (object):
  visible = False
  hasinput = False
  manager = Screenmanager()


  def __init__(self, manager):
    self.manager = manager
    self.label = label


  def destroy(self):
    pass


  def update(self):
    pass


  def draw(self, display, fontObj = []):
    pass


class Menuscreen (Screen):
  b_game = Button("Play", (1280/2, 720/2 - 50))
  b_quit = Button("Quit", (1280/2, 720/2 + 50))
  buttons = []
  pygame.font.init()
  font_small = pygame.font.Font('freesansbold.ttf', 50)
  font_big = pygame.font.Font('freesansbold.ttf', 80)

  def __init__(self, manager):
    self.buttons.append(self.b_game)
    self.buttons.append(self.b_quit)
    self.buttons[0].focus = True


  def update(self):
    for button in self.buttons:
      button.update()

    #pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
      if (event.type == KEYUP and event.key == K_UP):
        for i in range(0, len(self.buttons)):
          if self.buttons[i].focus and i > 0:
            self.buttons[i].focus = False
            self.buttons[i - 1].focus = True
            break
      if (event.type == KEYUP and event.key == K_DOWN):
        for i in range(0, len(self.buttons)):
          if self.buttons[i].focus and i < len(self.buttons) - 1:
            self.buttons[i].focus = False
            self.buttons[i + 1].focus = True
            break
      if (event.type == KEYUP and event.key == K_SPACE):
        if self.b_game.focus:
          self.manager.blend_in(self.manager.screens[0])
        if self.b_quit.focus:
          pygame.quit()
          sys.exit()
      if (event.type == KEYUP and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()


  def draw(self, display, fontObj = []):
    for button in self.buttons:
      if button.focus:
        button.draw(display, self.font_big)
      else:
        button.draw(display, self.font_small)


class Gamescreen (Screen):
  def __init__(self, manager):
    self.player = Ball(50, 50, 15, GREEN, 5)
    self.qt = Quadtree(0, 5, 5, BLACK, Rect((0,0), (1280,720)), True)
    self.qt.insert_obj(self.player)
    self.balls = []

  def update(self):
    if not self.hasinput:
      return
    # Handle the Input
    # KEYUP input
    for event in pygame.event.get():
      if (event.type == KEYUP and event.key == K_ESCAPE):
        self.manager.blend_in(self.manager.screens[1])

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
    if not self.visible:
      return

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

