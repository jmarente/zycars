#-*- encoding: utf-8 -*-

import gameobject
import basiccar
import math
import astar

from basiccar import BasicCar
from gameobject import *

class IA(BasicCar):
    def __init__(self, game_control, xml_file, x, y, angle = 0):
        BasicCar.__init__(self, game_control, xml_file, x, y, angle)
        
        #Simulación se Switch de C o C++.
        #Según el estado llamaremos a una función u otra.
        self.states = {
                    NORMAL: self.__normal_state,
                    RUN: self.__run_state
                    }
                                    
        self.falling = False
        self.min_scale = 0.3
        self.count_scale = 0.02
        self.actual_scale = 1
        self.target_angle = self.target_x = self.target_x = 0
        self.astar = astar.Astar()
        self.targets = None
        self.no_run = False
    
    def estimate_angle(self):
        x = self.target_x - self.rect.x
        y = self.target_y - self.rect.y
        
        if abs(x + y) > 45:
            self.no_run = False
            angle = self.update_angle2(math.degrees(math.atan2(y, x)))
            #print "Angulo: ", angle
            self.target_angle = angle
        
            '''if self.target_angle < self.actual_angle:
                self.actual_angle -= self.rotation_angle * self.max_speed
            elif self.target_angle > self.actual_angle:
                self.actual_angle += self.rotation_angle * self.max_speed'''
        
            self.actual_angle = self.target_angle
        
        else:
            self.no_run = True
    
    def update(self, element_x, element_y):
        
        self.target_x = element_x
        self.target_y = element_y
        
        #Si hemos cambiado de estado
        if self.state != self.previous_state:
            self.previous_state = self.state
            #Reiniciamos el estado
            self.animations[self.state].restart()
        
        #Llamamos a la función encargada de actualizar segun el estado
        self.states[self.state]()
        
        self.update_position()
        self.update_direction()
        self.update_image()
        
        self.update_angle()
    
    def set_targets(self, targets):
        pass
    
    def __normal_state(self):
        if self.game_control.get_state() == 'race':
            self.state = RUN
    
    def __run_state(self):
        self.estimate_angle()
        
        if not self.no_run:
            self.move(+1)
            
        self.trigonometry()
    
    def update_angle2(self, angle):
        if angle < 0:
            angle += 360
        if angle > 360:
            angle -= 360
        
        return angle
