# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 00:13:28 2014

@author: joser
"""

from Tkinter import Tk, Canvas, Frame, Label, BOTH, LEFT, StringVar, OptionMenu, Button

from paddle import Paddle
from ball import Ball
#from player import Player

class PongGUI(Frame):
  
    player_1 = {'Up':-15, 
                 'Down': 15}  
    player_2 = {'w':-15, 
                 's': 15}  
                 
    cpu_level = {'Easy'  : {'Up'  : -3,
                            'Down':  3},
                 'Medium': {'Up'  : -9,
                            'Down':  9},
                 'Hard'  : {'Up'  : -15,
                            'Down': 15} }
    score = [0,0]
    plays =1
    __dx = -2
    __dy = -2
    cpu = True
 
    def __init__(self, parent,screen=[600,400]):
        Frame.__init__(self, parent)   
        self.parent = parent     
        self.bg_status = 0
        self.initUI()
        self.bind_all('<Key>', self.key)
        
    def initUI(self):
      
        self.parent.title("Pong")        
        self.pack(fill=BOTH, expand=1)
        
        self.canvas = Canvas(self, bg="#"+str(self.bg_status)+str(self.bg_status)+str(self.bg_status))
        
        self.left = Paddle(self.canvas, 1, [30, 10], 10, 100,"#fb0")
        self.right = Paddle(self.canvas, 1, [570, 40], 10, 100,"#05f")        
        
        #self.right = Player(self.canvas, "CPU", "Medium", [570,10], 10, 100, "#05f")

        self.ball = Ball(self.canvas,1,[70,70],10)        
                
        self.canvas.pack(fill=BOTH, expand=1)
        
        self.score_msg = '  Home  0 - 0  Visitor  '
        self.label_score = Label(self, text=self.score_msg, width=len(self.score_msg), bg='yellow')
        
        
        self.choices = ['Easy', 'Medium', 'Hard']
        self.dificulty = StringVar()
        self.dificulty.set('Medium')
        self.option = OptionMenu(self, self.dificulty, *self.choices)
        self.option.pack(side=LEFT, fill=BOTH)
        self.label_score.pack(side= LEFT, fill=BOTH)
        
        self.after(200, self.update)

    
    def key(self, event):
        #Check for key pressed
        if event.keysym == 'w' or event.keysym == 's':
            self.left.update_position(self.player_2[event.keysym])
                
        if event.keysym == 'Up':
            border = self.right.get_border()
            if border[1]>=0:
                self.right.update_position(self.player_1[event.keysym])            
                
        if event.keysym == 'Down':
            border = self.right.get_border()
            if border[3]<=375:
                self.right.update_position(self.player_1[event.keysym])            
           
            #self.update_right(self.player_1[event.keysym])

    def reset(self):
        self.bg_status = 0
        self.plays = 1
        self.__dx = 2
        self.__dy = -2
        self.canvas.configure(bg="#"+str(self.bg_status)+str(self.bg_status)+str(self.bg_status))
        
    def update(self):
     
        #Update new value fo the ball
        self.ball.update([self.__dx,self.__dy],"")        
        
        if not (self.plays % 5):
            print "Increasing speed"
            self.__dx += 0.125*self.__dx             
            self.__dy += 0.125*self.__dy             
            self.plays = 1
            self.bg_status += 1

            if self.bg_status ==9:
                self.bg_status = 0

            self.canvas.configure(bg="#"+str(self.bg_status)+str(self.bg_status)+str(self.bg_status))
            

            
        if self.cpu:
            pos = self.left.get_center()
            if (pos[1]>self.ball.get_center()[1]):
                border = self.left.get_border()
                if border[1]>0:
                    self.left.update_position(self.cpu_level[self.dificulty.get()]['Up'])#   self.player_1["Up"])
            else:
                border = self.left.get_border()
                if border[3]<375:
                    self.left.update_position(self.cpu_level[self.dificulty.get()]['Down'])#self.player_1["Down"])
            
                
        #Bounce top
        if self.ball.get_position()[1] <= 0:
            self.__dy = -self.__dy
            
        #Bounce bottom
        if self.ball.get_position()[1] >= 360: #self.winHEIGHT:
            self.__dy = -self.__dy
            
        #Collision with paddle
        if self.left.check_collision(self.ball.get_position()) or self.right.check_collision(self.ball.get_position()):
            self.__dx = -self.__dx
            self.plays +=1
            self.cpu = not self.cpu

        if self.ball.get_position()[0] <= 0:
            self.__dx = -self.__dx
            self.score[1] += 1
            self.update_score()
            self.ball.set_position([300,200])
            self.reset()
            
        if self.ball.get_position()[2] >= 580:
            self.__dx = -self.__dx
            self.score[0] += 1
            self.update_score()
            self.ball.set_position([300,200])
            self.reset()    
            
        self.after(10, self.update)
 
    def update_score(self):
        self.label_score['text']=self.score_msg[:8]+str(self.score[0])+self.score_msg[9:12]+str(self.score[1])+self.score_msg[13:]
        self.label_score.update()

def main():

    screen=[600,400]  
    root = Tk()
    
    pong = PongGUI(root,screen)
    
    root.geometry(str(screen[0])+"x"+str(screen[1])+"+500+300")
    root.mainloop()  


if __name__ == '__main__':
    main() 