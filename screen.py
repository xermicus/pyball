import pygame, sys
from pygame.locals import *
from colors import *
from quadtree import *
from gamecomponents import *
from random import randint
from pygame.math import *
import pickle


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
      self.screens[1] = Menuscreen(self)
    if self.screens[2].visible:
      self.screens[2] = Levelscreen(self)
      self.screens[0] = Gamescreen(self)

    newscreen.visible = True
    newscreen.hasinput = True


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
  bg_img = pygame.image.load('bg_menu.png')
  b_game = Button("Play", (1280/2, 720/2 - 100))
  b_quit = Button("Quit", (1280/2, 720/2 + 100))
  b_level = Button("Leveleditor", (1280/2, 720/2))
  buttons = []
  pygame.font.init()
  font_small = pygame.font.Font('freesansbold.ttf', 40)
  font_big = pygame.font.Font('freesansbold.ttf', 70)

  def __init__(self, manager):
    self.buttons.append(self.b_game)
    self.buttons.append(self.b_level)
    self.buttons.append(self.b_quit)
    for button in self.buttons:
      button.focus = False
    self.buttons[0].focus = True


  def update(self):
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
        if self.b_level.focus:
          self.manager.blend_in(self.manager.screens[2])
        if self.b_quit.focus:
          pygame.quit()
          sys.exit()
      if (event.type == KEYUP and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()


  def draw(self, display, fontObj = []):
    if not self.visible:
      return

    for i in range(0,3):
      for j in range(0,3):
        display.blit(self.bg_img, (540 * i, 578 * j))

    for button in self.buttons:
      if button.focus:
        button.draw(display, self.font_big)
      else:
        button.draw(display, self.font_small)


class Gamescreen (Screen):
  bg_img = pygame.image.load('bg_menu.png')
  level = []
  shots = []
  shotdir = LEFT
  shotevent = pygame.USEREVENT+1
  canshoot = True


  def __init__(self, manager):
    self.player = Ball(randint(200, 1080), -50, 15, NAVYBLUE, 5)
    self.player.direction = DOWN
    self.qt = Quadtree(0, 5, 5, BLACK, Rect((0,0), (1280,720)), True)
    self.qt.insert_obj(self.player)
    self.balls = []
    self.drawqt = False
    lvl = []
    self.level = []
    with open("lvl.txt", 'rb') as f:
      lvl = pickle.load(f)
    for block in lvl:
      self.level.append(Block(block))
      self.qt.insert_obj(Block(block))
    pygame.time.set_timer(self.shotevent, 500)

  def respawn_player(self):
    self.qt.remove_obj(self.player)
    self.player = Ball(randint(200, 1080), -50, 15, self.player.color, 5)
    self.player.direction = DOWN
    self.qt.insert_obj(self.player)

  def update(self):
    if not self.hasinput:
      return

    # Handle the Input
    pressed = pygame.key.get_pressed()
    # KEYUP input
    for event in pygame.event.get():
      if (event.type == KEYUP and event.key == K_ESCAPE):
        self.manager.blend_in(self.manager.screens[1])
      if event.type == KEYUP and (event.key == K_LEFT or event.key == K_RIGHT):
        if self.player.direction.x > 0:
          self.player.direction.x = 0.9
        else:
          self.player.direction.x = -0.9
      if event.type == self.shotevent:
        self.canshoot = True


    # PRESSED input
    if pressed[K_LEFT]:
      self.player.direction.x = -1
      self.shotdir = LEFT
    if pressed[K_RIGHT]:
      self.player.direction.x = 1
      self.shotdir = RIGHT
    if pressed[K_DOWN]:
      pass#self.player.move(Vector2(0,0.6), self.qt)
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
    # shoot
    if pressed[K_LSHIFT] and self.canshoot:
      self.canshoot = False
      new = True
      for shot in self.shots:
        if not shot.alive:
          shot.position = Vector2(self.player.get_postuple())
          shot.direction = self.shotdir
          shot.alive = True
          shot.player = self.player
          new = False
      if new:
         newshot = Shot(Vector2(self.player.get_postuple()), self.player.get_rect(), self.shotdir, True, 11, self.player)
         self.shots.append(newshot)
         #self.qt.insert_obj(newshot)

    # Gravity
    #jump
    self.player.gravity += 0.05
    #offset
    if self.player.direction.x <= 1 and self.player.direction.x >= 0:
      self.player.direction.x -= 0.04
      if self.player.direction.x < 0:
        self.player.direction.x = 0
    elif self.player.direction.x >= -1 and self.player.direction.x <= 0:
      self.player.direction.x += 0.04


    # Level Collision
    oldpos = self.player.get_rect().bottomleft
    self.player.move(self.player.direction, self.qt, self.player.gravity)
    self.player.collisions = self.qt.get_collisions(self.player)
    for colobj in self.player.collisions:
      if oldpos[1] <= colobj.get_rect().top and not pressed[K_DOWN]:
        if pressed[K_UP]:
          self.player.gravity = -2
        else:
          self.player.move(Vector2(0, self.player.direction.y * -1), self.qt, self.player.gravity)
          self.player.gravity = 0
      elif oldpos[0]+self.player.get_rect().w <= colobj.get_rect().left  or oldpos[0] >= colobj.get_rect().right:
        self.player.move(Vector2(self.player.direction.x * -1, 0), self.qt, self.player.gravity)

    # die
    if self.player.position.y >= 2500:
      self.respawn_player()
    # shoot
    for shot in self.shots:
      shot.update(self.qt)
      if self.player.get_rect().colliderect(shot.get_rect()) and shot.player == self.player:
        if shot.direction.x < 0:
          self.player.direction.x = 0.9
        else:
          self.player.direction.x = -0.9
      if self.player.get_rect().colliderect(shot.get_rect()) and shot.player != self.player:
        if shot.direction.x > 0:
          self.player.direction.x = 0.9
        else:
          self.player.direction.x = -0.9

    self.last_tick = pygame.time.get_ticks()


  def draw(self, display, fontObj = []):
    if not self.visible:
      return

    for i in range(0,3):
      for j in range(0,3):
        display.blit(self.bg_img, (540 * i, 578 * j))

    for block in self.level:
      pygame.draw.rect(display, block.color, block.get_rect())
      if self.player.get_rect().colliderect(block.get_rect()):
        self.player.color = NAVYBLUE


    # Draw the Player and Balls
    pygame.draw.circle(display, self.player.color, self.player.get_postuple(), self.player.radius, 0)
    if self.shotdir == LEFT:
      display.blit(self.player.guntex, (self.player.get_rect().left - 20, self.player.get_rect().top))
    else:
      display.blit(pygame.transform.flip(self.player.guntex, True, False), (self.player.get_rect().left + 15, self.player.get_rect().top))
    for ball in self.balls:
      if ball.alive:
        pygame.draw.circle(display, ball.color, ball.get_postuple(), ball.radius, 0)

    # shots
    for shot in self.shots:
      shot.draw(display)

    if self.drawqt:
      self.qt.draw(display, fontObj)
      for quad in self.qt.get_quads(self.player.get_rect()):
        pygame.draw.rect(display, GREEN, quad.rect, 1)




class Levelscreen (Screen):
  bg_img = pygame.image.load('bg_menu.png')
  b_safe = Button("Safe", (60, 30))
  b_quit = Button("Quit", (60, 70))
  buttons = []
  pygame.font.init()
  font_small = pygame.font.Font('freesansbold.ttf', 25)
  font_big = pygame.font.Font('freesansbold.ttf', 40)

  pos_mouse = (0,0)
  pos_new1 = (0,0)
  pos_new2 = (0,0)
  blocks = []

  def __init__(self, manager):
    self.buttons.append(self.b_safe)
    self.buttons.append(self.b_quit)
    self.buttons[0].focus = True
    self.blocks = []

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
        if self.b_safe.focus:
          with open("lvl.txt", 'wb') as f:
            for block in self.blocks:
              block.normalize()
            pickle.dump(self.blocks, f)
        if self.b_quit.focus:
          self.manager.blend_in(self.manager.screens[1])
      if (event.type == KEYUP and event.key == K_ESCAPE):
        self.manager.blend_in(self.manager.screens[1])
    # Mouse
      if (event.type == MOUSEBUTTONUP and event.button == 1):
        if self.pos_new1 == (0,0):
          self.pos_new1 = self.pos_mouse
        else:
          self.blocks.append(Rect(self.pos_new1, (self.pos_mouse[0] - self.pos_new1[0], self.pos_mouse[1] - self.pos_new1[1])))
          self.pos_new1 = (0,0)
      if event.type == MOUSEMOTION:
        self.pos_mouse = event.pos


  def draw(self, display, fontObj = []):
    if not self.visible:
      return

    # Background
    for i in range(0,3):
      for j in range(0,3):
        display.blit(self.bg_img, (540 * i, 578 * j))


    if self.pos_new1 != (0,0):
      pygame.draw.rect(display, BLACK, (self.pos_new1, (self.pos_mouse[0] - self.pos_new1[0], self.pos_mouse[1] - self.pos_new1[1])))

    for block in self.blocks:
      pygame.draw.rect(display, BLACK, block)


    for button in self.buttons:
      if button.focus:
        button.draw(display, self.font_big)
      else:
        button.draw(display, self.font_small)


    if fontObj:
      textObj = fontObj.render(str(self.pos_mouse), True, BLACK)
      textObjRect = textObj.get_rect()
      textObjRect.center = (1240,705)
      display.blit(textObj, textObjRect)
