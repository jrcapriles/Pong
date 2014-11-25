# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 23:48:51 2014

@author: Jose Capriles
"""

class Ball(object):
    
    def __init__(self, canvas, size=1, pos=[70,70], radious = 10, vel=[0,0], outline="black", fill="white"):
        
        self.size = size
        self.pos = pos
        self.previous = pos
        self.radious = radious
        self.inside = True
        self.vel = vel
        self.cpu = True
        self.gravity = False
        self.canvas = canvas
        self.ball = self.canvas.create_oval(pos[0]-radious, pos[1]-radious, pos[0]+radious,pos[1]+radious, outline=outline, fill=fill, width=2)
        self.last_player = 'None'

    def re_draw(self):
        self.canvas.coords(self.ball, self.pos[0]-self.radious, self.pos[1]-self.radious,self.pos[0]+self.radious, self.pos[1]+self.radious)
        
    def set_position(self,pos):
        self.pos = pos
        self.canvas.coords(self.ball, self.pos[0]-self.radious, self.pos[1]-self.radious,self.pos[0]+self.radious, self.pos[1]+self.radious)
        
    def get_center(self):
        return self.pos        
        
    def get_position(self):
        return [self.pos[0]-self.radious,self.pos[1]-self.radious,self.pos[0]+self.radious,self.pos[1]+self.radious]
    
    def set_radious(self, new_radious):
        self.radious = new_radious
        
    def set_velocity(self,vel):
        self.vel = vel
       
    def get_inside(self):
        return self.inside
        
    def set_inside(self,arg=None):
        if arg is None:
            self.inside = not self.inside
        else:
            self.inside = arg
        
    def get_velocity(self):
        return self.vel
  
    def set_gravity(self, y=-0.1):
        self.gravity = not self.gravity
        
        if y > 200:
            self.g_effect = -0.1
        else:
            self.g_effect = 0.1
        
    def update(self):
        
        if self.gravity:
            self.vel[1] = self.vel[1] - self.g_effect
        
        self.canvas.move(self.ball, self.vel[0], self.vel[1])
        self.pos[0] = self.pos[0] + self.vel[0]
        self.pos[1] = self.pos[1] + self.vel[1]



