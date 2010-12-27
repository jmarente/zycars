# -*- encoding: utf-8 -*-

import pygame
from pygame.color import *
import data
import resource
import keyboard
import button
import xml.dom.minidom

from pygame.locals import *

class Game:
    '''
    Clase encargada de inicializar pygame. Tiene el bucle principal .
    También lleva el control de cada estado del juego.
    '''
    def __init__(self):
        '''
        Carga e inicializa la configuración principal y las variables principales de la clase
        '''
        parser = xml.dom.minidom.parse(data.get_path_xml('configuration.xml'))
        
        for element in parser.getElementsByTagName('screen'):
            self.__screen_width = int(element.getAttribute('width'))
            self.__screen_height = int(element.getAttribute('height'))
            self.caption = element.getAttribute('caption')
        
        for element in parser.getElementsByTagName('fps'):
            self.fps = int(element.getAttribute('value'))
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        
        for element in parser.getElementsByTagName('icon'):
            icon_code = str(element.getAttribute('code'))
            self.icon = resource.get_image(icon_code)
        
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.__actual_state = None
        
        self.button = button.Button("menu/mainoption1.xml", "Prueba", 400, 300, 'cheesebu', True)
        self.button2 = button.Button("menu/mainoption2.xml", "Prueba2lslsls", 400, 365, 'cheesebu', True)
        self.button3 = button.Button("menu/mainoption1.xml", "Prueba3", 400, 405, 'cheesebu', True)
            
    def run(self):
        '''
        Función que contiene el bucle principal del juego.
        Actualiza y dibuja el estado actual.
        '''
        while not keyboard.quit():
            
            self.clock.tick(self.fps)
            
            keyboard.update()
            
            self.button.update()
            self.button2.update()
            self.button3.update()
            
            self.screen.fill(THECOLORS['white'])
            
            self.button.draw(self.screen)
            self.button2.draw(self.screen)
            self.button3.draw(self.screen)
            
            #self.__actual_state.update()
            #self.__actual_state.draw(screen)
            
            pygame.display.flip()
        
    def get_screen_width(self):
        '''
        Devuelve el ancho de la pantalla en píxeles
        '''
        return self.__screen_width
        
    def get_screen_height(self):
        '''
        Devuelve el alto de la pantalla en píxeles
        '''
        return self.__screen_height
        
    def change_state(self, new_state):
        '''
        Recibe y cambia el nuevo estado del juego.
        '''
        self.__actual_state = new_state
