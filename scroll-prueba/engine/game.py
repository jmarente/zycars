# -*- encoding: utf-8 -*-

import pygame
import data
import resource
import keyboard
import xml.dom.minidom

import circuit

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
        
        ###########PRUEBA DE CIRCUIT###########
        
        self.circuit = circuit.Circuit(None, 'circuito.tmx')
        #self.circuit.move(0, self.circuit.get_height() * self.circuit.get_tile_height() - pygame.display.get_surface().get_height())
            
    def run(self):
        '''
        Función que contiene el bucle principal del juego.
        Actualiza y dibuja el estado actual.
        '''
        while not keyboard.quit():
            
            self.clock.tick(self.fps)
            
            keyboard.update()
            
            self.screen.fill((0,0,0))
            
            #self.__actual_state.update()
            #self.__actual_state.draw(screen)
            
            if keyboard.pressed(K_DOWN):
                if self.circuit.get_y() < self.circuit.get_tile_height() * self.circuit.get_height() - self.screen.get_height():
                    self.circuit.move(self.circuit.get_x(), self.circuit.get_y() + 25)
            elif keyboard.pressed(K_UP):
                if self.circuit.get_y() > 0:
                    self.circuit.move(self.circuit.get_x(), self.circuit.get_y() - 25)
            if keyboard.pressed(K_LEFT):
                if self.circuit.get_x() > 0:
                    self.circuit.move(self.circuit.get_x() - 25, self.circuit.get_y())
            elif keyboard.pressed(K_RIGHT):
                if self.circuit.get_x() < self.circuit.get_tile_width() * self.circuit.get_width() - self.screen.get_width():
                    self.circuit.move(self.circuit.get_x() + 25, self.circuit.get_y())
            
            self.circuit.draw(self.screen, 0)
            self.circuit.draw(self.screen, 1)
            self.circuit.draw(self.screen, 2)
            
            
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
