#-*- encoding: utf-8 -*-

'''
@file gameanimation.py
@brief Implementa la clase GameAnimation
@author José Jesús Marente Florín
@date Mayo 2011.
'''

import gameobject
import data
import xml.dom.minidom

class GameAnimation(gameobject.GameObject):
    '''
    @brief Representa a una animación estatica del juego
    '''
    def __init__(self, game_control, path_xml, position_x, position_y):
        '''
        @brief Consturctor
        
        @param game_control Referencia a GameControl
        @param path_xml Xml con la animacion
        @param x Posicion en el eje x
        @param y Posicion en el eje y
        '''
        gameobject.GameObject.__init__(self, game_control)

        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        self.parser_basic_info(parse)
        
        self.rect.x = position_x
        self.rect.y = position_y
        
    def update(self):
        '''
        @brief Actualiza la animacion
        '''
        self.animations[gameobject.NORMAL].update()
        
        self.image = self.original_sprite.get_frame(self.animations[gameobject.NORMAL].get_frame())
