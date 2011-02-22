# -*- encoding: utf-8 -*-

'''
Módulo encargado de gestionar el telcado.
Simulación de patrón Singleton con el módulo.
Lleva el control de qué teclas están pulsadas en un momento determinado, 
cuáles se sueltan y cuáles se vuelven a presionar.
'''

import pygame
from pygame.locals import *

__actual_keyboard = None
__old_keyboard = None
__quit = False
__initialize = False

def __check_initialize():
    '''
    Inicializa el módulo si es la primera vez que se accede a él.
    '''
    global __actual_keyboard
    global __old_keyboard
    global __initialize
    
    if not __initialize:
        print "Inicializando modulo keyboard"
        __initialize = True
        __actual_keyboard = pygame.key.get_pressed()
        __old_keyboard = pygame.key.get_pressed()
    
def update():
    '''
    Actualiza el estado del teclado.
    Se debe llamar al principio del bucle principal.
    '''
    global __actual_keyboard
    global __old_keyboard
    global __quit
    
    __check_initialize()
    __old_keyboard = __actual_keyboard
    __actual_keyboard = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            __quit = True


def pressed(key):
    '''
    True si la tecla Key está pulsada, False en caso contrario.
    '''
    return __actual_keyboard[key]

def release(key):
    '''
    True si la tecla Key estaba antes pulsada en la última actualización y ahora no lo está, False en caso contrario.
    '''
    return (__old_keyboard[key] and (not __actual_keyboard[key]))
    
def newpressed(key):
    '''
    True si la tecla Key NO estaba antes pulsada en la última actualización y ahora lo está, False en caso contrario.
    '''
    return (__actual_keyboard[key] and (not __old_keyboard[key])) 
    
def quit():
    '''
    True si se produce el evento de salida, False en caso contrario.
    '''
    return __quit
