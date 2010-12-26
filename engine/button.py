#-*- encoding: utf-8 -*-
import pygame
import resource
import data
import xml.dom.minidom

class Button:
    def __init__(self, xml_file, text, x, y, font_code, center = False):
        
        self.text = text
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        
        if center:           
            self.centerx = x
            self.centery = y
        else:
            self.centerx = (self.rect.w + self.rect.x) / 2
            self.centery = (self.rect.h + self.rect.y) / 2
            
        aux_rect = None
        
        for element in parser.getElementsByTagName('normal'):
            
            normal_image_code = str(element.getAttribute('normal_image'))
            self.normal_image = resource.get_image(normal_image_code)
            aux_rect = self.normal_image.get_rect()
            aux_rect.x = self.centerx
            aux_rect.y = self.centery
            self.rect_normal = pygame.Rect((0,0,0,0))
            self.rect_normal.x = int(element.getAttribute('x')) + aux_rect.x
            self.rect_normal.y = int(element.getAttribute('y')) + aux_rect.y
            self.rect_normal.w = int(element.getAttribute('w'))
            self.rect_normal.h = int(element.getAttribute('h'))
            
        for element in parser.getElementsByTagName('selected'):
            
            selected_image_code = str(element.getAttribute('selected_image'))
            self.selected_image = resource.get_image(selected_image_code)
            aux_rect = self.selected_image.get_rect()
            aux_rect.x = self.centerx
            aux_rect.y = self.centery
            self.rect_selected = pygame.Rect((0,0,0,0))
            self.rect_selected.x = int(element.getAttribute('x')) + aux_rect.x
            self.rect_selected.y = int(element.getAttribute('y')) + aux_rect.y
            self.rect_selected.w = int(element.getAttribute('w'))
            self.rect_selected.h = int(element.getAttribute('h'))
            
        for element in parser.getElementsByTagName('normal_text'):
            
            font_size = int(element.getAttribute('size'))
            r = int(element.getAttribute('r'))
            g = int(element.getAttribute('g'))
            b = int(element.getAttribute('b'))
            color = (r, g, b)
            self.normal_font = resource.get_font(font_code, font_size)
            self.text_render_normal = self.normal_font.render(self.text, True, color)
            self.normal_text_rect = self.text_render_normal.get_rect()
            self.normal_text_rect.x = int(element.getAttribute('x'))
            self.normal_text_rect.y = int(element.getAttribute('y'))
            
        for element in parser.getElementsByTagName('selected_text'):
            
            font_size = int(element.getAttribute('size'))
            r = int(element.getAttribute('r'))
            g = int(element.getAttribute('g'))
            b = int(element.getAttribute('b'))
            color = (r, g, b)
            self.selected_font = resource.get_font(font_code, font_size)
            self.text_render_selected = self.selected_font.render(self.text, True, color)
            self.selected_text_rect = self.text_render_selected.get_rect()
            self.selected_text_rect.x = int(element.getAttribute('x'))
            self.selected_text_rect.y = int(element.getAttribute('y'))
            
        self.selected = False
        self.actual_rect = self.rect_normal
        self.actual_rect_text = self.normal_text_rect
        self.rect_draw = self.normal_image.get_rect()
        self.rect_draw.centery = self.centery
        self.rect_draw.centerx = self.centerx
        
    def draw(self, screen):
        
        aux_surface = None
        destiny_rect = None

        if self.selected:
            aux_surface = self.selected_image
            aux_surface.blit(self.text_render_selected, self.selected_text_rect)

        else:
            aux_surface = self.normal_image
            aux_surface.blit(self.text_render_normal, self.normal_text_rect)

        screen.blit(aux_surface, self.rect_draw)
        
    def update(self):
                
        if self.rect_draw.collidepoint(pygame.mouse.get_pos()):
            self.selected = True
            self.actual_rect = self.rect_selected
            self.rect_draw = self.selected_image.get_rect()

        else:
            self.selected = False
            self.actual_rect = self.rect_normal
            self.rect_draw = self.normal_image.get_rect()

        self.rect_draw.centery = self.centery
        self.rect_draw.centerx = self.centerx
        
    def get_selected():
        return self.selected
    
    def set_selected(boolean):
        self.selected = boolean
        

        

