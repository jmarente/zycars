#-*- encoding: utf-8 -*-

import pygame

class CheckPoint:
    def __init__(self, game_control, x, y, width, height):
        self.game_control = game_control
        self.rect = pygame.Rect((x, y, width, height))
        
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - self.game_control.circuit_x(), self.rect.y - self.game_control.circuit_y(), self.rect.w, self.rect.h), 1)
        
    def update(self):
        pass
        
    def collision_sprite(self, sprite):
        pass

class CheckPoints:
    def __init__(self, game_control):
        pass
    def draw(self):
        pass
    def update(self):
        pass
    def total_chekpoints(self):
        pass
    def add_checkpoint(self):
        pass
