#-*- encoding: utf-8 -*-

import pygame
import circuit
import basiccar

class CollisionManager:
    '''
    Clase encargada de comprobar si se a producido algun tipo de colision,
    tanto entre objetos, como objetos con los elemento del circuito.
    '''
    def __init__(self):
        pass
    def actor_perfectcollision(self, sprite1, sprite2):
        '''
        Comprueba la colision pixel por pixel.
        '''
        return pygame.sprite.collision_mask(sprite1, sprite2)
        
    def actor_rectanglecollision(self, sprite1, sprite2):
        '''
        Comprueba la colision de los rectangulos de los sprites
        '''
        return pygame.sprite.collision_rect(sprite1, sprite2)
        
    def actor_edgecollision(self, sprite1, sprite2):
        '''
        Devuelve un diccionario indicando por que filos 
        han colisionado los sprites.
        '''
        rect1 = sprite1.get_rect()
        rect2 = sprite2.get_rect()
        edge = {"left": False, "right": False, "top": False, "bottom": False}
        
        if self.actor_perfectcollision(sprite1, sprite2):
            
            if (rect1.left - rect2.left) > 0:
                edge["right"] = True
                
            if (rect1.left - rect2.left) < 0:
                edge["left"] = True
                
            if (rect1.top - rect2.top) > 0:
                edge["bottom"] = True
                
            if (rect1.top - rect2.top) < 0:
                edge["top"] = True
        
        return edge
        
    def tile_collision():
        pass
    def level_collision(self, sprite, circ):
        '''
        Comprueba la colision de los objetos con los elementos del circuito,
        si se produce alguna colisión, se corrige la posicion del objeto.
        '''
        #Comprobamos el eje X.
        x_collision = False
        y_collision = False
        tile_pos = None
        
        #Colisiones verticales, con el eje x
        if sprite.go_left():
            tile_pos_x1 = self.__collision_ver(sprite, circ, "left")
            if tile_pos_x1:
                x_collision = True
                print "Colision en el eje x"
                print tile_pos
                sprite.rect.x = tile_pos_x1 + circ.get_tile_width() + 1
                sprite.actual_speed *= -1
            else:
                print "No hay colision en el eje x"
        elif sprite.go_right():
            tile_pos_x2 = self.__collision_ver(sprite, circ, "right")
            if tile_pos_x2:
                x_collision = True
                sprite.rect.x = tile_pos_x2 - sprite.rect.w
                sprite.actual_speed *= -1
        
        #Colisiones horizontales, con el eje y
        if sprite.go_up():
            tile_pos_y1 = self.__collision_hor(sprite, circ, "up")
            if tile_pos_y1:
                y_collision = True
                print "Colision en el eje Y"
                sprite.rect.y = tile_pos_y1  + circ.get_tile_height() + 1
                sprite.actual_speed *= -1
            else:
                print "No hay colision en el eje y"
                
        '''elif sprite.go_down():
            tile_pos_y2 = self.__collision_hor(sprite, circ, "down")
            if tile_pos_y2:
                y_collision = True
                sprite.rect.y = tile_pos_y2 - sprite.rect.h
                sprite.actual_speed *= 1'''
            
    def __collision_ver(self, sprite, circ, side):

        tile_y0 = sprite.rect.y / circ.get_tile_height()
        tile_y1 = (sprite.rect.y + sprite.rect.h) / circ.get_tile_height()
        if side == "left":
            tilecoordx = sprite.rect.x / circ.get_tile_width()
        else:
            tilecoordx = (sprite.rect.x + sprite.rect.w) / circ.get_tile_width()
        
        i = tile_y0
        
        while i <= tile_y1:
            if (circ.get_tile(1, tilecoordx, i).type == circuit.NOPASSABLE) or \
            (circ.get_tile(0, tilecoordx, i).type == circuit.NOPASSABLE):
                tilecoordx *= circ.get_tile_width();
                return tilecoordx
            i += 1
        
        return False
            
    def __collision_hor(self, sprite, circ, side):

        tile_x0 = sprite.rect.x / circ.get_tile_width()
        tile_x1 = (sprite.rect.x + sprite.rect.w) / circ.get_tile_width()
        if side == "up":
            tilecoordy = sprite.rect.y /circ.get_tile_height()
        else:
            tilecoordy = (sprite.rect.y + sprite.rect.h) /circ.get_tile_height()
        
        i = tile_x0
        
        while i <= tile_x1:
            if (circ.get_tile(1, i, tilecoordy).type == circuit.NOPASSABLE) or \
            (circ.get_tile(0, i, tilecoordy).type == circuit.NOPASSABLE):
                tilecoordy *= circ.get_tile_height()
                return tilecoordy
            i += 1
            
        return False
