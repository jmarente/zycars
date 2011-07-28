#-*- encoding: utf-8 -*-

'''
@file cursor.py
Implementa la clase Cursor
@author José Jesús Marente Florín
@date Diciembre 2010.
'''

import pygame
import data
import resource
import xml.dom.minidom

class Cursor(pygame.sprite.Sprite):
    '''
    @brief Clase encargada de representar un cursor en pantalla
    '''
    def __init__(self):
        '''
        @brief Constructor de cursor
        
        @param xml_path Ruta del archivo de configuración del cursor
        '''
        parser = xml.dom.minidom.parse(data.get_path_xml('cursor.xml'))
        
        root = parser.firstChild
        
        #Obtenemos la imagen para cada caso
        self.normal_image = resource.get_image(root.getAttribute('normal_image'))
        self.over_image = resource.get_image(root.getAttribute('over_image'))
        
        #La actual
        self.actual_image = self.normal_image
        
        #Inicializamos la posición del cursor
        self.x = self.y = 0
        
        #Actualizamos la posición del cursor
        self.update()
        
    def draw(self, screen):
        '''
        @brief Método que dibuja el curso en pantalla
        
        @param screen Superficie destino
        '''
        screen.blit(self.actual_image, (self.x, self.y))
        
    def update(self):
        '''
        @brief Método encargado de actualizar la posición del cursor
        '''
        self.x, self.y = pygame.mouse.get_pos()
        
    def over(self):
        '''
        @brief Método para indicar que el cursor se encuentra sobre algo colisionable
        '''
        self.actual_image = self.over_image
        
    def normal(self):
        '''
        @brief Método para indicar que el cursor NO se encuentra sobre algo colisionable
        '''
        self.actual_image = self.normal_image
