#-*- encoding: utf-8 -*-

'''
@file checkpoint.py
Implementa la clase CheckPoint y CheckPoints
@author José Jesús Marente Florín
@date Febrero 2011.
'''

import pygame
from collections import deque
from log import Log

class CheckPoint:
    '''
    @brief Clase que controla la posicion, dibujado y collisión con un punto de control
    '''
    def __init__(self, game_control, x, y, width, height):
        '''
        @brief Constructor.
        
        @param game_control Referencia a GameControl que pertenece el punto de control
        @param x Posición x
        @param y Posición y
        @param width Ancho del punto de control
        @param height Alto del punto de control
        '''
        self.game_control = game_control
        #Obtenemos el rectangulo del punto de control
        self.rect = pygame.Rect((x, y, width, height))
        
    def draw(self, screen, color):
        '''
        @brief Función que dibuja el punto de control en pantalla
        
        @param screen Superficie destino
        @param color Color del punto de control
        '''
        #Dibujamos el punto de control con respecto a la pantalla
        pygame.draw.rect(screen, color, (self.rect.x - self.game_control.circuit_x(), self.rect.y - self.game_control.circuit_y(), self.rect.w, self.rect.h), 1)
        
    def update(self):
        pass
        
    def collision_sprite(self, sprite):
        '''
        @brief Método que comprueba si algun sprite colisiona con el punto de control
        
        @param sprite Sprite a comprobar
        '''
        return self.rect.colliderect(sprite.get_rect())

class CheckPoints:
    '''
    @brief Clase controladora de los CheckPoints, comprueba cuales se han sobrepasado
    y cuales no, también controla las vueltas realizadas al circuito
    '''
    def __init__(self, game_control):
        '''
        @brief Constructor.
        
        @param game_control Referencia a game_control que pertence
        '''
        self.game_control = game_control
        
        #Lista con los puntos de control son pasar
        self.unchecked = deque()
        
        self.actual_checkpoint = None
        
        self.total_checked = 0
        
        #Lista con los puntos de control ya pasados
        self.checked = deque()
        
        #Punto de meta
        self.goal = None
        
        #Todos los Checkpoints
        self.all_checkpoints = {}
        
        #Numero de vueltas
        self.laps = 0
        
        #¿Comenzamos?
        self.start = False
        
        self.wrong_direction = False
        
    def draw(self, screen):
        '''
        @brief Método encargado de mostrar los puntos de control por pantalla-
        
        @param screen Superficie destino
        '''
        #Mostramos todos los puntos de control de color negro
        #for cp in self.unchecked:
            #cp.draw(screen, (0, 0, 0))
        
        #Mostramos el punto de control actual
        if self.actual_checkpoint:
            self.actual_checkpoint.draw(screen, (0, 0, 255))
            
        #Mostramos la meta de color rojo
        self.goal.draw(screen, (255, 0, 0))
            
    def update(self, sprite, player = False):
        '''
        @brief Método encargado de actualizar los distintos CheckPoints
        
        @param sprite Sprite con el que comprobaremos el estado de los CheckPoints
        '''
        
        #Si aun no hemos pasado por la meta ni una sola vez y pasamos,
        #indicamos que se inicia la actualización de los CheckPoinst
        if not self.start and self.goal.collision_sprite(sprite):
            Log().info("Comienza el control de vueltas")
            self.start = True
        
        #Si hemos pasado al menos una vez por la meta una vez tomada la salida
        elif self.start and not self.wrong_direction:
            
            #Si colisionamos con el sprite actual
            if self.actual_checkpoint and self.actual_checkpoint.collision_sprite(sprite):
                
                self.total_checked += 1
                
                #Lo introducimos en la lista de comprobados
                self.checked.append(self.actual_checkpoint)
                
                #Si aun quedan puntos por pasar
                if len(self.unchecked) > 0:
                    
                    #Obtenemos el siguiente y lo ponemos como actual
                    self.actual_checkpoint = self.unchecked.popleft()
                
                #Si no quedan, ponemos el actual a nulo
                else:
                    self.actual_checkpoint = None
            
            #Si hemos pasado todos los puntos, no estamos colisionando con ninguno y pasamos por la meta
            if len(self.unchecked) == 0 and self.goal.collision_sprite(sprite):
                
                #Aumentamos en uno el número de vueltas dadas
                self.laps += 1
                Log().info("Nº de vueltas:" + str(self.laps))
                
                #Informamos a GameControl de que se ha completado una vuelta
                if player:
                    self.game_control.lap_complete()
            
                #Todos los puntos de control pasan a estar sin chequear
                self.unchecked = self.checked
                #La lista de punto chequeados la vaciamos
                self.checked = deque()
                
                #Obtenemos el siguiente punto actual
                self.actual_checkpoint = self.unchecked.popleft()
            
            '''#Controlamos que el coche no de marcha atras en la meta
            if not self.wrong_direction and len(self.unchecked) > 0 and self.goal.collision_sprite(sprite):
                #Indicamos que va en mala dirección
                self.wrong_direction = True'''
                
        '''#Si vamos en mala direccion y pasamos por la meta
        elif self.wrong_direction and self.goal.collision_sprite(sprite):
            #Indicamos que la dirección es correcta
            self.wrong_direction = False'''
        
    def total_chekpoints(self):
        '''
        @brief Método consultor.
        
        @return Número de puntos de control que tiene el circuito
        '''
        return len(self.checked) + len(self.unchecked)

    def add_checkpoint(self, cp, position):
        '''
        @brief Método que añade un nuevo CheckPoint a la lista
        
        @param cp Nuevo Checkpoint a insertar
        '''
        self.all_checkpoints[position] = cp
    
    def order_checkpoints(self):
        '''
        @brief Método encargado de ordenar todos los checkpoints, introduciendolos
        en una cola para su posterior gestión
        '''
        for key in self.all_checkpoints.keys():
            #Introducimos en la cola segun la posición
            self.unchecked.append(self.all_checkpoints[key])
        
        #Obtenemos el primer de los checkpoints a controlar
        self.actual_checkpoint = self.unchecked.popleft()
        
    def set_goal(self, goal):
        '''
        @brief Método que añade la meta del circuito
        
        @param goal Meta 
        '''
        self.goal = goal
    
    def get_laps(self):
        return self.laps
    
    def get_checked(self):
        return len(self.checked)
    
    def get_total_checked(self):
        return self.total_checked
        
