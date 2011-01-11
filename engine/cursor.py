#-*- encoding: utf-8 -*-

import pygame
import data
import resource
import xml.dom.minidom

class Cursor(pygame.sprite.Sprite):
    def __init__(self, xml_path):
        parser = xml.dom.minidom.parse(data.get_path_xml('cursor.xml'))
        
        root = parser.firstChild
        self.normal_image = resource.get_image(root.getAttribute('normal_image'))
        self.over_image = resource.get_image(root.getAttribute('over_image'))
        self.actual_image = self.normal_image
        
        self.x = self.y = 0
        self.update()
        
    def draw(self, screen):
        screen.blit(self.actual_image, (self.x, self.y))
        
    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        
    def over(self):
        self.actual_image = self.over_image
        
    def normal(self):
        self.actual_image = self.normal_image
