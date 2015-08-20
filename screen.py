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


  def blend_in(self, newscreen, oldscreen):
    if self.screens[0].visible:
      self.screens[0] = Gamescreen(self)
    if self.screens[1].visible:
      self.screens[1] = Menuscreen(self)
    if self.screens[2].visible:
      self.screens[2] = Levelscreen(self)
      self.screens[0] = Gamescreen(self)

    oldscreen.visible = False
    oldscreen.hasinput = False
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
          self.manager.blend_in(self.manager.screens[0], self)
        if self.b_level.focus:
          self.manager.blend_in(self.manager.screens[2], self)
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
  fontObj = pygame.font.Font('freesansbold.ttf', 35)
  sps = 250


  def __init__(self, manager):
    self.player = Ball(randint(200, 1080), -50, 20, NAVYBLUE, 5, None, 1)
    self.player2 = Ball(randint(200, 1080), -50, 20, RED, 5, None, 2)
    self.player.direction = Vector2(0, 1)
    self.player2.direction = Vector2(0, 1)
    self.qt = Quadtree(0, 5, 5, BLACK, Rect((0,0), (1280,720)), True)
    self.qt.insert_obj(self.player)
    self.qt.insert_obj(self.player2)
    self.balls = []
    self.drawqt = False
    lvl = []
    self.level = []
    with open("lvl.txt", 'rb') as f:
      lvl = pickle.load(f)
    for block in lvl:
      self.level.append(Block(block))
      self.qt.insert_obj(Block(block))
    pygame.time.set_timer(self.player.shotevent, self.sps)
    pygame.time.set_timer(self.player2.shotevent, self.sps)
    self.score1 = 0
    self.score2 = 0
    self.winner = None

  def respawn_player(self):
    self.score2 += 1
    self.qt.remove_obj(self.player)
    self.player = Ball(randint(200, 1080), -50, 20, self.player.color, 5, None, self.player.number)
    self.player.direction = Vector2(0, 1)
    self.qt.insert_obj(self.player)
    pygame.time.set_timer(self.player.shotevent, self.sps)

  def respawn_player2(self):
    self.score1 += 1
    self.qt.remove_obj(self.player2)
    self.player2 = Ball(randint(200, 1080), -50, 20, self.player2.color, 5, None, self.player2.number)
    self.player2.direction = Vector2(0, 1)
    self.qt.insert_obj(self.player2)
    pygame.time.set_timer(self.player2.shotevent, self.sps)

  def process_events(self):
    for event in pygame.event.get():
      if (event.type == KEYUP and event.key == K_ESCAPE):
        self.manager.blend_in(self.manager.screens[1], self)
      if event.type == KEYUP and (event.key == K_LEFT or event.key == K_RIGHT):
        if self.player.direction.x > 0:
          self.player.direction.x = 0.9
        else:
          self.player.direction.x = -0.9
      if event.type == KEYUP and (event.key == K_a or event.key == K_d):
        if self.player2.direction.x > 0:
          self.player2.direction.x = 0.9
        else:
          self.player2.direction.x = -0.9
      if event.type == self.player.shotevent:
        self.player.canshoot = True
      if event.type == self.player2.shotevent:
        self.player2.canshoot = True
      if event.type == self.player2.shotevent:
        self.player2.canshoot = True

      for shot in self.shots:
        if event.type == shot.explosion and shot.alive:
          radius = 200
          ### FIX
          posp = self.player.get_rect().center
          poss = shot.get_rect().center
          #if posp[0] < poss[0]:
          if shot.get_rect().colliderect(self.player.get_rect().inflate(radius, radius)):
            self.player.gravity = -1.5
            if self.player.get_rect().left > shot.get_rect().right:
              self.player.direction.x = 1.4
            else:
              self.player.direction.x = -1.4
          if shot.get_rect().colliderect(self.player2.get_rect().inflate(radius, radius)):
            self.player2.gravity = -1.5
            if self.player2.get_rect().left > shot.get_rect().right:
              self.player2.direction.x = 1.4
            else:
              self.player2.direction.x = -1.4
          shot.explode = True

  def process_pressedinput(self):
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
      if not self.player.acclock:
        self.player.direction.x = -1
        self.player.shotdir = LEFT
    if pressed[K_RIGHT]:
      if not self.player.acclock:
        self.player.direction.x = 1
        self.player.shotdir = RIGHT
    # Player2
    if pressed[K_a]:
      if not self.player2.acclock:
        self.player2.direction.x = -1
        self.player2.shotdir = LEFT
    if pressed[K_d]:
      if not self.player2.acclock:
        self.player2.direction.x = 1
        self.player2.shotdir = RIGHT
    if pressed[K_SPACE]:
      self.drawqt = True
    else:
      self.drawqt = False
    if pressed[K_r]:
      pass#if self.balls:
        #self.qt.remove_obj(self.balls[len(self.balls) -1])
        #self.balls.remove(self.balls[len(self.balls) -1])
    if pressed[K_e]:
      pass#ball = Ball(randint(20, 1260), randint(20, 700), randint(self.player.radius - 14, self.player.radius + 10), YELLOW, 0)
      #self.balls.append(ball)
      #self.qt.insert_obj(ball)
    # Nades
    if pressed[K_k] and self.player.canshoot and self.player.nades > 0:
      self.player.nades -= 1
      self.player.canshoot = False
      new = True
      for shot in self.shots:
        if not shot.alive and shot.tex:
          shot.position = Vector2(self.player.get_postuple())
          shot.direction = DOWN
          shot.alive = True
          shot.player = self.player
          new = False
          pygame.time.set_timer(shot.explosion, 3000)
      if new:
        nades = []
        for shot in self.shots:
          if shot.tex:
            nades.append(shot)
        newshot = Shot(Vector2(self.player.get_postuple()), self.player.get_rect(), self.player.shotdir, True, 11, self.player, GREEN, pygame.image.load('nade.png'), len(nades)+3)
        self.shots.append(newshot)
         #self.qt.insert_obj(newshot)if pressed[K_LSHIFT] and self.canshoot:
    if pressed[K_f] and self.player2.canshoot and self.player2.nades > 0:
      self.player2.nades -= 1
      self.player2.canshoot = False
      new = True
      for shot in self.shots:
        if not shot.alive and shot.tex:
          shot.position = Vector2(self.player2.get_postuple())
          shot.direction = DOWN
          shot.alive = True
          shot.player = self.player2
          new = False
          pygame.time.set_timer(shot.explosion, 2500)
      if new:
        nades = []
        for shot in self.shots:
          if shot.tex:
            nades.append(shot)
        newshot = Shot(Vector2(self.player2.get_postuple()), self.player2.get_rect(), self.player2.shotdir, True, 11, self.player2, GREEN, pygame.image.load('nade.png'), len(nades)+3)
        self.shots.append(newshot)
         #self.qt.insert_obj(newshot)if pressed[K_LSHIFT] and self.canshoot:


  def process_components(self):
    pressed = pygame.key.get_pressed()
    if pressed[K_COMMA] and self.player.canshoot:
      self.player.canshoot = False
      new = True
      for shot in self.shots:
        if not shot.alive and not shot.tex:
          shot.position = Vector2(self.player.get_postuple())
          shot.direction = self.player.shotdir
          shot.alive = True
          shot.player = self.player
          new = False
      if new:
         newshot = Shot(Vector2(self.player.get_postuple()), self.player.get_rect(), self.player.shotdir, True, 11, self.player)
         self.shots.append(newshot)
         #self.qt.insert_obj(newshot)if pressed[K_LSHIFT] and self.canshoot:
    # Player2
    if pressed[K_LSHIFT] and self.player2.canshoot:
      self.player2.canshoot = False
      new = True
      for shot in self.shots:
        if not shot.alive and not shot.tex:
          shot.position = Vector2(self.player2.get_postuple())
          shot.direction = self.player2.shotdir
          shot.alive = True
          shot.player = self.player2
          new = False
      if new:
         newshot = Shot(Vector2(self.player2.get_postuple()), self.player2.get_rect(), self.player2.shotdir, True, 11, self.player2)
         self.shots.append(newshot)
         #self.qt.insert_obj(newshot)

    # Gravity
    #jump
    self.player.gravity += 0.05
    self.player2.gravity += 0.05
    #offset
    if self.player.direction.x <= 1.5 and self.player.direction.x >= 0:
      self.player.direction.x -= 0.04
      if self.player.direction.x < 0:
        self.player.direction.x = 0
    elif self.player.direction.x >= -1.5 and self.player.direction.x <= 0:
      self.player.direction.x += 0.04
    if self.player.direction.x > -0.3 and self.player.direction.x < 0.3:
        self.player.acclock = False
    # Player2
    if self.player2.direction.x <= 1.5 and self.player2.direction.x >= 0:
      self.player2.direction.x -= 0.04
      if self.player2.direction.x < 0:
        self.player2.direction.x = 0
    elif self.player2.direction.x >= -1.5 and self.player2.direction.x <= 0:
      self.player2.direction.x += 0.04
    if self.player2.direction.x > -0.3 and self.player2.direction.x < 0.3:
        self.player2.acclock = False

    # die
    if self.player.position.y >= 2500:
      self.respawn_player()
    if self.player2.position.y >= 2500:
      self.respawn_player2()
    # shoot
    for shot in self.shots:
      shot.update(self.qt)
      if shot.alive and not shot.tex:
        if self.player.get_rect().colliderect(shot.get_rect()) and shot.player == self.player:
          if shot.direction.x < 0:
            self.player.direction.x = 0.9
            self.player.acclock = True
          else:
            self.player.direction.x = -0.9
            self.player.acclock = True
        if self.player.get_rect().colliderect(shot.get_rect()) and shot.player != self.player:
          shot.alive = False
          if shot.direction.x > 0:
            self.player.direction.x = 1.5
            self.player.acclock = True
          else:
            self.player.direction.x = -1.5
            self.player.acclock = True
        #Player2
        if self.player2.get_rect().colliderect(shot.get_rect()) and shot.player == self.player2:
          if shot.direction.x < 0:
            self.player2.direction.x = 0.9
            self.player2.acclock = True
          else:
            self.player2.direction.x = -0.9
            self.player2.acclock = True
        if self.player2.get_rect().colliderect(shot.get_rect()) and shot.player != self.player2:
          shot.alive , self= False
          if shot.direction.x > 0:
            self.player2.direction.x = 1.5
            self.player2.acclock = True
          else:
            self.player2.direction.x = -1.5
            self.player2.acclock = True

    if self.winner:
      pygame.time.wait(2500)
      self.manager.blend_in(self.manager.screens[1], self)

    if self.score1 >= 10:
      self.winner = self.player
    elif self.score2 >= 10:
      self.winner = self.player2


  def process_collisions(self):
    pressed = pygame.key.get_pressed()
    oldpos = self.player.get_rect().bottomleft
    self.player.move(self.player.direction, self.qt, self.player.gravity)
    self.player.collisions = self.qt.get_collisions(self.player)
    for colobj in self.player.collisions:
      if oldpos[1] <= colobj.get_rect().top and not pressed[K_DOWN] and not type(colobj) == Ball:
        if pressed[K_UP]:
          self.player.gravity = -2
        else:
          self.player.move(Vector2(0, self.player.direction.y * -1), self.qt, self.player.gravity)
          self.player.gravity = 0
      elif oldpos[0]+self.player.get_rect().w < colobj.get_rect().left  or oldpos[0] > colobj.get_rect().right and not type(colobj) == Ball:
        self.player.move(Vector2(self.player.direction.x * -1, 0), self.qt, self.player.gravity)
    # Player2
    oldpos = self.player2.get_rect().bottomleft
    self.player2.move(self.player2.direction, self.qt, self.player2.gravity)
    self.player2.collisions = self.qt.get_collisions(self.player2)
    for colobj in self.player2.collisions:
      if oldpos[1] <= colobj.get_rect().top and not pressed[K_s] and not type(colobj) == Ball:
        if pressed[K_w]:
          self.player2.gravity = -2
        else:
          self.player2.move(Vector2(0, self.player2.direction.y * -1), self.qt, self.player2.gravity)
          self.player2.gravity = 0
      elif oldpos[0]+self.player2.get_rect().w < colobj.get_rect().left  or oldpos[0] > colobj.get_rect().right and not type(colobj) == Ball:
        self.player2.move(Vector2(self.player2.direction.x * -1, 0), self.qt, self.player2.gravity)


  def update(self):
    if not self.hasinput:
      return

    self.process_events()
    self.process_pressedinput()
    self.process_components()
    self.process_collisions()


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
    pygame.draw.circle(display, self.player2.color, self.player2.get_postuple(), self.player2.radius, 0)
    if self.player.shotdir == LEFT:
      display.blit(self.player.guntex, (self.player.get_rect().left - 20, self.player.get_rect().top))
    else:
      display.blit(pygame.transform.flip(self.player.guntex, True, False), (self.player.get_rect().left + 15, self.player.get_rect().top))
    if self.player2.shotdir == LEFT:
      display.blit(self.player2.guntex, (self.player2.get_rect().left - 20, self.player2.get_rect().top))
    else:
      display.blit(pygame.transform.flip(self.player2.guntex, True, False), (self.player2.get_rect().left + 15, self.player2.get_rect().top))


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

    textObj = self.fontObj.render(str(self.score1), True, self.player.color)
    textObjRect = textObj.get_rect()
    textObjRect.center = (1280/2 - 50,40)
    display.blit(textObj, textObjRect)
    textObj = self.fontObj.render(str(self.score2), True, self.player2.color)
    textObjRect = textObj.get_rect()
    textObjRect.center = (1280/2 + 50,40)
    display.blit(textObj, textObjRect)

    if self.winner == self.player:
      textObj = self.fontObj.render("Player 1 wins!", True, self.player.color)
      textObjRect = textObj.get_rect()
      textObjRect.center = (1280/2,90)
      display.blit(textObj, textObjRect)
    elif self.winner == self.player2:
      textObj = self.fontObj.render("Player 2 wins!", True, self.player2.color)
      textObjRect = textObj.get_rect()
      textObjRect.center = (1280/2,90)
      display.blit(textObj, textObjRect)



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
        if self.b_safe.focus:
          with open("lvl.txt", 'wb') as f:
            for block in self.blocks:
              block.normalize()
            pickle.dump(self.blocks, f)
        if self.b_quit.focus:
          self.manager.blend_in(self.manager.screens[1], self)
      if (event.type == KEYUP and event.key == K_ESCAPE):
        self.manager.blend_in(self.manager.screens[1], self)
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
