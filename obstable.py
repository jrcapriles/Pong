# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 11:22:37 2014

@author: Jose Capriles
"""

import random
import time
from Tkinter import LAST

class Obstacle(object):
    
    
    def __init__(self, canvas, pos=[70,70],type_obstacle="Cloud", timer = 5, vel=None):
        
        self.pos = pos
        self.vel = vel
        self.canvas = canvas
        self.alive = False
        self.sized = False
        
        self.affected = False

        self.start = time.time()
        self.timer = timer
        self.type_obstacle = type_obstacle

        self.colors = {"Pin":"yellow",
                       "Size": "blue",
                       "Switch": "red",
                       "Paddle": "green",
                       "Teleport":"cyan2",
                       "Reset":"deep pink",
                       "Gravity":"saddle brown"}        
    
    def start_obstacle(self):
        self.start = time.time()
        self.r = 10# + int(10*random.random())
        self.pos = [(100 + int(400*random.random())) , (60 + int(300 * random.random()))]
        
        self.pos = [self.pos[0]-self.r, self.pos[1]-self.r, self.pos[0] + self.r, self.pos[1] + self.r]
    
        if self.type_obstacle == "Gravity":
            self.obstacle = self.canvas.create_line(self.pos[0],self.pos[1],self.pos[2],self.pos[3],arrow=LAST, fill='white')
        else:
            self.obstacle = self.canvas.create_oval(self.pos[0],self.pos[1],self.pos[2],self.pos[3], outline="black", 
                                                fill=self.colors[self.type_obstacle], width=2)
        self.alive = True
    
    def update(self, ball = None):
        if self.alive:
            if time.time()-self.start > self.timer:
                #Shutdown the obstacle
                self.canvas.delete(self.obstacle)
                self.alive = not self.alive
                self.start = time.time()
                self.affected = False
                return
                
            if ball is not None:
                return not (ball[2] < self.pos[0] or ball[3] < self.pos[1] or ball[0] > self.pos[2] or ball[1] > self.pos[3])

        else:
            if time.time()-self.start > self.timer:
                self.start_obstacle() #[self.type_obstacle]()
                return
        return
            
            
    def set_position(self,pos):
        self.pos = pos
        self.canvas.coords(self.obstacle, self.pos[0], self.pos[1],self.pos[2], self.pos[3])
        
        
    def get_position(self):
        return self.pos        
        
    def get_type(self):
        return self.type_obstacle
        
    def move(self):
        self.pos[0] = self.pos[0] + self.vel[0]
        self.pos[1] = self.pos[1] + self.vel[1]
        self.canvas.move(self.obstacle, self.vel[0], self.vel[1])
        
    