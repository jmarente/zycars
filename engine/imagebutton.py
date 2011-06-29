#-*- encoding: utf-8 -*-

import button
import resource

class ImageButton(button.Button):
    '''
    @brief Clase que modela el comportamiento de un boton que tiene una imagen
    Hereda todas las funcionalidades de Button
    '''
    def __init__(self, menu, xml_file, text, centerx, centery, font_code, image_code, image_x, image_y, show_text = True, center = True):
        '''
        @brief Constructor
        
        @param xml_file Ruta del archivo xml con la configuración básica
        @param text Texto con la opción del botón
        @param centerx Posicion del centro de la x del botón
        @param centery Posicion del centro de la y del botón
        @param font_code Código de la fuente a usar
        @param image_code Código de la imagen a usar
        @param image_x Posición x de la imagen respecto al botón
        @param image_y Posición y de la imagen respecto al botón
        @param show_text Indica si se debe mostrar el texto o no
        '''
        button.Button.__init__(self, menu, xml_file, text, centerx, centery, font_code, show_text)
        
        #self.text_render_normal = pygame.transform.rotozoom(self.text_render_normal, 12, 1)
        
        #Si se muestra el texto y no es sobre el botón, asignamos la posición
        if self.show_text:
            if not self.on_button:
                self.normal_text_rect.x += self.rect_draw.x
                self.normal_text_rect.y += self.rect_draw.y
        
        #Obtenemos la imagen del botón
        self.image = resource.get_image(image_code)
        
        #Obtenemos posición de la imagen
        self.rect_image = self.image.get_rect()
        self.rect_image.x = image_x + self.rect_draw.x
        self.rect_image.y = image_y + self.rect_draw.y
             
    def draw(self, screen):
        '''
        @brief Método encargado de dibujar el botón en pantalla
        
        @param screen Superficie destino
        '''
        aux_surface = None

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
        screen.blit(self.image, self.rect_image)
        
        #Si debemos mostrar el bóton y no es sobre este
        if self.show_text:
            if not self.on_button:
                screen.blit(self.text_render_normal, self.normal_text_rect)
    
    def update(self):
        '''
        @brief Método encargado de actualizar el estado del botón
        '''
        button.Button.update(self)
