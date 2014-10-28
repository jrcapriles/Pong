# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 23:58:44 2014

@author: Jose Capriles
"""

import Tkinter as tk


class Paddle( object ):
    
    def __init__(self, canvas, size=1, pos= [10, 10], width = 10, length = 30, color="#fb0"):
        self.size = size
        self.pos = pos
        self.width = width
        self.length = length
        self.color = color
        self.canvas = canvas
        self.paddle = self.canvas.create_rectangle(pos[0], pos[1], pos[0]+width,pos[1]+length , outline=color, fill=color)
        
    def update_position(self, delta_pos):
        self.canvas.move(self.paddle, 0, delta_pos)
        self.pos[1] += delta_pos
        
    def check_collision(self, ball_xy):
        return not (ball_xy[2]<self.pos[0] or ball_xy[3] < self.pos[1] or ball_xy[0] > self.pos[0]+self.get_width() or ball_xy[1] > self.pos[1]+self.get_length())
        
        
    def set_position(self,pos):
        self.pos = pos
        self.update()
        
    def get_position(self):
        return self.pos
        
    def set_width(self,width):
        self.width = width
        
    def get_width(self):
        return self.width
    
    def set_length(self,length):
        self.length = length
        
    def get_length(self):
        return self.length
    
    def set_color(self, color):
        self.color = color
    
    def get_paddle(self):
        return self.paddle
        