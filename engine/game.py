# -*- encoding: utf-8 -*-

import pygame
from pygame.color import *
import data
import resource
import keyboard
import button
import timer
import xml.dom.minidom

import sys

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
        
        self.buttons = []
        self.buttons.append(button.Button("menu/genericbutton.xml", "Iniciar", 100, 200, 'cheesebu', True))
        self.buttons.append(button.Button("menu/genericbutton.xml", "Parar", 300, 200, 'cheesebu', True))
        self.buttons.append(button.Button("menu/genericbutton.xml", "Pausar", 500, 200, 'cheesebu', True))
        self.buttons.append(button.Button("menu/genericbutton.xml", "Salir", 700, 200, 'cheesebu', True))
        
        self.timer = timer.Timer('cheesebu', (0,0,0), 250, 300, "Tiempo:")
        self.timer.set_minutes(1)
        self.timer.set_seconds(5)
            
    def run(self):
        '''
        Función que contiene el bucle principal del juego.
        Actualiza y dibuja el estado actual.
        '''
        while not keyboard.quit():
            
            self.clock.tick(self.fps)
            
            keyboard.update()
            
            for button in self.buttons:
                button.update()
                if button.get_selected() and pygame.mouse.get_pressed()[0]:
                    self.treat_option(button.get_option())
            
            self.timer.update()
            
            self.screen.fill(THECOLORS['white'])
            
            for button in self.buttons:
                button.draw(self.screen)
                
            self.timer.draw(self.screen)
            
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
        
    def treat_option(self, text):
        if text == "Salir":
            sys.exit()
        elif text == "Iniciar":
            self.timer.start()
        elif text == "Parar":
            self.timer.stop()
        elif text == "Pausar":
            self.timer.pause()
