#-*- encoding: utf-8 -*-

import gameobject
import basiccar
import math
import astar
import time

from basiccar import BasicCar
from gameobject import *
from collections import deque

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
        self.left_targets = deque()
        self.actual_target = None
        self.passed_targets = deque()
        self.no_run = False
        self.astar = astar.Astar()
        self.actual_point = None
        self.passed_points = deque()
        self.left_points = deque()
    
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
        
        if len(self.left_points) == 0 and not self.actual_point:
            print "No ai puntos, calcular"
            tiempo = time.time()
            self.left_points = self.astar.get_road(self.game_control.current_tile(self.rect), self.game_control.current_tile(self.actual_target))
            
            print "Ha tardado: ", time.time() - tiempo
            print "RESULTADO: "
            for point in self.left_points:
                print point
            
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
    
    def set_points(self, points):
        
        for key in points.keys():
            self.left_targets.append(points[key])
        
        self.actual_target = self.left_targets.popleft()
