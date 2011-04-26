#-*- encoding: utf-8 -*-

import gameobject
import resource
import animation
import data
import xml.dom.minidom
import pygame

'''class GameAnimation(gameobject.GameObject):
    def __init__(self, game_control, path_xml, x, y):
        gameobject.GameObject.__init__(self, game_control)
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        self.parser_basic_info(parse)
        
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        
        self.animations[gameobject.NORMAL].update()
        
        self.image = self.original_sprite[self.animations[gameobject.NORMAL].get_frame()]'''

class GameAnimation(gameobject.GameObject):
    def __init__(self, game_control, path_xml, x, y):
        gameobject.GameObject.__init__(self, game_control)

        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))

        #self.new_animations = {}
        parent_node = parse.firstChild
        sprite_name = str(parent_node.getAttribute('sprite_code'))
        self.new_sprite = resource.get_new_sprite(sprite_name)
        
        #Cargamos las distintas animaciones del objeto
        for element in parse.getElementsByTagName('animation'):
            animation_name = str(element.getAttribute('name'))
            animation_frames = str(element.getAttribute('frames'))
            animation_delay = int(element.getAttribute('delay'))
            
            #Vemos que tipo de animación es y lo añadimos al mapa de imagenes
            if animation_name == 'normal':
                self.animations[gameobject.NORMAL] = animation.Animation(animation_frames, animation_delay)
        
        #Inicializamos la imagen, el rectangulo y la mascara de pixeles
        self.image = self.new_sprite.get_frame(self.animations[gameobject.NORMAL].get_frame())
        self.rect = self.image.get_rect()
        
        #self.parser_basic_info(parse)
        
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        
        self.animations[gameobject.NORMAL].update()
        
        #self.image = self.original_sprite[self.animations[gameobject.NORMAL].get_frame()]
        self.image = self.new_sprite.get_frame(self.animations[gameobject.NORMAL].get_frame())
