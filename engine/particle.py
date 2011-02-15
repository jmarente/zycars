#-*- encoding: utf-8 -*-

'''
@file particle.py
Implementa la clase Particle, SystemParticle, basado en las clases Particula y 
SistemaParticulas de José Tomás Tocino García del proyecto oflute.
@author José Jesús Marente Florín
@date Febrero 2011.
'''

import pygame
import resource
import math
import random
import time
from random import randint

class Particle:
    '''
    @brief Clase que controla el comportamiento de una particula
    '''
    def __init__(self, angle, distance, scale, image, speed, rotation):
        '''
        @brief Constructor.
        
        @param angle Ángulo de desplazamiento
        @param distance Distancia máxima que puede alcanzar desde el origen
        @param scale Escala que tendrá la imagen
        @param speed Velocidad de la particula
        @param rotation Rotación de la imagen
        '''
        #self.angle = math.radians(angle)
        #Asignamos los distintos valores
        self.angle = angle
        self.distance = distance
        self.scale = scale
        
        #Escalamos y rotamos la imagen
        self.image = pygame.transform.rotozoom(image, rotation, scale)
        #self.image.convert_alpha(self.image)
        #self.image = self.image.set_alpha(0, pygame.RLEACCEL)
        '''self.actual_step = 0
        self.dx = speed * randint(-1, 1) * random.random()
        self.dy = speed* randint(-1, 1) * random.random()'''
        self.speed = speed
        self.x = 0
        self.y = 0
        self.status = "normal"
        
    def update(self):
        '''
        @brief Método que actualiza lógicamente el comportamiento de la particula
        '''
        #Si estamos en estado normal
        if self.status == 'normal':
            #Actualizamos la posición de la particula
            self.x = math.cos(self.angle) * self.speed + self.x
            self.y = math.sin(self.angle) * self.speed + self.y
        
            '''self.x += self.dx
            self.y += self.dy'''
            #Si no está en los limites de distancia, indicamos que acaba su ejecución
            if abs(self.x) > self.distance or abs(self.y) > self.distance:
                self.status = "done"
              
    def draw(self, screen, source_x, source_y):
        '''
        @brief Método encargado de dibujar la particula en pantalla
        
        @param screen Superficie destino
        @param source_x Origen x
        @param source_y Origen y
        '''
        #Si está en estado normal lo mostramos por pantalla
        if self.status == "normal":
            screen.blit(self.image, (source_x + self.x, source_y + self.y))
        
    def get_status(self):
        '''
        @brief Método que indica el estado actual de la particula
        
        @return Estado actual del elemento
        '''
        return self.status

class SystemParticle:
    '''
    @brief Clase que simula el comportamiento de una explosión mediante un sistema de particulas
    '''
    def __init__(self, x, y, images_code, number, duration, speed, distance=200, scale = 1):
        '''
        @brief Constructor
        
        @param x Posición x del origen
        @param y Posición y del origen
        @param images_code Lista con los códigos de imagen
        @param number Número de particulas
        @param duration Duración en segundos del sistema
        @param speed Velocidad máxima que pueden alcanzar las particulas
        @param distance Distancia máxima que pueden alcanzar
        @param scale Escala máxima que tendrán las imagenes de las particulas
        '''
        #Asinamos los distintos parametros
        self.x = x
        self.y = y
        self.images_code = images_code
        self.number = number
        self.duration = duration
        self.distance = distance
        self.scale = scale 
        self.speed = speed
        
        #Lista de particulas
        self.particles = []
        
        self.status = 'normal'
        self.__start = None
        
        #Insertamos las particulas en la lista
        self.__insert_particles()

    def update(self):
        '''
        @brief Método que actualiza el sistema de particulas
        '''
        #Si es la primera vez que llamamos al método
        if not self.__start:
            #obtenemos el tiempo actual
            self.__start = time.time()
            
        #Si no
        else:
            #Calculamos el tiempo que lleva ejecutandose el sistema
            actual = time.time() - self.__start
            #si a superado el tiempo, lo indicamos
            if actual >= self.duration:
                self.status = 'done'
                
        #Actualizamos cada una de las particulas
        for particle in self.particles:
            particle.update()
            
    def draw(self, screen):
        '''
        @brief Método que dibuja las particulas en pantalla
        
        @param screen Superficie de destino
        '''
        for particle in self.particles:
            particle.draw(screen, self.x, self.y)
    
    def get_status(self):
        '''
        @brief Método para consultar el estado del sistema de particulas
        
        @return done si ya terminó o normal si no
        '''
        return self.status
    
    def restart(self):
        '''
        @brief Método que reinicia el sistema de particulas
        '''
        #Reiniciamos variables
        self.status = 'normal'
        self.__start = None
        self.particles = []
        
        #Insertamos las particulas en la lista
        self.__insert_particles()
        
    def __insert_particles(self):
        '''
        @brief Método privado encargado de insertar particulas en la lista
        '''
        #Insertamos cada una de las particulas en la lista
        for i in range(0, self.number):
            
            #Obtenemos el código de una imagen aleatoria de la lista de códigos
            image = resource.get_image(self.images_code[randint(0, len(self.images_code ) - 1)])
            
            particle = Particle(randint(0, 360),#Obtenemos un angulo aleatorio
                                        random.uniform(0.1, self.distance),#Distancia máxima aleatoria
                                        random.uniform(0.1, self.scale),#Escala aleatoria
                                        image,#Imagen en cuestión
                                        random.uniform(0.1, self.speed),#Velocidad aleatoria
                                        randint(0,360))
            #Insertamos una nueva particula
            self.particles.append(particle)#Rotación de la imagen 
        
