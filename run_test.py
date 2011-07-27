#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@author Jose J. Marente Florin
@brief Encargdo de iniciar el juego
'''

from engine import game

def main():
    '''
    @brief Función main del juego.
    '''
    zycars = game.Game()
    zycars.run()
    
if __name__ == "__main__":
    main()
