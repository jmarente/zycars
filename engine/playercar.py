#-*- encoding: utf-8 -*-

import basiccar
import gameobject
import keyboard
import data
import math
import pygame
import xml.dom.minidom

from basiccar import *
from gameobject import *
from pygame.locals import *
from math import *

class PlayerCar(BasicCar):
    '''
    Clase que modela el comportamiento y las características del vehículo del jugador
    '''
    def __init__(self, game_control, xml_file, x, y, angle = 0, player = 1):
        '''
        Recibe la referencia a game control que pertenece el objeto.
        Archivo xml con la configuración del vehículo(animaciones, características...).
        Posición x.
        Posición y.
        Ángulo del coche, teniendo en cuenta que el angulo 0 es mirando hacia la 
        derecha, se aumenta el sentido de las agujas del reloj.
        Player, si su valor es 1 se asignarán los controles de las flechas,
        si el valor es 2, w,a,s,d.
        '''
        basiccar.BasicCar.__init__(self, game_control)
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        self.parser_car_info(parser)
        self.parser_basic_info(parser)
        
        self.__assing_controls(player)
        
        self.x = x
        self.y = y
        
        if angle == 0:
            self.dx = 0
            self.dy = 0
        else:
            self.actual_angle = angle
            self.dx = cos(angle) * self.actual_speed
            self.dy = sin(angle) * self.actual_speed
            
        self.update_position()
        self.update_image()
        
        #Simulación se Switch de C o C++.
        #Según el estado llamaremos a una función u otra.
        self.states = {
                    NORMAL: self.__normal_state, 
                    NOACTION: self.__noaction_state, 
                    RUN: self.__run_state, 
                    FORWARD: self.__forward_state, 
                    REVERSE: self.__reverse_state, 
                    DAMAGED: self.__damaged_state, 
                    ERASE: self.__erase_state, 
                    YAW: self.__yaw_state
                    }
                    
    def update(self):
        '''
        Actualiza lógicamente al personaje.
        '''
        if self.state != self.previous_state :
            self.previous_state
            self.animations[self.state].restart()
            
        self.states[self.state]()
        
        self.update_position()
        self.update_image()
        
    def __normal_state(self):
        '''
        Control del estado normal, el coche esta detenido.
        '''
        if keyboard.pressed(self.UP):
            self.state = RUN
        elif keyboard.pressed(self.DOWN):
            self.state = REVERSE
            
    def __run_state(self):
        '''
        Control del estado, el coche va hacia el frente.
        '''
        self.move(+1)
        
        if keyboard.release(self.UP):
            self.state = NOACTION
        if keyboard.pressed(self.DOWN):
            self.state = REVERSE
            
        self.__control_rotation()
        
        self.__trigonometry()
            
    def __noaction_state(self):
        '''
        Control del estado, no se pulsa ningún boton de dirección.
        '''
        if keyboard.pressed(self.UP):
            state = RUN
        if keyboard.pressed(self.DOWN):
            state = REVERSE
        
        if self.actual_speed > self.desaceleration:
            self.actual_speed -= self.desaceleration
        elif self.actual_speed < -self.desaceleration:
            self.actual_speed += self.desaceleration
        else:
            self.actual_speed = 0
            self.state = NORMAL
                    
        self.__control_rotation()
            
        self.__trigonometry()
            
    def __reverse_state(self):
        '''
        Control del estado, marcha atrás.
        '''
        self.move(-1)
        
        if keyboard.release(self.DOWN):
            self.state = NOACTION
        if keyboard.pressed(self.UP):
            self.state = RUN
        
        self.__control_rotation()
        
        self.__trigonometry()
    
    def __forward_state(self):
        pass
    def __damaged_state(self):
        pass
    def __erase_state(self):
        pass
    def __yaw_state(self):
        pass
    
    def __trigonometry(self):
        '''
        Control de rotación.
        '''
        angle = radians(self.actual_angle)
        self.dx = cos(angle) * self.actual_speed
        self.dy = sin(angle) * self.actual_speed
    
    def __control_rotation(self):
        '''
        Control del cambio de dirección.
        '''
        if keyboard.pressed(self.LEFT):
            self.actual_angle -= self.rotation_angle * self.actual_speed
        elif keyboard.pressed(self.RIGHT):
            self.actual_angle += self.rotation_angle * self.actual_speed
        
    def __assing_controls(self, player):
        '''
        Asignamos los controles segun el jugador que sea.
        '''
        if player == 1:
            self.UP = K_UP
            self.DOWN = K_DOWN
            self.RIGHT = K_RIGHT
            self.LEFT = K_LEFT
        elif player == 2:
            self.UP = K_w
            self.DOWN = K_s
            self.RIGHT = K_a
            self.LEFT = K_d
    
    def __update(self):
        '''
        Movimiento básico sin actualización de estado.
        Actualmente si uso.
        '''
        if keyboard.pressed(self.LEFT):
            self.actual_angle -= self.rotation_angle * self.actual_speed
        elif keyboard.pressed(self.RIGHT):
            self.actual_angle += self.rotation_angle * self.actual_speed

        if keyboard.pressed(self.UP):
            self.move(+1)
        elif keyboard.pressed(self.DOWN):
            self.move(-1)
        else:
            # Reduce la velocidad de manera gradual.
            if self.actual_speed > self.desaceleration:
                self.actual_speed -= self.desaceleration
            elif self.actual_speed < -self.desaceleration:
                self.actual_speed += self.desaceleration
            else:
                self.actual_speed = 0

        angle = radians(self.actual_angle)
        self.dx = cos(angle) * self.actual_speed
        self.dy = sin(angle) * self.actual_speed

        self.update_position()
        self.update_image()
