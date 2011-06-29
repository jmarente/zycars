#-*- encoding: utf-8 -*-

import data
import keyboard
import pygame
import basicmenu
import optionmenu
import charactermenu
import xml.dom.minidom
import config

class MainMenu(basicmenu.BasicMenu):
    '''
    @brief Clase que modela el comportamiento del menú principal del juego
    '''
    def __init__(self, game, path_xml):
        '''
        @brief Constructor
        
        @param game Referencia a game
        @param path_xml Ruta del archivo xml con las características del menú
        '''
        basicmenu.BasicMenu.__init__(self, game)
        
        #Cambiamos el titulo de la ventana
        pygame.display.set_caption("Zycars: Menú Principal")
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Le pasamos el archivo parseado a BasicMenu para que obtenga los elementos básicos
        self.parser_basic_info(parse)

    def draw(self, screen):
        '''
        @brief Método que dibuja todos los elementos en pantalla
        
        @param screen Superficie destino
        '''
        #Dibujamos todos los elementos basicos
        self.draw_basic_elements(screen)
        
        #Dibujamos el cursor
        self.cursor.draw(screen)
            
    def treat_option(self, option):
        '''
        @brief Método que controla la opción elegida y que hacer según el caso.
        '''
        if option == u"Carrera Rápida":
            print "Elegido: Carrera Rapida"
            config.Config().set_mode(config.FASTRACE)
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
            
        elif option == "Campeonato":
            print "Elegido: Campeonato"
            config.Config().set_mode(config.CHAMPIONSHIP)
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
            
        elif option == "Contrarreloj":
            print "Ha elegido: Contrarreloj"
            config.Config().set_mode(config.TIMED)
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
            
        elif option == "Opciones":
            print "Ha elegido: Opciones"
            self.game.change_state(optionmenu.OptionMenu(self.game, 'menu/optionmenu.xml'))
            
        elif option == "Salir":
            print "Ha elegido: Salir"
            keyboard.set_quit(True)
