# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 23:48:51 2014

@author: Jose Capriles
"""

class Ball(object):
    
    def __init__(self, canvas, size=1, pos=[70,70], radious = 10, vel=[0,0], outline="black", fill="white"):
        
        self.size = size
        self.pos = pos
        self.radious = radious
        self.vel = vel
        self.canvas = canvas
        self.ball = self.canvas.create_oval(pos[0]-radious, pos[1]-radious, pos[0]+radious,pos[1]+radious, outline=outline, fill=fill, width=2)
        self.last_player = 'None'
        
    def set_position(self,pos):
        self.pos = pos
        self.canvas.coords(self.ball, self.pos[0]-self.radious, self.pos[1]-self.radious,self.pos[0]+self.radious, self.pos[1]+self.radious)
        
    def get_position(self):
        return [self.pos[0]-self.radious,self.pos[1]-self.radious,self.pos[0]+self.radious,self.pos[1]+self.radious]
        
    def set_velocity(self,vel):
        self.vel = vel
        
    def get_velocity(self):
        return self.vel
        
    def update(self, delta, last_player):
        self.last_player = last_player
        self.canvas.move(self.ball, delta[0], delta[1])
        self.pos[0] = self.pos[0] + delta[0]
        self.pos[1] = self.pos[1] + delta[1]
