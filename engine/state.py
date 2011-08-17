#-*- encoding: utf-8 -*-

'''
@file state.py
Implementa la clase State
@author José Jesús Marente Florín
@date octubre 2010.
'''

class State:
    '''
    @brief Clase virtual pura que sirve como base de implementación de los 
    distintos estados que esta compuesto el juego.
    '''
    
    def __init__(self, game):
        '''
        @brief Constructor.
        
        @param screen Referencia al game.
        '''
        self.game = game
        
    def update(self):
        '''
        @brief Método que actualiza logicamente el estado. Debe ser implementado
        por los descendientes de state.
        '''
        raise NotImplementedError("Debe ser implementada por sus descendientes")
        
    def draw(self, screen):
        '''
        @brief Método que dibuja el estado sobre la superficie dada. Debe ser 
        implementado por los descentiendes de state.
        '''
        raise NotImplementedError("Debe ser implementada por sus descendientes")
