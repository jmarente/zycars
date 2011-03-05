# -*- encoding: utf-8 -*-

import pygame
import gameobject
import data
import xml.dom.minidom
import math

from math import *

class BasicCar(gameobject.GameObject):
    '''
    @brief Clase "virtual pura" que abstrae el comportamiento y las características 
    básicas de los vehiculos en el juego
    '''
    def __init__(self, game_control, xml_file, x, y, angle = 0):
        '''
        @brief Constructor.
        
        @param game_control Referencia a Gamecontrol
        @param xml_file Archivo xml con la configuración del objeto
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param angle Ángulo del objeto, por defecto será 0.
        '''
        gameobject.GameObject.__init__(self, game_control)
        
        #Distintos atributos del objeto
        self.max_speed = None
        self.actual_speed = 0
        self.min_speed = None
        #self.__angle_rotation = None
        self.actual_angle = 0
        self.rotation_angle = None
        self.aceleration = None
        self.desaceleration = None
        self.break_force = None
        
        #Parseamos la información básica
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        self.parser_car_info(parser)
        self.parser_basic_info(parser)
        
        #Definimos la posición del objeto
        self.x = self.old_x = x
        self.y = self.old_y = y
        
        #Si el angulo es 0, no hacemos nada
        if angle == 0:
            self.dx = 0
            self.dy = 0
        #Si es 0 actualizamos el angulo del coche
        else:
            self.actual_angle = angle
            self.dx = cos(angle) * self.actual_speed
            self.dy = sin(angle) * self.actual_speed
        
        #Actualizamos la posicion del coche según su angulo
        self.update_position()
        #Actualizamos la rotación de la imagen del coche
        self.update_image()
        
    def parser_car_info(self, parse):
        '''
        @brief Método que parsea la información básica de los coches.
        '''
        parent_node = parse.firstChild
        self.max_speed = float(parent_node.getAttribute('max_speed'))
        self.min_speed = float(parent_node.getAttribute('min_speed'))
        self.rotation_angle = float(parent_node.getAttribute('rotation_angle'))
        self.aceleration = float(parent_node.getAttribute('aceleration'))
        self.desaceleration = float(parent_node.getAttribute('desaceleration'))
        
    def update(self):
        '''
        @brief Método que debe ser implementado por sus descendientes
        '''
        raise NotImplemented("La funcion update de GameObject debe ser implementada por sus descendientes")
        
    def update_image(self):
        '''
        @bnief Actualiza la imagen, según el estado actual de la animación y el angulo del coche
        '''
        #Rotamos la imagen actual de la animación
        self.image = pygame.transform.rotate(self.original_sprite[self.animations[self.state].get_frame()], -self.actual_angle)
        
        #Actualizamos tanto el alto como el ancho 
        self.rect.w = self.image.get_width()
        self.rect.h = self.image.get_height()
        
        #Obtenemos la nueva mascara de pixeles
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self, delta):
        '''
        @brief Movemos el vehículo en el sentido dado 
        
        @param delta Entero +1 hacia delante, -1 hacia atras
        '''
        #Actualizamos la velocidad actual
        self.actual_speed += self.aceleration * delta
        
        #Controlamos los limites de velocidad del coche
        if self.actual_speed > self.max_speed:
            self.actual_speed = self.max_speed
        elif self.actual_speed < -self.min_speed:
            self.actual_speed = -self.min_speed

    def update_position(self):
        '''
        @brief Actualiza la posición del coche.
        '''
        self.rect.x = int(self.x) - self.rect.w / 2
        self.rect.y = int(self.y) - self.rect.h / 2
        self.x += self.dx
        self.y += self.dy

    def trigonometry(self):
        '''
        @brief Aplica la rotación al coche segun el angulo de este
        '''
        angle = radians(self.actual_angle)
        self.dx = cos(angle) * self.actual_speed
        self.dy = sin(angle) * self.actual_speed
        
    def get_speed(self):
        '''
        @brief Método consultor.
        
        @return La velocidad actual del vehículo.
        '''
        return self.actual_speed
        
    def set_speed(self, new_speed):
        '''
        @brief Método que modifica la velocidad actual.
        
        @param new_speed Nueva velocidad actual para el vehículo.
        '''
        self.actual_speed = new_speed
        
    def get_max_speed(self):
        '''
        @brief Métodod consultor
        
        @return Velocidad máxima del vehículo.
        '''
        return self.max_speed
        
    def set_max_speed(self, new_max_speed):
        '''
        @brief Método que modifica la velocidad maxima del vehiculo
        
        @param new_max_speed Nueva velocidad máxima del vehículo.
        '''
        self.max_speed = abs(new_max_speed)
        
    def get_min_speed(self):
        '''
        @brief Método consultor
        
        @return Velocidad mínima(marcha atrás) del vehículo.
        '''
        return self.min_speed
        
    def set_min_speed(self, new_min_speed):
        '''
        @brief Metodo encargado de modificar la velocidad minima del vehiculo
        
        @param new_min_speed Nueva velocidad mínima del vehículo.
        '''
        self.min_speed = abs(new_min_speed)
        
    def get_angle(self):
        '''
        @brief Métodod Consultor
        
        @return Ángulo actual del vehículo.
        '''
        return self.actual_angle
        
    def set_angle(self, new_angle):
        '''
        @brief Método encargado de modificar el angulo del objeto.
        
        @param new_angle Nuevo ángulo para el vehículo
        '''
        self.actual_angle = new_angle
