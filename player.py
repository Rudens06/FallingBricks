import pygame as pg

class Player():
  def __init__(self, x, y, width, height, color):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = color
    self.rect = (x, y, width, height)
    self.velocity = 5
  
  def draw(self, win):
    pg.draw.rect(win, self.color, self.rect)
    
  def move(self):
    keys = pg.key.get_pressed()
    
    if keys[pg.K_LEFT] and self.x - self.velocity >= 0: 
      self.x -= self.velocity
    if keys[pg.K_RIGHT] and  self.x + self.velocity + self.width <= 800:
      self.x += self.velocity
    if keys[pg.K_UP] and  self.y - self.velocity >= 0:
      self.y -= self.velocity
    if keys[pg.K_DOWN] and  self.y + self.velocity + self.height <= 600:
      self.y += self.velocity
      
    self.update()
    
  def update(self):
    self.rect = (self.x, self.y, self.width, self.height)
    