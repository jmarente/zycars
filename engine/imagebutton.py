#-*- encoding: utf-8 -*-

import button
import resource
import data
import pygame
import xml.dom.minidom

class ImageButton(button.Button):
    def __init__(self, xml_file, text, centerx, centery, font_code, image_code, center = True):
        
        button.Button.__init__(self, xml_file, text, centerx, centery, font_code, center)
        
        self.text_render_normal = pygame.transform.rotozoom(self.text_render_normal, 15, 1)
        
        self.image = resource.get_image(image_code)
        self.rect_image = self.image.get_rect()
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        
        for element in parser.getElementsByTagName('image'):
            self.rect_image.x = int(element.getAttribute('x'))
            self.rect_image.y = int(element.getAttribute('y'))
             
    def draw(self, screen):
        
        aux_surface = None
        destiny_rect = None

        if self.selected:
            aux_surface = self.selected_image.copy()

        else:
            aux_surface = self.normal_image.copy()
        
        aux_surface.blit(self.text_render_normal, self.normal_text_rect)
        aux_surface.blit(self.image, self.rect_image)

        screen.blit(aux_surface, self.rect_draw)
    
    def update(self):
        button.Button.update(self)
