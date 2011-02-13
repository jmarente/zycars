#-*- encoding: utf-8 -*-

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
        self.unchecked = []
        
        #Lista con los puntos de control ya pasados
        self.checked = []
        
        #Punto de meta
        self.goal = None
        
        #Numero de vueltas
        self.laps = 0
        
        #¿Comenzamos?
        self.start = False
        
    def draw(self, screen):
        '''
        @brief Método encargado de mostrar los puntos de control por pantalla-
        
        @param screen Superficie destino
        '''
        #Mostramos todos los puntos de control de color negro
        for cp in self.unchecked:
            cp.draw(screen, (0, 0, 0))
        
        #Mostramos la meta de color rojo
        self.goal.draw(screen, (255, 0, 0))
            
    def update(self, sprite):
        '''
        @brief Método encargado de actualizar los distintos CheckPoints
        
        @param sprite Sprite con el que comporbaremos el estado de los CheckPoints
        '''
        
        #Si aun no hemos pasado por la meta ni una sola vez y pasamos,
        #indicamos que se inicia la actualización de los CheckPoinst
        if not self.start and self.goal.collision_sprite(sprite):
            Log().info("Comienza el control de vueltas")
            self.start = True
        
        #Si hemos pasado al menos una vez por la meta una vez tomada la salida
        elif self.start:
            
            #Lista auxiliar
            aux_list = []
            
            #Comprobamos cada uno de los puntos
            for cp in self.unchecked:
                #Si el coche collisiona con él
                if cp.collision_sprite(sprite):
                    #Lo añadimos a la lista de comprobados
                    self.checked.append(cp)
                    Log().debug("Punto de control")
                #Si no, a la lista auxiliar
                else:
                    aux_list.append(cp)
            
            #Asignamos la lista auxiliar a la lista de puntos no pasados
            self.unchecked = aux_list
            
            #Si hemos pasado todos los puntos, no estamos colisionando con ninguno y pasamos por la meta
            if len(self.unchecked) == 0 and self.__none_collision(sprite) and self.goal.collision_sprite(sprite):
                #Aumentamos en uno el número de vueltas dadas
                self.laps += 1
                Log().info("Nº de vueltas:" + str(self.laps))
                
                #Todos los puntos de control pasan a estar sin chequear
                self.unchecked = self.checked
                self.checked = []
        
    def total_chekpoints(self):
        '''
        @brief Método consultor.
        
        @return Número de puntos de control que tiene el circuito
        '''
        return len(self.checked) + len(self.unchecked)

    def add_checkpoint(self, cp):
        '''
        @brief Método que añade un nuevo CheckPoint a la lista
        
        @param cp Nuevo Checkpoint a insertar
        '''
        self.unchecked.append(cp)
        
    def set_goal(self, goal):
        '''
        @brief Método que añade la meta del circuito
        
        @param goal Meta 
        '''
        self.goal = goal
    
    def __none_collision(self, sprite):
        
        for cp in self.checked:
            if cp.collision_sprite(sprite):
                return False
        
        return True
