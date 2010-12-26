import pygame
import resource

class Button:
    def __init__(self, text, x, y, normal_image_code, selected_image_code, font_code, center = False):
        
        self.normal_image = resource.get_image(normal_image_code)
        self.selected_image = resource.get_image(selected_image_code)
        self.rect = self.normal_image.get_rect()
        if center:
            self.rect.centerx = x
            self.rect.centery = y            
            self.centerx = x
            self.centery = y
        else:
            self.rect.x = x
            self.rect.y = y
            self.centerx = self.rect.w - seef.rect.x
            self.centery = self.rect.h - seef.rect.y
        
        self.mask = pygame.mask.from_surface(self.normal_image)
        self.list_rect = self.mask.get_bounding_rects()
        self.font = resource.get_font(font_code, 40)
        self.font2 = resource.get_font(font_code, 45)
        self.text = text
        self.selected = False
        self.change = True
        self.text_render_normal = self.font.render("Prueba", True, (248, 179, 51))
        self.text_render_selected = self.font2.render("Prueba", True, (188, 8, 37))
        
    def draw(self, screen):
        
        aux_surface = None
        destiny_rect = None

        if self.selected:
            aux_surface = self.selected_image
            aux_surface.blit(self.text_render_selected, (220, 7))

        else:
            aux_surface = self.normal_image
            aux_surface.blit(self.text_render_normal, (200, 5))

        screen.blit(aux_surface, self.rect)
        
    def update(self):
        over = False
                
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.selected:
                self.change = True
            self.selected = True
            self.rect.w = self.selected_image.get_width()
            self.rect.h = self.selected_image.get_height()
        else:
            if self.selected:
                self.change = True
            self.selected = False            
            self.rect.w = self.normal_image.get_width()
            self.rect.h = self.normal_image.get_height()
        
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        
    def get_selected():
        return self.selected
    
    def set_selected(boolean):
        self.selected = True
        

        

