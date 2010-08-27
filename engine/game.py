# -*- encoding: utf-8 -*-

import pygame
import data
import resource
import xml.dom.minidom
import animation

from pygame.locals import *

'''def blit_animation(screen, image, animation):
    while True:
        screen.blit(image[animation.get_frame()],(50, 50))
        animation.update()
'''

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
        self.__exit = False
        self.__actual_state = None
        
        ## A partir de aqui las variables no pertenecen a la clase game
        ## Si no para realizar las pruebas necesarias de la clase animation
        
        self.granny = resource.get_sprite('granny')
        self.walk = animation.Animation("0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30", 1)
        self.jump = animation.Animation("49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64", 1)
        self.attack =  animation.Animation("64,65,67,68,69,70,71,72,73,74,75,76,77,78,79,80", 1)
        self.actual_animation = self.walk
        
    def __control_exit(self):
        '''
        Función privada que controla la salida del juego
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                self.__exit = True
            # Control de teclado para prueba de modulo animation
            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.walk.restart()
                    self.actual_animation = self.walk
                elif event.key == K_s:
                    self.jump.restart()
                    self.actual_animation = self.jump
                elif event.key == K_d:
                    self.attack.restart()
                    self.actual_animation = self.attack
            
    def run(self):
        '''
        Función que contiene el bucle principal del juego.
        Actualiza y dibuja el estado actual.
        '''
        while not self.__exit:
            self.clock.tick(self.fps)
            self.__control_exit()
            
            self.screen.fill((0,0,0))
            
            self.screen.blit(self.granny[self.actual_animation.get_frame()], (50, 50))
            print self.actual_animation.get_frame()
            self.actual_animation.update()
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
