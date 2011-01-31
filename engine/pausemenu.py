#-*- encoding: utf-8 -*-

import basicmenu
import data
import keyboard
import pygame
import xml.dom.minidom

class PauseMenu(basicmenu.BasicMenu):
    def __init__(self, game, path_xml):
        basicmenu.BasicMenu.__init__(self, None)
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        self.parser_basic_info(parse)
        
        self.layer = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))
        self.layer.set_alpha(125)
        
        center_screen = (pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2)
        
        self.rect_background = self.background.get_rect()
        self.rect_background.centerx = center_screen[0]
        self.rect_background.centery = center_screen[1]
        
    def draw(self, screen):
        screen.blit(self.layer, (0, 0))
        screen.blit(self.background, self.rect_background)
        
        for button in self.buttons:
            button.draw(screen)
        
        screen.blit(self.title, self.title_rect)
        
        self.cursor.draw(screen)
    def update(self):
        
        self.cursor.update()
        
        self.actual_option = None
        for button in self.buttons:
            button.update()
            if button.get_selected():
                self.actual_option = button.get_option()
        
        if self.actual_option:
            self.cursor.over()
        else:
            self.cursor.normal()
        
        self.cursor.update()

        if pygame.mouse.get_pressed()[0]:
            self.treat_option()
            
    def treat_option(self):
        if self.actual_option == "Reanudar":
            print "Elegido: Reanudar"
        elif self.actual_option == "Menu":
            print "Elegido: Menú"
        elif self.actual_option == "Salir":
            print "Ha elegido: Salir"
            keyboard.set_quit(True)
