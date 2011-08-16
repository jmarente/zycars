#-*- encoding: utf-8 -*-

'''
@file itembox.py
Implementa la clase ItemBox
@author José Jesús Marente Florín
@date Febrero 2011.
'''

import gameobject
import particle
import data
import xml.dom.minidom

class ItemBox(gameobject.GameObject):
    '''
    @brief Clase que simula el comportamiento de las "cajas" de items 
    '''
    def __init__(self, game_control, xml_path, x, y):
        '''
        @brief Constructor.
        
        @param game_control Referencia a GameControl
        @param xml_path Ruta del archibo xml con la configuración
        @param x posición en el eje x
        @param y posición en el eje y
        '''
        gameobject.GameObject.__init__(self, game_control)

        #Parseamos la información básica
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_path))
        self.parser_basic_info(parser)
        
        #Establecemos posiciones
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        #Creamos el sistema de particulas, para cuando colisionemos con la caja
        self.particles = particle.SystemParticle(self.game_control, 
                                                self.rect.centerx, 
                                                self.rect.centery, 
                                                ['particle'], 25, 1, 5, 
                                                100, 0.5)

        #Establecemos las funciones a tratar según el estado
        self.states = {gameobject.NORMAL: self.__normal_state,
                    gameobject.EXPLOSION: self.__explosion_state
                    }
                    
        self.update_image()
        
    def draw(self, screen):
        '''
        @brief Método que dibuja el elemento en pantalla
        
        @param screen Superficie destino
        '''
        #Si el estado no es de explosión dibujamos normal
        if self.state != gameobject.EXPLOSION:
            gameobject.GameObject.draw(self, screen)
            
        #Si el estado es de explosión dibujamos el sistema de particulas
        else:
            self.particles.draw(screen)
            
    def update(self):
        '''
        @brief Método que actualiza lógicamente la caja de item
        '''
        #Controlamos el cambio de estado para reiniciar la animación
        if self.state != self.previous_state:
            self.previous_state = self.state
            if self.state != gameobject.EXPLOSION:
                self.animations[self.state].restart()
        
        #Llamamos a la función del estado actual para actualizar
        self.states[self.state]()
        
        #self.update_image()
        
    def __normal_state(self):
        '''
        @brief Método privado que actualiza la caja de item cuando esta en su estado normal
        '''
        self.animations[self.state].update() 
        
        self.image = self.original_sprite.get_frame(self.animations[self.state].get_frame())
    
    def __explosion_state(self):
        '''
        @brief Método privado que actualia la caja cuando esta en estado de explosión
        '''
        #Actualizamos el sistema de particulas
        self.particles.update()
        
        #Si se ha acabado, cambiamos el estado de la caja y 
        #reiniciamos el sistema de particulas
        if self.particles.done():
            self.particles.restart()
            self.state = gameobject.NORMAL 
