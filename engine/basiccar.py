# -*- encoding: utf-8 -*-

import pygame
import gameobject
import data
import xml.dom.minidom
import math

from math import *

class BasicCar(gameobject.GameObject):
    '''
    Clase "virtual pura" que abstrae el comportamiento y las características 
    básicas de los vehiculos en el juego
    '''
    def __init__(self, game_control, xml_file, x, y, angle = 0):
        '''
        Obtiene como parametro la referencia a GameControl al que pertenece
        el objeto.
        Define las principales variables.
        '''
        gameobject.GameObject.__init__(self, game_control)
        self.max_speed = None
        self.actual_speed = 0
        self.min_speed = None
        #self.__angle_rotation = None
        self.actual_angle = 0
        self.rotation_angle = None
        self.aceleration = None
        self.desaceleration = None
        self.break_force = None
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        self.parser_car_info(parser)
        self.parser_basic_info(parser)
        
        self.x = self.old_x = x
        self.y = self.old_y = y
        
        if angle == 0:
            self.dx = 0
            self.dy = 0
        else:
            self.actual_angle = angle
            self.dx = cos(angle) * self.actual_speed
            self.dy = sin(angle) * self.actual_speed
            
        self.update_position()
        self.update_image()
        
    def parser_car_info(self, parse):
        '''
        Parsea la información básica de los vehículo.
        '''
        parent_node = parse.firstChild
        self.max_speed = float(parent_node.getAttribute('max_speed'))
        self.min_speed = float(parent_node.getAttribute('min_speed'))
        self.rotation_angle = float(parent_node.getAttribute('rotation_angle'))
        self.aceleration = float(parent_node.getAttribute('aceleration'))
        self.desaceleration = float(parent_node.getAttribute('desaceleration'))
        
    def update(self):
        '''
        Método que debe ser implementado por sus descendientes
        '''
        raise NotImplemented("La funcion update de GameObject debe ser implementada por sus descendientes")
        
    def update_image(self):
        '''
        Actualiza la imagen, seleccionando la imagen actual correspondiente
        al conjutno de animaciones del estado en el q se encuentra el vehículo.
        Rotamos la imagen al angulo actual.
        Actualizamo tanto rect como mask
        '''
        self.image = pygame.transform.rotate(self.original_sprite[self.animations[self.state].get_frame()], -self.actual_angle)
        self.rect.w = self.image.get_width()
        self.rect.h = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self, delta):
        '''
        Movemos el vehículo en el sentido dado (+1 hacia delante, -1 hacia atras).
        También se encarga de no sobre pasar los limites de velocidad del coche.
        '''
        self.actual_speed += self.aceleration * delta
        
        if self.actual_speed > self.max_speed:
            self.actual_speed = self.max_speed
        elif self.actual_speed < -self.min_speed:
            self.actual_speed = -self.min_speed

    def update_position(self):
        '''
        Actualiza la posición del coche.
        '''
        self.rect.x = int(self.x) - self.rect.w / 2
        self.rect.y = int(self.y) - self.rect.h / 2
        self.x += self.dx
        self.y += self.dy

    def trigonometry(self):
        '''
        Control de rotación.
        '''
        angle = radians(self.actual_angle)
        self.dx = cos(angle) * self.actual_speed
        self.dy = sin(angle) * self.actual_speed
        
    def get_speed(self):
        '''
        Devuelve la velocidad actual del vehículo.
        '''
        return self.actual_speed
        
    def set_speed(self, new_speed):
        '''
        Recibe la nueva velocidad actual para el vehículo.
        '''
        self.actual_speed = new_speed
        
    def get_max_speed(self):
        '''
        Devuelve la velocidad máxima del vehículo.
        '''
        return self.max_speed
        
    def set_max_speed(self, new_max_speed):
        '''
        Recibe la nueva velocidad máxima del vehículo.
        '''
        self.max_speed = new_max_speed
        
    def get_min_speed(self):
        '''
        Devuelve la velocidad mínima(marcha atrás) del vehículo.
        '''
        return self.min_speed
        
    def set_min_speed(self, new_min_speed):
        '''
        Recibe la nueva velocidad mínima del vehículo.
        '''
        self.min_speed = new_min_speed
        
    def get_angle(self):
        '''
        Obtiene el ángulo actual del vehículo.
        '''
        return self.actual_angle
        
    def set_angle(self, new_angle):
        '''
        Recibe el nuevo ángulo para el vehículo
        '''
        self.actual_angle = new_angle
