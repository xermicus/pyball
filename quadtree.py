import pygame, copy

class Quadtree (object):
  def __init__(self, level, maxlevel, maxobj, color, rect, render = False):
    self.quads = []
    self.objects = []
    self.level = level
    self.maxlevel = maxlevel
    self.maxobj = maxobj
    self.color = color
    self.rect = rect
    self.render = render


  # Update our Tree
  def update(self, display):
    if self.level == 0:
      self.quads = []

    if len(self.objects) > self.maxobj and self.level < self.maxlevel:
      self.subdivide()
      for quad in self.quads:
        if not quad.quads:
          quad.update(display)

    if self.render and self.quads:
      self.draw(display)



  # Check for all collisions
  def get_collisions(self):
    cols = []
    for obj1 in self.objects:
      for obj2 in self.objects:
        pass

    return cols


  # Splits up the quad (and all objects)
  def subdivide(self):
    for rect in self.split_rect(self.rect):
      self.quads.append(Quadtree(self.level + 1, self.maxlevel, self.maxobj, self.color, rect, self.render))

    for quad in self.quads:
      for obj in self.objects:
          if self.get_rect().colliderect(obj.get_rect()):
            quad.objects.append(obj)


  # Splits up a rect
  def split_rect(self, rect):
    w=rect.width/2.0
    h=rect.height/2.0
    rl=[]
    rl.append(pygame.Rect(rect.left, rect.top, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top, w, h))
    rl.append(pygame.Rect(rect.left, rect.top+h, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top+h, w, h))
    return rl

  # Set new Objects
  def set_objects(self, objects):
    self.objects = objects


  # Add an Object
  def add_object(self, obj):
    self.objects.append(obj)


  # Get Rectangle
  def get_rect(self):
    return self.rect


  # Render the Quad
  def draw(self, display):
    pygame.draw.rect(display, self.color, self.rect, 2)
