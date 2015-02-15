# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:12:22 2014

@author: Jose Capriles
"""

from paddle import Paddle

class Player(object):
 
    difficulty = {"Easy": 7.5,
                  "Medium": 15,
                  "Hard": 20}   
    
    def __init__(self, canvas, name="CPU", difficulty="Medium", pos=[70,70], width = 10, height=100, color="#fb0"):
        
        self.canvas = canvas        
        self.name = name
        self.pos = pos
        self.width = width
        self.height = height
        self.turn = True
        self.color =color
        
        self.player_steps={"Up": self.difficulty[difficulty],
                           "Down": -self.difficulty[difficulty]}
        
        self.paddle = Paddle(self.canvas, 1, self.pos, self.width, self.height, self.color)
       

    def check_collision(self, ball_xy):
        return self.paddle.check_collision(ball_xy)


    def update(self, ball):
        pos = self.paddle.get_position()
        if (pos[1]>ball.get_center()[1]):
            self.paddle.update_position(self.player_steps["Up"])
        else:
            self.paddle.update_position(self.player_steps["Down"])

        
 