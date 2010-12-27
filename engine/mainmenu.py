#-*- encoding: utf-8 -*-

import state
import data
import resource
import button
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
    
    def draw(self, screen):
        
        screen.blit(self.background, (0, 0))
        
        for image in self.images:
            screen.blit(image[1], image[2])
        
        for button in self.buttons:
            button.draw(screen)
    
    def update(self):
        
        for button in self.buttons:
            button.update()
