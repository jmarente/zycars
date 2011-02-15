# -*- encoding: utf-8 -*-

import pygame
import data
import resource
import keyboard
import particle
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
        self.__actual_state = particle.SystemParticle(400, 300, ['particle', 'particle2'], 100, 1, 10, 300, 1)
            
    def run(self):
        '''
        Función que contiene el bucle principal del juego.
        Actualiza y dibuja el estado actual.
        '''
        while not keyboard.quit():
            
            self.clock.tick(self.fps)
            
            keyboard.update()
            
            if keyboard.pressed(K_UP) or self.__actual_state.get_status() == 'done':
                print "pulsandooo"
                #self.__actual_state = particle.SystemParticle(400, 300, ['particle', 'particle2'], 100, 1, 10, 300, 1)
                self.__actual_state.restart()
                    
            self.screen.fill((255,255,255))
            
            self.__actual_state.update()
            self.__actual_state.draw(self.screen)
            
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
