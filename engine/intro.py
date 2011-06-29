#-*- encoding: utf-8 -*-

import state
import data
import resource
import mainmenu
import keyboard
import pygame
import xml.dom.minidom

class Intro(state.State):
    '''
    @brief Clase encargada de representar la introducción del juego
    consiste en un simple fadein y fadeout del logo.
    '''
    def __init__(self, game, xml_file):
        '''
        @brief Constructor 
        
        @param game Referencia a game
        @param xml_file ruta del archivo xml con la configuración deseada
        '''
        state.State.__init__(self, game)
        
        pygame.display.set_caption("Zycars")

        #Parseamos el fichero xml
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        
        #Obtenemos la velocidad con la que avanzará la introducción
        self.speed = int(parser.firstChild.getAttribute('speed'))
        self.actual_alpha = 0
        
        #Obtenemos una superficie negra del mismo tamaño que la pantalla
        self.surface = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))
        
        #Obtenemos la imagen del logo
        for element in parser.getElementsByTagName('image'):
            
            image_code = str(element.getAttribute('imagecode'))
            x = int(element.getAttribute('x'))
            y = int(element.getAttribute('y'))
            
            image = resource.get_image(image_code)
            
            #La dibujamos sobre la superficie antes mencionada
            self.surface.blit(image, (x,y))
        
        #Indicamos el alfa de la superficie, en un principio será 0, es decir
        #Negra completamente
        self.surface.set_alpha(self.actual_alpha)
        
        #Definimos los estados en los que se encuentra la intro
        self.to_opaque = True
        self.quit = False
        
    def update(self):
        '''
        @brief Método que actualiza la intro
        '''
        #Si vamos de negro a transparente
        if self.to_opaque:
            
            #Si pulsamos alguna de las teclas cancelamos al intro
            if keyboard.pressed(pygame.K_ESCAPE) or keyboard.pressed(pygame.K_SPACE) or keyboard.pressed(pygame.K_RETURN):
                self.quit = True
            
            #Vamos aumentado el alpha segun la velocidad indicada
            self.actual_alpha += self.speed
            self.surface.set_alpha(self.actual_alpha)
            
            #Si la superficie es completamente transparente cambiamos de estado
            if self.actual_alpha >= 255:
                self.to_opaque = False
        
        #Si vamos de transparente a negro
        else:
            
            #si pulsamos alguna de las teclas cancelamos la intro
            if keyboard.pressed(pygame.K_ESCAPE) or keyboard.pressed(pygame.K_SPACE) or keyboard.pressed(pygame.K_RETURN):
                self.quit = True
            
            #Vamos disminuyendo el canal alpha de la superficie
            self.actual_alpha -= self.speed
            self.surface.set_alpha(self.actual_alpha)
            
            #Cuando llegamos de nuevo al negro completo, indicamos que la intro ha terminado
            if self.actual_alpha <= 0:
                self.quit = True
    
        #Si la intro se ha terminado o se ha cancelado
        if self.quit:
            print "Al menú principal"
            #Pasamos al menu principal
            self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))
            
    def draw(self, screen):
        '''
        @brief Método que dibuja la superficie en pantalla
        
        @param screen Superficie destino
        '''
        screen.blit(self.surface, (0,0))
        
