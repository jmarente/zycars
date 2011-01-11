#-*- encoding: utf-8 -*-

import button
import resource
import data
import pygame
import xml.dom.minidom

class ImageButton(button.Button):
    def __init__(self, xml_file, text, centerx, centery, font_code, image_code, image_x, image_y, center = True):
        
        button.Button.__init__(self, xml_file, text, centerx, centery, font_code, center)
        
        #self.text_render_normal = pygame.transform.rotozoom(self.text_render_normal, 12, 1)
        
        if not self.on_button:
            self.normal_text_rect.x += self.rect_draw.x
            self.normal_text_rect.y += self.rect_draw.y
        
        self.image = resource.get_image(image_code)
        self.rect_image = self.image.get_rect()

        self.rect_image.x = image_x + self.rect_draw.x
        self.rect_image.y = image_y + self.rect_draw.y
             
    def draw(self, screen):
        
        aux_surface = None
        destiny_rect = None

        if self.selected:
            aux_surface = self.selected_image.copy()

        else:
            aux_surface = self.normal_image.copy()
        
        if self.on_button:
            aux_surface.blit(self.text_render_normal, self.normal_text_rect)
        
        screen.blit(aux_surface, self.rect_draw)
        screen.blit(self.image, self.rect_image)
        if not self.on_button:
            screen.blit(self.text_render_normal, self.normal_text_rect)
    
    def update(self):
        button.Button.update(self)
