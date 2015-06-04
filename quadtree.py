import pygame, copy

class Quadtree (object):
  def __init__(self, level, maxlevel, maxobj, color, rect, render = False, parent = None):
    self.quads = []
    self.objects = []
    self.level = level
    self.maxlevel = maxlevel
    self.maxobj = maxobj
    self.color = color
    self.rect = rect
    self.render = render
    if parent:
      self.parent = parent
    else:
      self.parent = self


  def get_quads(self, rect, qlist = None, init = True):
    if init:
      qlist = []

    for quad in self.quads:
        if rect.colliderect(quad.rect):
          if not quad.quads:
            qlist.append(quad)
          quad.get_quads(rect, qlist, False)

    if not qlist:
      qlist.append(self)
    return qlist


  def insert_obj(self, obj):
    quads = self.get_quads(obj.get_rect())
    for quad in quads:
      quad.objects.append(obj)
      if len(quad.objects) > self.maxobj and quad.level < self.maxlevel:
        quad.subdivide()


  def remove_obj(self, obj):
    if obj in self.objects:
      self.objects.remove(obj)
    for quad in self.quads:
      quad.remove_obj(obj)
    self.merge()


  def merge(self):
    if self.count_objects() < self.maxobj:
      for quad in self.quads:
        for obj in quad.objects:
          if not obj in self.objects:
            self.insert_obj(obj)
      self.quads = []


  def count_objects(self):
    i = len(self.objects)
    for quad in self.quads:
      i += quad.count_objects()
    return i


  # Check for all collisions
  def get_collisions(self, obj):
    collisions = []
    quads = self.get_quads(obj.get_rect())
    for quad in quads:
      for qobj in quad.objects:
        if qobj.get_rect().colliderect(obj.get_rect()) and qobj != obj:
          collisions.append(qobj)
    return collisions


  def subdivide(self):
    for rect in self.split_rect(self.rect):
      self.quads.append(Quadtree(self.level + 1, self.maxlevel, self.maxobj, self.color, rect, self.render, self))

    for quad in self.quads:
      for obj in self.objects:
          if quad.get_rect().colliderect(obj.get_rect()):
            quad.objects.append(obj)


  def split_rect(self, rect):
    w=rect.width/2.0
    h=rect.height/2.0
    rl=[]
    rl.append(pygame.Rect(rect.left, rect.top, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top, w, h))
    rl.append(pygame.Rect(rect.left, rect.top+h, w, h))
    rl.append(pygame.Rect(rect.left+w, rect.top+h, w, h))
    return rl


  def get_rect(self):
    return self.rect


  def draw(self, display):
    pygame.draw.rect(display, self.color, self.rect, 1)
