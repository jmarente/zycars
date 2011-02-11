#-*- encoding: utf-8 -*-

import pygame
import xml.dom.minidom

import data
import resource

class Slider:
    def __init__(self, xml_path, actual_value, max_value, x, y):
        
        parse = xml.dom.minidom.parse(data.get_path_xml(xml_path))
        
        bar = parse.getElementsByTagName('bar')
        
        image_code = str(bar[0].getAttribute('image_code'))
        self.bar_image = resource.get_image(image_code)
        self.bar_rect = self.bar_image.get_rect()
        self.bar_rect.x = x
        self.bar_rect.y = y
        
        controler = parse.getElementsByTagName('controler')
        
        image_code = str(controler[0].getAttribute('image_code'))
        self.controler_image = resource.get_image(image_code)
        self.controler_rect = self.controler_image.get_rect()
        self.controler_rect.centerx = self.bar_rect.centerx
        self.controler_rect.centery = self.bar_rect.centery
        
        font = parse.getElementsByTagName('font')
        
        font_code = str(font[0].getAttribute('font_code'))
        self.font = resource.get_font(font_code, 30)
        r = int(font[0].getAttribute('r'))
        g = int(font[0].getAttribute('g'))
        b = int(font[0].getAttribute('b'))
        self.color_font = (r,b,g)
        
        self.max_value = max_value
        self.actual_value = actual_value
        self.update_controler()
        self.still_pressed = False
        
    def update(self):
        
        if (pygame.mouse.get_pressed()[0] and \
            (self.controler_rect.collidepoint(pygame.mouse.get_pos()) \
            or self.bar_rect.collidepoint(pygame.mouse.get_pos()))) \
            or self.still_pressed:
                                                    
            self.controler_rect.centerx = pygame.mouse.get_pos()[0]
            self.still_pressed = True
            self.new_pressed = False
            
            if self.controler_rect.centerx >= (self.bar_rect.x + self.bar_rect.w):
                self.controler_rect.centerx = self.bar_rect.x + self.bar_rect.w
                
            elif self.controler_rect.centerx <= self.bar_rect.x:
                self.controler_rect.centerx = self.bar_rect.x
            
            self.update_value()
        
        if not pygame.mouse.get_pressed()[0]:
            self.still_pressed = False
                
    def draw(self, screen):
        
        value_render = self.font.render(str(self.actual_value), True, self.color_font)
        value_rect = value_render.get_rect()
        value_rect.x = self.bar_rect.x + self.bar_rect.w + 10
        value_rect.centery =self.bar_rect.centery
        
        screen.blit(self.bar_image, self.bar_rect)
        screen.blit(self.controler_image, self.controler_rect)
        screen.blit(value_render, value_rect)
        
    def get_value(self):
        return self.actual_value
        
    def set_value(self, new_value):
        if new_value >= self.min_value and new_value <= self.max_value:
            self.actual_value = new_value
    
    def update_value(self):
        posicion_100 = self.bar_rect.w
        posicion_barra = self.controler_rect.centerx - self.bar_rect.x - self.bar_rect.w
        self.actual_value = (posicion_barra * self.max_value / posicion_100) + self.max_value
    
    def update_controler(self):
        posicion_100 = self.bar_rect.w
        posicion = (self.actual_value * posicion_100) / self.max_value
        self.controler_rect.centerx = posicion + self.bar_rect.x
