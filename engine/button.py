#-*- encoding: utf-8 -*-
import pygame
import resource
import data
import xml.dom.minidom

def strTobool(string):
    return string.lower() in ['yes', 'true', 't', '1']

class Button:
    '''
    @brief Clase que modela el comportamiento de un botón
    '''
    def __init__(self, xml_file, text, centerx, centery, font_code, show_text = True, center = True):
        '''
        @brief Constructor.
        
        @param xml_file ruta del archivo xml donde se encuentra la configuración básica del botón
        @param text Texto que aparecera sobre el botón
        @param centerx Posición del centro x del boton 
        @param centery Posición del centro y del boton 
        '''
        self.text = text
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        
        self.centerx = centerx
        self.centery = centery 
            
        aux_rect = None
        
        father = parser.firstChild
        
        #Obtenemos la posición del texto en el boton
        self.text_position = str(father.getAttribute('text_position'))
        
        #Comprobamos si el boton mostrará el texto o no.
        if father.hasAttribute('on_button'):
            self.on_button = strTobool(str(father.getAttribute('on_button')))
        else:
            self.on_button = True
        
        #Obtenemos la imagen y sus características cuando el boton esta en estado normal
        for element in parser.getElementsByTagName('normal'):
            
            #Cargamos la imagen
            normal_image_code = str(element.getAttribute('normal_image'))
            self.normal_image = resource.get_image(normal_image_code)
            
            #obtenemos posicion de la imagen
            aux_rect = self.normal_image.get_rect()
            aux_rect.x = self.centerx
            aux_rect.y = self.centery
            self.rect_normal = pygame.Rect((0,0,0,0))
            self.rect_normal.x = int(element.getAttribute('x')) + aux_rect.x
            self.rect_normal.y = int(element.getAttribute('y')) + aux_rect.y
            self.rect_normal.w = int(element.getAttribute('w'))
            self.rect_normal.h = int(element.getAttribute('h'))
        
        #Obtenemos la imagen y caracteristicas cuando el botón está seleccionado    
        for element in parser.getElementsByTagName('selected'):
            
            #Cargamos imagen
            selected_image_code = str(element.getAttribute('selected_image'))
            self.selected_image = resource.get_image(selected_image_code)
            
            #Obtenemos la posicion
            aux_rect = self.selected_image.get_rect()
            aux_rect.x = self.centerx
            aux_rect.y = self.centery
            self.rect_selected = pygame.Rect((0,0,0,0))
            self.rect_selected.x = int(element.getAttribute('x')) + aux_rect.x
            self.rect_selected.y = int(element.getAttribute('y')) + aux_rect.y
            self.rect_selected.w = int(element.getAttribute('w'))
            self.rect_selected.h = int(element.getAttribute('h'))
        
        #Obtenemos el la posicion centrar de las dos imagenes
        self.rect_draw = self.normal_image.get_rect()
        self.rect_draw.centery = self.centery
        self.rect_draw.centerx = self.centerx
        
        #Si indicamos que se muestre el texto
        if show_text:
            
            #Obtenemos el texto normal que se mostrará
            for element in parser.getElementsByTagName('normal_text'):
                
                #Tamaño
                font_size = int(element.getAttribute('size'))
                
                #Color
                r = int(element.getAttribute('r'))
                g = int(element.getAttribute('g'))
                b = int(element.getAttribute('b'))
                color = (r, g, b)
                
                #Renderizamos
                self.normal_font = resource.get_font(font_code, font_size)
                self.text_render_normal = self.normal_font.render(self.text, True, color)
                
                #Vemos si el texto tendrá algun tipo de inclinación
                if element.hasAttribute('angle'):
                    angle = int(element.getAttribute('angle'))
                    self.text_render_normal = pygame.transform.rotozoom(self.text_render_normal, angle, 1)
                
                #Obtenemos la posicion del texto
                self.normal_text_rect = self.text_render_normal.get_rect()
                posx = int(element.getAttribute('x'))
                posy = int(element.getAttribute('y'))
                self.normal_text_rect = self.__set_rect_text(self.normal_text_rect, posx, posy)
            
            #Si hay opcion de cambio del color del texto cuando el botón esté seleccionado
            if len(parser.getElementsByTagName('selected_text')) > 0:
                #Obtenemos dicho texto
                for element in parser.getElementsByTagName('selected_text'):
                    
                    #tamaño
                    font_size = int(element.getAttribute('size'))
                    
                    #Color
                    r = int(element.getAttribute('r'))
                    g = int(element.getAttribute('g'))
                    b = int(element.getAttribute('b'))
                    color = (r, g, b)
                    
                    #Renderizamos
                    self.selected_font = resource.get_font(font_code, font_size)
                    self.text_render_selected = self.selected_font.render(self.text, True, color)
                    
                    #Si tiene opcion de angulo
                    if element.hasAttribute('angle'):
                        #Rotamos el texto renderizado
                        angle = int(element.getAttribute('angle'))
                        self.text_render_selected = pygame.transform.rotozoom(self.text_render_selected, angle, 1)
                    
                    #Asignamos la posición que tendrá
                    self.selected_text_rect = self.text_render_selected.get_rect()
                    posx = int(element.getAttribute('x'))
                    posy = int(element.getAttribute('y'))
                    self.selected_text_rect = self.__set_rect_text(self.selected_text_rect, posx, posy)
            #Si no hay opción de texto seleccionado, asignamos el mismo texto anterior
            else:
                self.text_render_selected = self.text_render_normal
                self.selected_text_rect = self.normal_text_rect
            
        self.selected = False
    
        #Obtenemos las mascaras de colisiones para los dos botones
        self.normal_mask = pygame.mask.from_surface(self.normal_image)
        self.selected_mask = pygame.mask.from_surface(self.selected_image)
        self.actual_mask = self.normal_mask
        self.show_text = show_text

    def draw(self, screen):
        '''
        @brief Método encargado de dibujar el boton en pantalla
        
        @param screen Supercifie destino
        '''
        #Superficie y rectangulo de destino auxiliar
        aux_surface = None
        destiny_rect = None
        
        #Si el boton esta seleccionado
        if self.selected:
            #Copiamos la imagen en la superficie y dibujamos el texto en el
            aux_surface = self.selected_image.copy()
            if self.show_text:
                aux_surface.blit(self.text_render_selected, self.selected_text_rect)
        
        #Si el botón no está seleccionado
        else:
            #Idem de lo anterior
            aux_surface = self.normal_image.copy()
            if self.show_text:
                aux_surface.blit(self.text_render_normal, self.normal_text_rect)
        
        #Dibujamos el resultado
        screen.blit(aux_surface, self.rect_draw)
        
    def update(self):
        '''
        @brief Método encargado de actualizar el botón
        '''
        #if self.rect_draw.collidepoint(pygame.mouse.get_pos()):
        
        #Comprobamos si el raton se encuentra dentro de la máscara de colisión
        if self.mask_collision(pygame.mouse.get_pos()):
            #Indicamos que el botón esta seleccionado
            self.selected = True
            self.rect_draw = self.selected_image.get_rect()
            self.actual_mask = self.selected_mask
        
        #Si no, pues lo contrario
        else:
            self.selected = False
            self.rect_draw = self.normal_image.get_rect()
            self.actual_mask = self.normal_mask
        
        #Actualizamos la posicion del centro del botón
        self.rect_draw.centery = self.centery
        self.rect_draw.centerx = self.centerx
        
    def get_selected(self):
        '''
        @brief Método que indica si el botón está seleccionado
        
        @return True si lo está, False en caso contrario
        '''
        return self.selected
    
    def set_selected(self, boolean):
        '''
        @brief Método que fuerza a un botón a estar seleccionado o no
        
        @param boolean Indica si el botón debe estar o no seleccionado
        '''
        self.selected = boolean
        
    def __set_rect_text(self, rect, posx, posy):
        '''
        @brief Método privado que situa el texto dentro de un botón según la opción de text_position
        '''
        if self.text_position == 'left':
            rect.x = posx
            rect.y = posy
        elif self.text_position == 'right':
            rect.x = posx - rect.w
            rect.y = posy
        elif self.text_position == 'bottom':
            rect.x = posx
            rect.y = posy - rect.h
        elif self.text_position == 'center':
            rect.centerx = posx
            rect.centery = posy
        else:
            rect.x = posx
            rect.y = posy
        return rect
        
    def get_option(self):
        '''
        @brief Método para obtener la opción de un botón
        
        @return El texto del boton que a la vez es su opción
        '''
        return self.text
    
    def set_option(self, new_text):
        '''
        @brief Método para asignar una nueva opcion al botón
        
        @param new_text Nuevo texto con la opción
        '''
        self.text = new_text
    
    def mask_collision(self, pos):
        '''
        @brief función que comprueba si dado una posicion x e y, se encuentra dentro de la máscara de colisión
        '''
        x = int(pos[0])
        y = int(pos[1])
        
        x -= self.rect_draw.x
        y -= self.rect_draw.y
        
        if 0 <= x < self.rect_draw.w and 0 <= y < self.rect_draw.h:
            return self.actual_mask.get_at((x, y))
    
    def get_width(self):
        '''
        @brief Método para consultar el ancho del botón
        
        @return El tamaño maximo de la imagen normal y seleccionada
        '''
        return max(self.rect_normal.w, self.rect_selected.w)
    
    def get_height(self):
        '''
        @brief Método para consultar el alto del botón
        
        @return El tamaño maximo de la imagen normal y seleccionada
        '''
        return max(self.rect_normal.h, self.rect_selected.w)
    
    def set_x(self, new_x):
        '''
        @brief Sitúa una nueva x en el botón
        '''
        self.rect_normal.x = new_x
        self.rect_selected.x = new_x
        

        

