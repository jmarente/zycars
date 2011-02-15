#-*- encoding: utf-8 -*-

'''
@file countdown.py
Implementa la clase CountDown
@author José Jesús Marente Florín
@date Febrero 2011.
'''

import pygame
import resource
import time
from collections import deque

class CountDown:
    '''
    @brief Clase que simula una cuenta atrás
    '''
    def __init__(self, font_code, size_font, inicial_scale, increase_scale, number = 3):
        '''
        @brief Constructor
        
        @param font_code Código de la fuente a usar
        @param size_font Tamaño de la fuente a usar
        @param inicial_scale Escala inicial
        @param increase_scale Parametro de incremento de la escalaa
        @param number Número en segundos de la cuenta atrás
        '''
        #Obtenemos la fuente
        self.font = resource.get_font(font_code, size_font)
        
        #Creamos la cola de elementos
        self.elements = deque()
        
        #Introducimos todos los elementos
        for i in range(1,number + 1):
            self.elements.appendleft(self.font.render(str(i), True, (0, 0, 0)))
        
        #Introducimos el fin de la cuenta atras
        self.elements.append(self.font.render('Go!!!', True, (0, 0, 0)))
        
        #Obtenemos el primer elemento de la cola
        self.actual_element = self.elements.popleft()
        self.element_modify = self.actual_element
        
        #Asinamos valores
        self.inicial_scale = inicial_scale
        self.increase_scale = increase_scale
        self.scale = inicial_scale
        
        #Obtenemos el centro de la pantalla para que todos los número queden 
        #igual posicionados
        self.centerx = pygame.display.get_surface().get_width() / 2
        self.centery = pygame.display.get_surface().get_height() / 2
        
        #Variables que representan posicion de destino, tiempo inicial y 
        #condicion de parada, respectivamente
        self.rect_destiny = None
        self.__start = None
        self.stop = False
        
    def update(self):
        '''
        @brief Método que actualiza logicamente la cuenta atrás
        '''
        
        #Si aún no se ha iniciado
        if not self.__start:
            #La iniciamos
            self.__start = time.time()
        
        #Si ya ha pasado un segundo o más y aún quedan elementos
        elif (time.time() - self.__start) >= 1 and len(self.elements) > 0:
            
            #Obtenemos el nuevo elemento a dibujar
            self.actual_element = self.elements.popleft()
            self.element_modify = self.actual_element
            
            #Reiniciamos la escala
            self.scale = self.inicial_scale
            
            #reiniciamos el contador
            self.__start = None
        
        #Si ya ha pasado un segundo o más y no quedan elementos
        elif (time.time() - self.__start) >= 1 and len(self.elements) == 0:
            #Detenemos la ejecución
            self.stop = True
        
        #Si la ejecución continua
        if not self.stop:
            
            #Escalamos la imagen actual
            self.element_modify = pygame.transform.rotozoom(self.actual_element, 0, self.scale)
            
            #Incrementamos la escala para la siguiente iteración
            self.scale += self.increase_scale
            
            #Asignamos la posición
            self.rect_destiny = self.element_modify.get_rect()
            self.rect_destiny.centerx = self.centerx 
            self.rect_destiny.centery = self.centery 
        
    def draw(self, screen):
        '''
        @brief Método encargado de dibujar en pantalla
        
        @param screen Superficie destino
        '''
        screen.blit(self.element_modify, self.rect_destiny)
    
    def complete(self):
        '''
        @brief Métodod que indica si la cuenta atrás se ha completado
        
        @return True si se ha completado, False en otro caso
        '''
        return self.stop
