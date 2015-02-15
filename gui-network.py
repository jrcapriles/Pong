# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 00:13:28 2014

@author: Jose Capriles
"""

#To do:
    #White reset
    #Gravity (chose direction depending on velocity or position of point)
    #Add timmer
    #Put a message when a power is applied (at least with switch)
    #Organize powers (not all at the same time)

from Tkinter import Tk, Canvas, Frame, Label, BOTH, LEFT, StringVar, OptionMenu, Button

from paddle import Paddle
from ball import Ball
from obstable import Obstacle
import random
import math
import socket


class PongGUI(Frame):
  
    player_1 = {'Up'  :-5, 
                'Down': 5}  
    player_2 = {'w':-5, 
                's': 5}  
                 
    cpu_level = {'Easy'  : {'Up'  :  -3,
                            'Down':   3},
                 'Medium': {'Up'  :  -9,
                            'Down':   9},
                 'Hard'  : {'Up'  : -15,
                            'Down':  15} }
    score = [0,0]
    plays =1

    cpu_enable = True
    cpu_turn = True
    buffsize = 1024

    
    #List to check all balls
    balls = []
    obs = []
 
    def __init__(self, parent,screen=[600,400]):
        Frame.__init__(self, parent)   
        self.parent = parent     
        self.bg_status = 0
        self.initUI()
        self.key_pressed = set()
        self.obstacles = set()
        
        self.bind_all('<KeyPress>', lambda event: self.key_pressed.add(event.keysym)) 
        self.bind_all('<KeyRelease>', lambda event: self.key_pressed.discard(event.keysym)) 
        
        self.bind_all('<Escape>',self.end)

        
    def end(self, event):
        self.master.destroy()
        
        
    def connect_server(self):
        self.setup = True
        host = 'localhost'
        port = 9000
        addr = (host, port)
        try: 
            self.tcpclisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcpclisock.connect(addr)
            print 'Connected to: ', addr
            self.tcpclisock.setblocking(0)
            self.parent.title("Pong Client "+'Connected to: '+ str(addr))
        except:
            print 'not able to connect to server.'
            self.create_server()

    def create_server(self):
        
        host = ''
        port = 9000
        addr = (host, port)
        self.setup = True
        
        print "makeServer():"
        
        self.tcpsersock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsersock.bind(addr)
        self.tcpsersock.listen(5)
        self.tcpclisock, addr = self.tcpsersock.accept()
        self.tcpclisock.setblocking(0)
        print 'Connected from: ', addr
        self.parent.title("Pong Server: " + 'Connected from: ' + str(addr))        


    def initUI(self):
      
        self.parent.title("Pong")        
        self.pack(fill=BOTH, expand=1)
        
        self.canvas = Canvas(self, bg="#"+str(self.bg_status)+str(self.bg_status)+str(self.bg_status))
        
        self.left = Paddle(self.canvas, 1, [30, 10], 10, 100,"#fb0")
        self.right = Paddle(self.canvas, 1, [570, 40], 10, 100,"#05f")        
        
        self.balls.append(Ball(self.canvas,1,[70,70],10,[-2,-2]))
        #self.balls.append(Ball(self.canvas,1,[100,100],10,[2,2]))
        #self.balls.append(Ball(self.canvas,1,[200,100],10,[2,-2]))
        #self.balls.append(Ball(self.canvas,1,[100,200],10,[-2,2]))
        
        self.obs.append(Obstacle(self.canvas,[200,200],"Pin",6))
        self.obs.append(Obstacle(self.canvas,[400,300],"Paddle",7))
        self.obs.append(Obstacle(self.canvas,[350,350],"Pin",4))
        self.obs.append(Obstacle(self.canvas,[210,250],"Paddle",8))
        self.obs.append(Obstacle(self.canvas,[250,250],"Size",8))
        self.obs.append(Obstacle(self.canvas,[300,350],"Switch",8))
        self.obs.append(Obstacle(self.canvas,[400,350],"Switch",8))
        self.obs.append(Obstacle(self.canvas,[420,320],"Teleport",6))
        self.obs.append(Obstacle(self.canvas,[250,200],"Gravity",8))
        self.obs.append(Obstacle(self.canvas,[300,50],"Reset",4,[0,1]))
        
        self.canvas.pack(fill=BOTH, expand=1)
        
        self.score_msg = '  Home  0 - 0  Visitor  '
        self.label_score = Label(self, text=self.score_msg, width=len(self.score_msg), bg='yellow')
        
        self.choices = ['Easy', 'Medium', 'Hard']
        self.dificulty = StringVar()
        self.dificulty.set('Medium')
        self.option = OptionMenu(self, self.dificulty, *self.choices)
        self.option.pack(side=LEFT, fill=BOTH)
        self.label_score.pack(side= LEFT, fill=BOTH)
        
        self.text = ""
        self.text_canvas = self.canvas.create_text(300,10, text=self.text, fill="white")
        
        self.after(200, self.update)
    

    def check_keys(self):
        for i in self.key_pressed:
            if i == 'w' or i == 's':
                border = self.left.get_border()
                if 270 >= (self.player_2[i] + border[1]) >=0:
                    self.left.update_position(self.player_2[i])
                
            if i == 'Up' or i == 'Down':
                border = self.right.get_border()
                if 270 >= (self.player_1[i] + border[1]) >=0:
                    self.right.update_position(self.player_1[i])            
    

    def reset(self):
        self.bg_status = 0
        self.plays = 1
        self.__dx = 2
        self.__dy = -2
        self.canvas.configure(bg="#"+str(self.bg_status)+str(self.bg_status)+str(self.bg_status))
        
        
    def check_collision(self):        
       
        #Check obstacle contacts
        for i in self.obs :
            for j in self.balls:
                
                if i.alive and i.vel is not None:
                    i.move()
                
                if i.update(j.get_position()) and j.get_inside():
                    #We have a collision!
                    
                    ball_pos = j.get_center()
                    obs_pos = i.get_position()
                    
                    if i.get_type() == 'Pin':
                        #If pin just ounce back
                        if abs(ball_pos[0] - obs_pos[0]) < abs(ball_pos[1] - obs_pos[1]):
                            j.set_velocity([ j.vel[0], -j.vel[1] ])
                        else:
                            j.set_velocity([ -j.vel[0], j.vel[1] ])
                    
                        j.set_inside(False)
                    
                        if j.get_velocity()[0]<0:
                            self.cpu_turn = True
                        else:
                            self.cpu_turn = False
                    
                    if i.get_type() == 'Size' and 'Size' not in self.obstacles:
                            self.obstacles.add('Size')
                            #Increase size of ball                        
                            self.text += "Size "
                            self.update_text()
                            i.affected = True
                            j.set_radious(20)
                            j.re_draw()
                        
                    if i.get_type() == 'Paddle':
                        #Increase size paddle
                        i.affected = True
                        if j.get_velocity()[0] < 0 and 'Paddle2' not in self.obstacles:
                            self.obstacles.add('Paddle2')
                            self.text += "Paddle2 "                            
                            self.update_text()
                            self.right.length = 150
                            self.right.re_draw()
                        elif j.get_velocity()[0] > 0 and 'Paddle1' not in self.obstacles:
                            self.obstacles.add('Paddle1')
                            self.text += "Paddle1 "                            
                            self.update_text()
                            self.left.length = 150
                            self.left.re_draw()
                    
                    if i.get_type() == 'Switch':
                        #Change controller configuration
                        i.affected = True
                        if j.get_velocity()[0] < 0 and 'Switch2' not in self.obstacles:
                            self.obstacles.add('Switch2')
                            self.text += "Switch2 "                            
                            self.update_text()
                            self.player_2['w'] = -1*self.player_2['w']
                            self.player_2['s'] = -1*self.player_2['s']
                        elif j.get_velocity()[0] > 0 and 'Switch1' not in self.obstacles:
                            self.obstacles.add('Switch1')
                            self.text += "Switch1 "                            
                            self.update_text()
                            self.player_1['Up'] = -1*self.player_1['Up']
                            self.player_1['Down'] = -1*self.player_1['Down']
                    
                    if i.get_type() == 'Teleport':
                        i.affected = True
                        j.set_position([200+int(200*random.random()), 100+int(100*random.random())])
                        j.set_velocity([j.vel[0],j.vel[1]*2*random.random()])
                        j.re_draw()
                        
                    if i.get_type() == "Reset":
                        i.affected = "True"
                        self.obstacle_reset(j)
                    
                elif not i.update(j.get_position()):
                    j.set_inside(True)
                    
                #TODO CHANGE DIRECTION OF GRAVITY RANDOMLY
                if i.get_type() == "Gravity":
                    if i.alive and 'Gravity' not in self.obstacles:
                        self.obstacles.add('Gravity')
                        self.text += "Gravity "
                        self.update_text()
                        j.set_gravity(j.pos[1])
                    elif not i.alive:
                        self.obstacles.discard('Gravity')
                        self.text = self.text.replace('Gravity ',"")
                        self.update_text()
                        if j.gravity:                        
                            j.set_gravity()
                    
    def update_text(self):
        self.canvas.delete(self.text_canvas)
        self.text_canvas = self.canvas.create_text(300,10, text=self.text, fill="white")

    def obstacle_reset(self, ball):
        self.text = ""
        self.update_text()
        
        ball.set_radious(10)
        ball.re_draw()
        self.right.length = 100
        self.right.re_draw()
        self.left.length = 100
        self.left.re_draw()
        self.player_2['w'] = -5
        self.player_2['s'] = 5
        self.player_1['Up'] = -5
        self.player_1['Down'] = 5
        
        if ball.gravity:
            ball.set_gravity()
            #ball.vel[1] = ball.vel[1]+0.1
            
        self.obstacles.clear()
                    

    def check_disable(self):
        for i in self.obs :
            for j in self.balls:
                if not i.affected:
                    if i.type_obstacle == 'Size':
                        j.set_radious(10)
                        j.re_draw()
                    if i.type_obstacle == 'Switch':
                        self.player_2['w'] = -5
                        self.player_2['s'] = 5
                        self.player_1['Up'] = -5
                        self.player_1['Down'] = 5
                    if i.type_obstacle == 'Paddle':
                        self.right.length = 100
                        self.left.length = 100
                        self.right.re_draw()
                        self.left.re_draw()
    


    def restart(self, ball, player):
        ball.set_position([300,250])
        ball.set_velocity([(-4*player)+2,(-4*player)+2])

        ball.set_radious(10)
        self.left.length = 100
        self.right.length = 100
                
        self.left.set_position(self.left.pos)
        self.right.set_position(self.right.pos)

        self.player_2['w'] = -5
        self.player_2['s'] = 5
        self.player_1['Up'] = -5
        self.player_1['Down'] = 5
                        
        if player == 1: 
            self.cpu_turn = True
        
        self.score[player] += 1
        self.update_score()
        self.reset()    

    def check_paddle_collision(self, paddle, ball):
        if paddle.check_collision(ball.get_position()):
            delta_y = ball.get_center()[1] - paddle.get_center()[1]
            ball.set_velocity([-ball.vel[0],ball.vel[1]+0.05*delta_y])
            self.plays +=1
            self.cpu_turn = not self.cpu_turn

            

    def update(self):
     
        self.check_keys()     

        self.check_collision()
        
        #self.check_disable()
        #Update new value fo the ball
        for i in self.balls:
            i.update()
            
            if not (self.plays % 5):
                print "Increasing speed"
                i.set_velocity([1.1*i.vel[0],1.1*i.vel[1]])
                self.plays = 1
                self.bg_status += 1
 
                if self.bg_status ==9:
                    self.bg_status = 0

                self.canvas.configure(bg="#"+str(self.bg_status)+str(self.bg_status)+str(self.bg_status))
                
            if i.get_position()[1] <= 0 or i.get_position()[1] >= 350:
                i.set_velocity([i.vel[0],-i.vel[1]])
       
       
            if i.get_position()[2] >= 580:
                self.obstacle_reset(i)                
                self.restart(i,0)
            elif i.get_position()[0] <= 0:
                self.obstacle_reset(i)                
                self.restart(i,1)                
                
             
            self.check_paddle_collision(self.left,i)
            
            self.check_paddle_collision(self.right,i)
 
            
        if self.cpu_turn and self.cpu_enable:
            for i in self.balls:
                pos = self.left.get_center()
                if (pos[1]>i.get_center()[1]):
                    border = self.left.get_border()
                    if border[1]>0:
                        self.left.update_position(self.cpu_level[self.dificulty.get()]['Up'])#   self.player_1["Up"])
                else:
                    border = self.left.get_border()
                    if border[3]<365:
                        self.left.update_position(self.cpu_level[self.dificulty.get()]['Down'])#self.player_1["Down"])
            
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
