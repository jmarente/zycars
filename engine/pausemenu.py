#-*- encoding: utf-8 -*-

import basicmenu
import data
import keyboard
import mainmenu
import pygame
import xml.dom.minidom

class PauseMenu(basicmenu.BasicMenu):
    '''
    @brief Clase que modela el comportamiento del menú de pausa del juego
    '''
    def __init__(self, game, game_control, path_xml):
        '''
        @brief Constructor
        
        @param game referencia a Game
        @param game_control referencia al GameControl que pertenece
        @param path_xml Archivo xml con la configuración
        '''
        basicmenu.BasicMenu.__init__(self, game)
        
        self.game_control = game_control
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Parseamos la configuración basica
        self.parser_basic_info(parse)
        
        #Obtenemos la superficie transparente que será el fondo del menú
        self.layer = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))
        self.layer.set_alpha(125)
        
        #Obtenemos el centro de la pantalla
        center_screen = (pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2)
        
        #Asigamos la posición de dibujado de la pantalla que será el centro
        self.rect_background = self.background.get_rect()
        self.rect_background.centerx = center_screen[0]
        self.rect_background.centery = center_screen[1]
        
    def draw(self, screen):
        '''
        @brief Método que dibuja los elementos en pantalla
        
        @param screen Superficie destino
        '''
        screen.blit(self.layer, (0, 0))
        screen.blit(self.background, self.rect_background)
        
        for button in self.buttons:
            button.draw(screen)
        
        screen.blit(self.title, self.title_rect)
        
        self.cursor.draw(screen)
        
    def update(self):
        '''
        @brief Método que actualiza el menú
        '''
        #Comprobamos el estado de los botones
        self.actual_option = None
        for button in self.buttons:
            button.update()
            if button.get_selected():
                self.actual_option = button.get_option()
        
        #Si alguno está seleccionado cambiamos el cursor
        if self.actual_option:
            self.cursor.over()
                
        #Si no, lo dejamos normal
        else:
            self.cursor.normal()
        
        #Actualizamos el cursor
        self.cursor.update()
            
    def treat_option(self, option):
        '''
        @brief Método encargado de manejar las opciones del menú
        '''
        if option == "Reanudar":
            print "Elegido: Reanudar"
            self.game_control.set_state('race')
        elif option == u"Menú":
            print "Elegido: Menú"
            self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))
        elif option == "Reiniciar":
            print "Ha elegido: Reinicar"
            self.game_control.reboot_race()
