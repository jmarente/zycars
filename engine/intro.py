#-*- encoding: utf-8 -*-

import state
import data
import resource
import pygame
import xml.dom.minidom

class Intro(state.State):
    def __init__(self, game, xml_file):
        
        state.State.__init__(self, game)
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        
        self.speed = int(parser.firstChild.getAttribute('speed'))
        self.actual_alpha = 0
        
        self.surface = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))
        
        for element in parser.getElementsByTagName('image'):
            
            image_code = str(element.getAttribute('imagecode'))
            x = int(element.getAttribute('x'))
            y = int(element.getAttribute('y'))
            
            image = resource.get_image(image_code)
            
            self.surface.blit(image, (x,y))
            
        self.surface.set_alpha(self.actual_alpha)
        
        self.to_opaque = True
        self.quit = False
        
    def update(self):
        
        if self.to_opaque:
            
            for event in pygame.event.get():
                self.quit = True
                
            self.actual_alpha += self.speed
            self.surface.set_alpha(self.actual_alpha)
            
            if self.actual_alpha >= 255:
                self.to_opaque = False
                
        else:
            
            for event in pygame.event.get():
                self.quit = True
                
            self.actual_alpha -= self.speed
            self.surface.set_alpha(self.actual_alpha)
            
            if self.actual_alpha <= 0:
                self.quit = True
            
        if self.quit:
            print "Al menú principal"
            
    def draw(self, screen):
        screen.blit(self.surface, (0,0))
        
