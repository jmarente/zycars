#-*- encoding: utf-8 -*-

'''
@file start.py
Implementa la clase Start
@author José Jesús Marente Florín
@date Febrero 2011.
'''

import resource
import pygame
import playercar
import ia

class Start:
    '''
    @brief Clase encargada de situar la linea de salida en el circuito, así como
    los distinos coches que compitan
    '''
    def __init__(self, game_control, circuit, x, y, image_code, orientation, car_angle):
        '''
        @brief Constructor.
        
        @param game_control Referencia a GameControl
        @param circuit Referencia a Circuit
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param image_code Código de la imagen(será del mismo ancho y algo que los tiles de circuito)
        @param orientation Indica si la linea será horizontal o vertical
        @param car_angle angulo para situar al coche
        '''
        #Referencias
        self.game_control = game_control
        self.circuit = circuit
        
        #Posición
        self.x = x
        self.y = y
        
        #Imagen
        self.image = resource.get_image(image_code)
        
        self.orientation = orientation

        #Si hemos indicado que la posición es vertical
        if orientation == 'vertical':
            #Obtenemos una superfice con el ancho de la "carretera" del circuito como referencia
            '''self.surface = pygame.Surface((self.image.get_width(), self.image.get_height() * self.circuit.get_circuit_width()))
            self.surface.set_alpha(0)
            aux_y = 0'''
            
            '''#Sobre la superficie anterior dibujamos tantas imagenes como ancho sea el circuito
            for i in range(self.circuit.get_circuit_width()):
                self.surface.blit(self.image, (0, aux_y))
                aux_y += self.image.get_height()'''
            
            #Situamos al coche según el angulo indicado
            
            #A la izquierda de la linea
            if car_angle >= 0 and car_angle < 90:
                self.game_control.add_player(playercar.PlayerCar(self.game_control, 
                'cars/coche_prueba_yellow.xml', self.x - self.circuit.get_tile_width(), 
                self.y + self.circuit.get_tile_height() * 2, 0))
            
            #A la derecha de la linea
            elif car_angle >= 180 and car_angle < 270:
                self.game_control.add_player(playercar.PlayerCar(self.game_control, 
                'cars/coche_prueba_yellow.xml', self.x + self.surface.get_width() + self.circuit.get_tile_width(), 
                self.y + self.circuit.get_tile_height() * 2, 180))
        
        #Si por el contrario la posición es horizontal
        else:
            #Creamos una superficie con el alto de la carretera del circuito como referencia
            '''self.surface = pygame.Surface((self.image.get_width() * self.circuit.get_circuit_width(), self.image.get_height()))
            self.surface.set_alpha(0)
            aux_x = 0'''
            
            '''#Sobre la superficie anterior dibujamos tantas imagenes como ancho sea el circuito
            for i in range(self.circuit.get_circuit_width()):
                self.surface.blit(self.image, (aux_x, 0))
                aux_x += self.image.get_width()'''
            
            #Situamos el coche en el angulo adecuado
            
            #Debajo de la linea
            if car_angle == 90:
                self.game_control.add_player(playercar.PlayerCar(self.game_control, 
                'cars/coche_prueba_yellow.xml', self.x + self.circuit.get_tile_width() * 2, 
                self.y - self.circuit.get_tile_height(), 90))
            
            #Arriba de la linea
            elif car_angle == 270:
                self.game_control.add_player(playercar.PlayerCar(self.game_control, 
                'cars/coche_prueba_yellow.xml', self.x + self.circuit.get_tile_width() * 2, 
                self.y + self.circuit.get_tile_height() * 2, 270))
                
                self.game_control.add_ia_car(ia.IA(self.game_control, 
                'cars/coche_prueba_purple.xml', self.x + self.circuit.get_tile_width() * 3, 
                self.y + self.circuit.get_tile_height() * 2, 270))
                
                
            
    def draw(self, screen):
        '''
        @brief Método que dibuja la linea de meta en pantalla
        
        @param screen Superficie destino
        '''
        #screen.blit(self.surface, (self.x - self.game_control.circuit_x(), self.y - self.game_control.circuit_y()))
        
        #Segun la orientación de la linea de meta, la dibujamos de una forma u otra
        if self.orientation == 'vertical':
            aux_y = 0
            for i in range(self.circuit.get_circuit_width()):
                screen.blit(self.image, (self.x - self.game_control.circuit_x(), \
                            aux_y + self.y - self.game_control.circuit_y()))
                #Obtenemos la posicion de la siguiente
                aux_y += self.image.get_height()
        else:
            aux_x = 0
            for i in range(self.circuit.get_circuit_width()):
                screen.blit(self.image, (aux_x + self.x - self.game_control.circuit_x(), \
                            self. y - self.game_control.circuit_y()))
                #Obtenemos la posicion de la siguiente
                aux_x += self.image.get_width()
