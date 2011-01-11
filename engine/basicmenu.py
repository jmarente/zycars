#-*- encoding: utf-8 -*-

import state
import cursor
import data
import resource
import xml.dom.minidom
import pygame

class BasicMenu(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)
        self.buttons = []
        self.background = None
        self.cursor = None
        self.title = None
        self.images = []
        self.actual_option = None
        
    def update(self):
        pass
    def draw(self):
        pass
    def draw_basic_elements(self, screen):
        
        screen.blit(self.background, (0, 0))
        
        screen.blit(self.title, self.title_rect)
        
        for image in self.images:
            screen.blit(image[1], image[2])
        
        for button in self.buttons:
            button.draw(screen)
    
    def parser_basic_info(self, parse):
        
        parent = parse.firstChild
        
        image_code = str(parent.getAttribute('background'))
        self.background = resource.get_image(image_code)
        cursor_xml = str(parent.getAttribute('cursor'))
        self.cursor = cursor.Cursor(data.get_path_xml(cursor_xml))
        
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
            
            if element.hasAttribute('scale'):
                scale = float(element.getAttribute('scale'))
                if scale != 1:
                    temporal = image.copy()
                    image = pygame.transform.rotozoom(temporal, 0, scale)
                
            rect = image.get_rect()
            rect.x = int(element.getAttribute('x'))
            rect.y = int(element.getAttribute('y'))
            self.images.append((image_code, image, rect))
            
    def treat_option(self):
        #raise NotImplemented('Esta función debe ser implementada por todos los descendientes de BasicMenu')
        pass
