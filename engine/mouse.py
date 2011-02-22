#-*- encoding: utf-8 -*-

'''
@brief Módulo encargado de gestionar del ratón.
Simulación de patrón Singleton con el módulo.
Lleva el control de qué botones están pulsados y cuales no.
'''

import pygame

#Distintos botones del raton
LEFT, CENTER, RIGHT = range(3)

#Varianles
__actual_mouse = None
__old_mouse = None
__initialize = False

def __check_initialize():
    '''
    @brief Función que inicializa el ratón si no lo estaba
    '''
    global __actual_mouse
    global __old_mouse
    global __initialize
    
    if not __initialize:
        __actual_mouse = pygame.mouse.get_pressed()
        __old_mouse = pygame.mouse.get_pressed()
        __initialize = True

def update():
    '''
    @brief Función que actualiza el ratón, llamar en cada iteración del bucle principal
    '''
    global __actual_mouse
    global __old_mouse
    
    __check_initialize()
    __old_mouse = __actual_mouse
    __actual_mouse = pygame.mouse.get_pressed()
    
def pressed(button):
    '''
    @brief Consulta si un botón está pulsado
    
    @param button Botón a consultar
    @return True si lo está, False en caso contrario
    '''
    global __actual_mouse
    
    return __actual_mouse[button]

def release(button):
    '''
    @brief Consulta si un botón acaba de ser soltado
    
    @param button Botón a consultar
    @return True si lo está, False en caso contrario
    '''
    global __actual_mouse
    global __old_mouse
    
    return ((not __actual_mouse[button]) and __old_mouse[button])

def newpressed(button):
    '''
    @brief Consulta si un botón acaba de ser pulsado
    
    @param button Botón a consultar
    @return True si lo está, False en caso contrario
    '''
    global __actual_keyboard
    global __old_mouse
    
    return (__actual_mouse[button] and (not __old_mouse[button]))
    
def position():
    '''
    @brief Función que devuelve la posición del puntero del ratón
    
    @return Tupla con la posición x e y
    '''
    return pygame.mouse.get_pos()

