#-*- encoding: utf-8 -*-

class State:
    '''
    Clase virtual pura que sirve como base de implementación de los
    distintos estados que esta compuesto el juego.
    '''
    def __init__(self, game):
        '''
        Constructor
        Recibe una referencia al game.
        '''
        self.game = game
    def update(self):
        '''
        Método que actualiza logicamente el estado.
        Debe ser implementado por los descendientes de state.
        '''
        raise NotImplemented("La funcion update de GameObject debe ser implementada por sus descendientes")
    def draw(self, screen):
        '''
        Método que dibuja el estado sobre la superficie dada.
        Debe ser implementado por los descentiendes de state.
        '''
        raise NotImplemented("La funcion update de State debe ser implementada por sus descendientes")
