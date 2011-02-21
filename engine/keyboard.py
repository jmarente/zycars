# -*- encoding: utf-8 -*-

'''
@brief Módulo encargado de gestionar el telcado.
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
    @brief Inicializa el módulo si es la primera vez que se accede a él.
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
    @brief ctualiza el estado del teclado. 
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
    @brief Consulta si una tecla determinada está pulsada o no.
    
    @param key Tecla a consultar
    @para True si la tecla Key está pulsada, False en caso contrario.
    '''
    return __actual_keyboard[key]

def release(key):
    '''
    @brief Consulta si se ha soltado una tecla.
    
    @param key Tecla a consultar
    @return True si la tecla Key estaba antes pulsada en la última actualización 
    y ahora no lo está, False en caso contrario.
    '''
    return (__old_keyboard[key] and (not __actual_keyboard[key]))
    
def newpressed(key):
    '''
    @brief Consulta si una tecla se a pulsado y antes no lo estaba
    
    @param Tecla a consultar
    @param True si la tecla Key NO estaba antes pulsada en la última actualización 
    y ahora lo está, False en caso contrario.
    '''
    return (__actual_keyboard[key] and (not __old_keyboard[key])) 
    
def quit():
    '''
    @brief Indica si se a producido algun evento de salida
    
    @return True si se produce el evento de salida, False en caso contrario.
    '''
    return __quit

def set_quit(new_value):
    '''
    @brief Le da una nuevo valor a la variable quit para indicar que se cierre el juego
    '''
    global __quit
    __quit = new_value
