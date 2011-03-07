#-*- encoding: utf-8 -*-

import basiccar
import gameobject
import keyboard
import data
import math
import pygame
import xml.dom.minidom
import random

from basiccar import *
from gameobject import *
from pygame.locals import *
from math import *

class Hud:
    '''
    @brief Clase que representa la casilla del item actual del jugador
    '''
    def __init__(self, player, path_xml):
        '''
        @brief Constructor.
        
        @param player Referencia al jugador.
        @param path_xml Ruta del archivo xml donde se encuentra toda las características
        '''
        self.player = player
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Obtenemos la imagen de fondo
        image = parse.getElementsByTagName('image')[0]
        image_code = image.getAttribute('image_code')
        self.image = resource.get_image(image_code)
        
        #Posicion de la imagen de fondo
        x = int(image.getAttribute('x'))
        y = int(image.getAttribute('y'))
        self.position_image = (x, y)
        
        #Posición para los items
        items = parse.getElementsByTagName('items')[0]
        x = int(items.getAttribute('x'))
        y = int(items.getAttribute('y'))
        self.item_position = (self.position_image[0] + x, self.position_image[1] + y)
        
        #Mapa para los items
        self.items = {}
        
        #Recorremos cada uno de los items
        for element in parse.getElementsByTagName('item'):
            code = element.getAttribute('code')
            
            self.items[code] = {}
            self.items[code]['image'] = None
            self.items[code]['xml'] = None
            
            #Nos quedamos con su imagen de muestra
            image_code = element.getAttribute('image_code')
            self.items[code]['image'] = resource.get_image(image_code)
            
            #Y con su archivo xml de configuración
            path_xml = element.getAttribute('path_xml')
            self.items[code]['xml'] = path_xml
        
        #En un principio no tenemos ningun item
        self.actual_item = None
                
    def draw(self, screen):
        '''
        @brief Método encargado de dibujar en pantalla el hud
        
        @param screen Superficie destino
        '''
        screen.blit(self.image, self.position_image)
        
        #Si hay algun item actualmente lo mostramos
        if self.actual_item:
            screen.blit(self.items[self.actual_item]['image'], self.item_position)
            
    def released_item(self):
        '''
        @brief Método llamado cuando se a lanzado un item
        '''
        #Si tenemos algun item, lo lanzamos
        if self.actual_item:
            self.actual_item = None
            self.player.released_item()
        
    def collected_item(self):
        '''
        @brief Método llamado cuando recogemos algun item
        '''
        #Si no tenemos actualmente un item
        if not self.actual_item:
            #Obtenemos uno aleatorio de la lista
            self.actual_item = self.items.keys()[random.randint(0, len(self.items.keys()) - 1)]

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
        basiccar.BasicCar.__init__(self, game_control, xml_file, x, y, angle)
        
        self.__assing_controls(player)
        
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
                    YAW: self.__yaw_state,
                    FALL: self.__fall_state
                    }
        
        self.falling = False
        self.min_scale = 0.2
        self.count_scale = 0.01
        self.actual_scale = 1
        
        #HUD del coche
        self.hud = Hud(self, 'hud.xml')
    
    def draw(self, screen):
        BasicCar.draw(self, screen)
        #Mostramos el hud
        self.hud.draw(screen)
                    
    def update(self):
        '''
        Actualiza lógicamente al personaje.
        '''
        if self.state != self.previous_state:
            self.previous_state = self.state
            self.animations[self.state].restart()
            
        self.states[self.state]()
        
        if keyboard.pressed(K_SPACE):
            self.hud.released_item()
        
        if self.state != FALL:
            self.update_position()
            self.update_image()
            self.update_direction()
        
        '''if self.actual_angle < 0:
            self.actual_angle += 360
        if self.actual_angle > 360:
            self.actual_angle -= 360'''
        
        
    def __normal_state(self):
        '''
        Control del estado normal, el coche esta detenido.
        '''
        if keyboard.pressed(self.UP):
            self.old_state = NORMAL
            self.state = RUN
        elif keyboard.pressed(self.DOWN):
            self.old_state = NORMAL
            self.state = REVERSE
            
    def __run_state(self):
        '''
        Control del estado, el coche va hacia el frente.
        '''
        self.move(+1)
        
        if keyboard.release(self.UP):
            self.old_state = RUN
            self.state = NOACTION
        if keyboard.pressed(self.DOWN):
            self.old_state = RUN
            self.state = REVERSE
            
        self.control_rotation()
        
        self.trigonometry()
            
    def __noaction_state(self):
        '''
        Control del estado, no se pulsa ningún boton de dirección.
        '''
        if keyboard.pressed(self.UP):
            self.old_state = NOACTION
            self.state = RUN
        if keyboard.pressed(self.DOWN):
            self.old_state = NOACTION
            self.state = REVERSE
        
        if self.actual_speed > self.desaceleration:
            self.actual_speed -= self.desaceleration
        elif self.actual_speed < -self.desaceleration:
            self.actual_speed += self.desaceleration
        else:
            self.actual_speed = 0
            self.state = NORMAL
                    
        self.control_rotation()
            
        self.trigonometry()
            
    def __reverse_state(self):
        '''
        Control del estado, marcha atrás.
        '''
        self.move(-1)
        
        if keyboard.release(self.DOWN):
            self.old_state = REVERSE
            self.state = NOACTION
        if keyboard.pressed(self.UP):
            self.old_state = REVERSE
            self.state = RUN
        
        self.control_rotation()
        
        self.trigonometry()
    
    def __fall_state(self):
        if not self.falling:
            self.image = self.original_sprite[self.animations[self.state].get_frame()]
            self.falling = True
        
        self.image = pygame.transform.rotozoom(self.image, -5, self.actual_scale)
        self.actual_scale -= self.count_scale
        
        if self.actual_scale < self.min_scale:
            self.actual_speed *= -1
            self.state = NORMAL
            self.old_state = FALL
            self.falling = False
            self.actual_scale = 1
    
    def __forward_state(self):
        pass
    def __damaged_state(self):
        pass
    def __erase_state(self):
        pass
    def __yaw_state(self):
        pass
    
    def control_rotation(self):
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
            self.RIGHT = K_d
            self.LEFT = K_a
    
    def collected_item(self):
        self.hud.collected_item()
    
    def released_item(self):
        pass
    
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
        self.update_direction()

