#-*- encoding: utf-8 -*-

'''
@file slider.py
@brief Implementa la clase Slider
@author José Jesús Marente Florín
@date Diciembre 2010.
'''

import pygame
import xml.dom.minidom
import data
import resource
import mouse

class Slider:
    '''
    @brief Clase que representa un slider
    '''
    def __init__(self, xml_path, actual_value, max_value, x, y, option = ''):
        '''
        @brief Constructor.
        
        @param xml_path Ruta del archivo xml.
        @param actual_value Valor actual que tendrá 
        @param max_value Valor máximo que puede alcanzar
        @param x Posición en el eje x
        @param y Posición en el eje y
        '''
        parse = xml.dom.minidom.parse(data.get_path_xml(xml_path))
        
        bar = parse.getElementsByTagName('bar')
        
        #Obtenemos la imagen que representará la barra
        image_code = str(bar[0].getAttribute('image_code'))
        self.bar_image = resource.get_image(image_code)
        
        #Indicamos su posicion
        self.bar_rect = self.bar_image.get_rect()
        self.bar_rect.x = x
        self.bar_rect.y = y
        
        #Obtenemos la imagen que representará al controlador
        controler = parse.getElementsByTagName('controler')
        image_code = str(controler[0].getAttribute('image_code'))
        self.controler_image = resource.get_image(image_code)
        
        #Indicamos su posición inicial
        self.controler_rect = self.controler_image.get_rect()
        self.controler_rect.centerx = self.bar_rect.centerx
        self.controler_rect.centery = self.bar_rect.centery
        
        #Cargamos la fuente con la que se representará el valor
        font = parse.getElementsByTagName('font')
        font_code = str(font[0].getAttribute('font_code'))
        self.font = resource.get_font(font_code, 30)
        r = int(font[0].getAttribute('r'))
        g = int(font[0].getAttribute('g'))
        b = int(font[0].getAttribute('b'))
        self.color_font = (r, b, g)
        
        self.max_value = max_value
        self.min_value = 0
        self.actual_value = actual_value
        self.update_controler()
        self.still_pressed = self.new_pressed = False
        self.option = option
        
    def update(self):
        '''
        @brief Método encargado de actualizar el slider
        '''
        #Si estamos pulsando el ratón y esta sobre el controlador, la linea o 
        #ya estaba el raton pulsado anteriormente
        if (mouse.newpressed(mouse.LEFT) and \
            (self.controler_rect.collidepoint(pygame.mouse.get_pos()) \
            or self.bar_rect.collidepoint(pygame.mouse.get_pos()))) \
            or self.still_pressed:
            
            #Actualizamos la posición del controlador
            self.controler_rect.centerx = pygame.mouse.get_pos()[0]
            
            #Indicamos que esta pulsado el ratón
            self.still_pressed = True
            self.new_pressed = False
            
            #Controlamos que el controlador no se salga de la barra
            if self.controler_rect.centerx >= (self.bar_rect.x + self.bar_rect.w):
                self.controler_rect.centerx = self.bar_rect.x + self.bar_rect.w
                
            elif self.controler_rect.centerx <= self.bar_rect.x:
                self.controler_rect.centerx = self.bar_rect.x
            
            #Actualizamos el valor según la posición del controlador
            self.update_value()
        
        #Si no esta pulsado el botón del raton, lo indicamos
        if not pygame.mouse.get_pressed()[0]:
            self.still_pressed = False
                
    def draw(self, screen):
        '''
        @brief Método encargado de mostrar el slider en pantalla
        
        @param screen Superficie destino
        '''
        #Renderizamos el valor actual
        value_render = self.font.render(str(self.actual_value), True, 
                                    self.color_font)
        
        #Asignamos la posición
        value_rect = value_render.get_rect()
        value_rect.x = self.bar_rect.x + self.bar_rect.w + 10
        value_rect.centery = self.bar_rect.centery
        
        #Dibujamos recta, controlador y valor
        screen.blit(self.bar_image, self.bar_rect)
        screen.blit(self.controler_image, self.controler_rect)
        screen.blit(value_render, value_rect)
        
    def get_value(self):
        '''
        @brief Método consultor del valor actual
        
        @return Valor actual
        '''
        return self.actual_value
        
    def set_value(self, new_value):
        '''
        @brief Método para establecer un nuevo valor actual
        
        @param new_value Nuevo valor actual
        '''
        if new_value >= self.min_value and new_value <= self.max_value:
            self.actual_value = new_value
    
    def update_value(self):
        '''
        @brief Función encargada de actualizar el valor actual en función de 
        la posición del controlador sobre la barra
        '''
        posicion_100 = self.bar_rect.w
        posicion_barra = self.controler_rect.centerx - self.bar_rect.x - self.bar_rect.w
        self.actual_value = (posicion_barra * self.max_value / posicion_100) + self.max_value
    
    def update_controler(self):
        '''
        @brief Función encargada de actualizar la posición del controlador en 
        función del valor actual del slider
        '''
        posicion_100 = self.bar_rect.w
        posicion = (self.actual_value * posicion_100) / self.max_value
        self.controler_rect.centerx = posicion + self.bar_rect.x
    
    def get_option(self):
        '''
        @brief Devuelve la opción del slider
        '''
        return self.option
