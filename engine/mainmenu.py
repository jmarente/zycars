#-*- encoding: utf-8 -*-

import state
import data
import resource
import button
import keyboard
import pygame
import xml.dom.minidom

class MainMenu(state.State):
    def __init__(self, game, path_xml):
        state.State.__init__(self, game)
        
        pygame.display.set_caption("Zycars: Menú Principal")
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        parent = parse.firstChild
        
        image_code = str(parent.getAttribute('background'))
        self.background = resource.get_image(image_code)
        
        for element in parse.getElementsByTagName('title'):
            font_code = str(element.getAttribute('font'))
            font_size = int(element.getAttribute('size'))
            font = resource.get_font(font_code, font_size)
            text = str(element.getAttribute('text'))
            r = int(element.getAttribute('r'))
            g = int(element.getAttribute('g'))
            b = int(element.getAttribute('b'))
            color = (r, g, b)
            self.title = font.render(text, True, color)
            self.title_rect = self.title.get_rect()
            self.title_rect.x = int(element.getAttribute('x'))
            self.title_rect.y = int(element.getAttribute('y'))
        
        self.images = []
        for element in parse.getElementsByTagName('image'):
            image_code = str(element.getAttribute('image_code'))
            image = resource.get_image(image_code)
            rect = image.get_rect()
            rect.x = int(element.getAttribute('x'))
            rect.y = int(element.getAttribute('y'))
            self.images.append((image_code, image, rect))
        
        self.buttons = []
        for element in parse.getElementsByTagName('option'):
            xml_file = str(element.getAttribute('xml_file'))
            font_code = str(element.getAttribute('font'))
            text = str(element.getAttribute('text'))
            x = int(element.getAttribute('x'))
            y = int(element.getAttribute('y'))
            aux_button = button.Button(xml_file, text, x, y, font_code, True)
            self.buttons.append(aux_button)
        
        self.actual_option = None
    
    def draw(self, screen):
        
        screen.blit(self.background, (0, 0))
        
        screen.blit(self.title, self.title_rect)
        
        for image in self.images:
            screen.blit(image[1], image[2])
        
        for button in self.buttons:
            button.draw(screen)
    
    def update(self):
        
        self.actual_option = None
        for button in self.buttons:
            button.update()
            if button.get_selected():
                self.actual_option = button.get_option()
        
        if pygame.mouse.get_pressed()[0]:
            self.__treat_option()
            
    def __treat_option(self):
        if self.actual_option == "Carrera Rapida":
            print "Elegido: Carrera Rapida"
        elif self.actual_option == "Campeonato":
            print "Elegido: Campeonato"
        elif self.actual_option == "Contrarreloj":
            print "Ha elegido: Contrarreloj"
        elif self.actual_option == "Opciones":
            print "Ha elegido: Opciones"
        else:
            print "Ha elegido: Salir"
            keyboard.set_quit(True)
