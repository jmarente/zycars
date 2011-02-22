# -*- encoding: utf-8 -*-

import pygame
from pygame.color import *
import data
import resource
import keyboard
import mouse
import button
import circuitmenu
import xml.dom.minidom
import os

from pygame.locals import *

class Game:
    '''
    @brief Clase encargada de inicializar pygame. Tiene el bucle principal. También lleva el control de cada estado del juego.
    '''
    def __init__(self):
        '''
        #brief Constructor. Carga e inicializa la configuración principal y las variables principales de la clase
        '''
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        #Cargamos el archivo de configuración
        parser = xml.dom.minidom.parse(data.get_path_xml('configuration.xml'))
        
        #Obtenemos las dimensiones de la pantalla
        for element in parser.getElementsByTagName('screen'):
            self.__screen_width = int(element.getAttribute('width'))
            self.__screen_height = int(element.getAttribute('height'))
            self.caption = element.getAttribute('caption')
        
        #Obtenemos los fps
        for element in parser.getElementsByTagName('fps'):
            self.fps = int(element.getAttribute('value'))
        
        #Inicializamos Pygame
        pygame.init()
        
        #Obtenemos la ventana de juego
        self.screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        
        #Obtenemos el icono
        for element in parser.getElementsByTagName('icon'):
            icon_code = str(element.getAttribute('code'))
            self.icon = resource.get_image(icon_code)
        
        #Deshabilitamos el cursor
        pygame.mouse.set_visible(False)
        pygame.display.set_icon(self.icon)
        
        #Creamos el reloj
        self.clock = pygame.time.Clock()
        
        #Estado actual del juego
        self.__actual_state = circuitmenu.CircuitMenu(self, 'menu/circuitmenu.xml')  
              
    def run(self):
        '''
        @brief Función que contiene el bucle principal del juego. Actualiza y dibuja el estado actual.
        '''
        
        #Mientras no cerremos la pantalla
        while not keyboard.quit():
            
            self.clock.tick(self.fps)
            
            #Actualizamos el teclado
            keyboard.update()
            mouse.update()
            
            #Ponemos la pantalla a negro completamente
            self.screen.fill(THECOLORS['black'])
            
            #Actualizamos y dibujamos el estado actual
            self.__actual_state.update()
            self.__actual_state.draw(self.screen)
            
            #Actualizamos la pantalla
            pygame.display.flip()
        
    def get_screen_width(self):
        '''
        @brief Método que devuelve el ancho de la pantalla en píxeles.
        
        @return Ancho de la pantalla en píxeles.
        '''
        return self.__screen_width
        
    def get_screen_height(self):
        '''
        @brief Método que devuelve el alto de la pantalla en píxeles.
        
        @return Alto de la pantalla en píxeles.
        '''
        return self.__screen_height
        
    def change_state(self, new_state):
        '''
        @brief Método que Recibe y cambia el nuevo estado del juego.
        
        @param new_state, nuevo estado del juego
        '''
        self.__actual_state = new_state
