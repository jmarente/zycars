#-*- encoding: utf-8 -*-
import pygame
import resource
import data
import xml.dom.minidom

class Button:
    def __init__(self, xml_file, text, centerx, centery, font_code, center = True):
        
        self.text = text
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        
        self.centerx = centerx
        self.centery = centery 
            
        aux_rect = None
        
        father = parser.firstChild
        
        self.text_position = str(father.getAttribute('text_position'))
        
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
            posx = int(element.getAttribute('x'))
            posy = int(element.getAttribute('y'))
            self.normal_text_rect = self.__set_rect_text(self.normal_text_rect, posx, posy)
            
        for element in parser.getElementsByTagName('selected_text'):
            
            font_size = int(element.getAttribute('size'))
            r = int(element.getAttribute('r'))
            g = int(element.getAttribute('g'))
            b = int(element.getAttribute('b'))
            color = (r, g, b)
            self.selected_font = resource.get_font(font_code, font_size)
            self.text_render_selected = self.selected_font.render(self.text, True, color)
            self.selected_text_rect = self.text_render_selected.get_rect()
            posx = int(element.getAttribute('x'))
            posy = int(element.getAttribute('y'))
            self.selected_text_rect = self.__set_rect_text(self.selected_text_rect, posx, posy)

            
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
            aux_surface = self.selected_image.copy()
            aux_surface.blit(self.text_render_selected, self.selected_text_rect)

        else:
            aux_surface = self.normal_image.copy()
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
        
    def __set_rect_text(self, rect, posx, posy):
        if self.text_position == 'left':
            rect.x = posx
            rect.y = posy
        elif self.text_position == 'right':
            rect.x = posx - rect.w
            rect.y = posy
        return rect

        

