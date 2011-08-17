#-*- encoding: utf-8 -*-

'''
@file timer.py
Implementa la clase Timer
@author José Jesús Marente Florín
@date Enero 2011.
'''

import time
import resource

class Timer:
    '''
    @brief Clase Timer, simula el comportamiento de de un cronómetro.
    '''
    def __init__(self, font_code, font_size, color, x, y, text, minutes = 0, 
                seconds = 0, hseconds = 0):
        '''
        @brief Constructor de timer.
        
        @param font_code Código de la fuente a usar.
        @param font_size Tamaño de la fuente.
        @param color Color de la fuente.
        @param x Posición en el eje x.
        @param y Posición en el eje y.
        @param text Texto que representará al cronómetro.
        @param minutes Minutos iniciales, por defecto 0.
        @param seconds Segundos iniciales, por defecto 0.
        @param hseconds Centésimas de segundo inidicales, por defecto 0.
        '''
        
        #Pasamos los minutos a segundos
        self.__start = minutes * 60.0
        #Añadimos los segundos
        self.__start += seconds
        #Pasamos las centésimas de segundo a segundos
        self.__start += hseconds / 100.0
        
        #Asignamos variable
        self.minutes = minutes
        self.seconds = seconds
        self.hseconds = hseconds
        
        #Chivatos
        self.running = False
        self.time_paused = False
        self.time_stopped = False
        
        #Cargamos la fuente necesaria
        self.font = resource.get_font(font_code, font_size)
        self.color = color
        self.x = x
        self.y = y
        
        #Obtenemos la superficie con el texto dado
        self.text = self.font.render(text, True, color)
        self.rect_text = self.text.get_rect()
        self.surface = None
        self.update_surface()
        
    def update(self):
        '''
        @brief Actualiza el estado del cronómetro
        '''
        #si el cronómetro esta en marcha
        if self.running:
            
            #Obtenemos el tiempo transcurrido
            elap = time.time() - self.__start
            
            #Hacemos las distintas conversiones
            #Obtenemos los minutos
            self.minutes = int(elap / 60) 
            #Obtenemos los segundos, restando los minutos anteriores
            self.seconds = int(elap - self.minutes * 60.0)
            #Obtenemos las centésimas de segundo, restando tanto minutos, 
            #como segundos anteriores
            self.hseconds = int((elap - self.minutes * 60.0 - self.seconds) * 100)
            
            #Actualizamos la superficie del cronometro
            self.update_surface()
            
    def draw(self, screen):
        '''
        @brief Dibuja los distintos elementos en pantalla
        
        @param screen Superficie destino
        '''
        screen.blit(self.text, (self.x, self.y))
        screen.blit(self.surface, (self.x, self.y + self.rect_text.h)) 
        
    def start(self):
        '''
        @brief Pone el cronómetro en marcha
        '''
        #Si el cronometro estaba parado, los reiniciamos
        if self.time_stopped:
            self.__start = time.time()
            self.time_stopped = False
        #Si no estaba en marcha o estaba pausado, comenzamos desde donde estaba
        elif not self.running or self.time_paused:
            self.__start = abs(self.__start - time.time())

        self.running = True 

    def stop(self):
        '''
        @brief Detiene y reinicia el cronómetro
        '''
        self.running = False
        self.time_stopped = True
        self.minutes = self.seconds = self.hseconds = 0
        self.update_surface()
    
    def pause(self):
        '''
        @brief Pausa el cronómetro
        '''
        self.running = False
        
        #Guardamos los valores actuales
        self.__start = self.minutes * 60.0
        self.__start += self.seconds
        self.__start += self.hseconds / 100.0
        
    def get_minutes(self):
        '''
        @brief Método que devuelve los minutos actuales
        '''
        return self.minutes
        
    def set_minutes(self, new_value):
        '''
        @brief Situa un nuevo valor para los minutos, preservando los segundos 
        y centésimas anteriores
        
        @param new_value nuevo valor para los minutos
        '''
        self.minutes =  new_value
        self.__start = new_value * 60
        self.__start += self.seconds
        self.__start += self.hseconds / 100.0        
        self.update_surface()
        
    def get_seconds(self):
        '''
        @brief Método que devuelve los segundos actuales
        '''
        return self.seconds 
        
    def set_seconds(self, new_value):
        '''
        @brief Situa un nuevo valor para los segundos, preservando los minutos
         y centésimas anteriores
        
        @param new_value nuevo valor para los segundos
        '''
        self.seconds = new_value
        self.__start = new_value
        self.__start += self.minutes * 60
        self.__start += self.hseconds / 100.0
        self.update_surface()

    def get_hseconds(self):
        '''
        @brief Método que devuelve las centésimas de segundo actuales
        '''
        return self.hseconds
        
    def set_hseconds(self, new_value):
        '''
        @brief Situa un nuevo valor para los segundos, preservando los minutos
         y segundos anteriores
        
        @param new_value nuevo valor para las centesimas
        '''
        self.hseconds = new_value
        self.__start = new_value / 100        
        self.__start += self.minutes * 60
        self.__start += self.seconds
        self.update_surface()
    
    def update_surface(self):
        '''
        @brief Método que actualiza la superficie del cronómetro
        '''
        string = '%02d:%02d:%02d' % (self.minutes, self.seconds, self.hseconds)
        self.surface = self.font.render(string, True, self.color)
    
    def assign(self, timer):
        '''
        @brief Método que actualiza un cronometo, con los datos de otro
        
        @param timer Recibe un nuevo timer, del que obtendrá todos los campos
        '''
        #Pasamos los minutos a segundos
        self.__start = timer.get_minutes() * 60.0
        #Añadimos los segundos
        self.__start += timer.get_seconds()
        #Pasamos las centésimas de segundo a segundos
        self.__start += timer.get_hseconds() / 100.0
        
        #Asignamos variable
        self.minutes = timer.get_minutes()
        self.seconds = timer.get_seconds()
        self.hseconds = timer.get_hseconds()
        self.update_surface()
    
    def less_than(self, timer):
        '''
        @brief Método que comprueba si el timer es menor que el que pasamos
        
        @param timer Timer a comparar
        @return True si el timer pasado el mayor, False si es menor o igual
        '''
        if self.minutes < timer.get_minutes():
            return True 
                  
        elif self.minutes == timer.get_minutes():
            
            if self.seconds < timer.get_seconds():
                return True
            elif self.seconds == timer.get_seconds():
                
                if self.hseconds < timer.get_hseconds():
                    return True
                return False
                
            return False

        return False
    
    def like(self, timer):
        '''
        @brief Método que comprueba si dos timer tienen el mismo valor.
        
        @param timer Timer a comparar
        @return True si son iguales, false en caso contrario
        '''
        if self.minutes == timer.get_minutes() and \
            self.seconds == timer.get_seconds() and\
            self.hseconds == timer.get_hseconds():
            return True
        return False
    
    def more_than(self, timer):
        '''
        @brief Método que comprueba si el timer es mayor que el que pasamos
        
        @param timer Timer a comparar
        @return True si el timer pasado es menor, False si es mayor o igual
        '''
        if not self.like(timer) and not self.less_than(timer):
            return True
        return False

