#-*- encoding: utf-8 -*-

import button
import imagebutton
import pygame

class CheckBox(imagebutton.ImageButton):
    def __init__(self, xml_file, text, centerx, centery, font_code, image_code, image_x, image_y, show_text = True, center = True):
        imagebutton.ImageButton.__init__(self, xml_file, text, centerx, centery, font_code, image_code, image_x, image_y, show_text, center)
        
        self.checked = False
    
    def draw(self, screen):
        '''
        @brief Método encargado de dibujar el botón en pantalla
        
        @param screen Superficie destino
        '''
        aux_surface = None
        destiny_rect = None

        #Si está seleccionado copiamos la imagen seleccionada
        if self.selected:
            aux_surface = self.selected_image.copy()        
        
        #Si no lo está copiamos la imagen normal
        else:
            aux_surface = self.normal_image.copy()
        
        #Si debemos mostrar el bóton y además es sobre este
        if self.show_text:
            if self.on_button:
                aux_surface.blit(self.text_render_normal, self.normal_text_rect)
        
        screen.blit(aux_surface, self.rect_draw)
        
        if self.checked:
            screen.blit(self.image, self.rect_image)
        
        #Si debemos mostrar el botón y no es sobre este
        if self.show_text:
            if not self.on_button:
                screen.blit(self.text_render_normal, self.normal_text_rect)

    def update(self):
        '''
        @brief Método encargado de actualizar el botón
        '''
        button.Button.update(self)

        if self.selected and pygame.mouse.get_pressed()[0]:
            self.control_checked()
    
    def control_checked(self):
        
        if self.checked:
            self.checked = False
        else:
            self.checked = True
