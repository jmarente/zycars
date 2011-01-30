#-*- encoding: utf-8 -*-

import pygame
import circuit
import basiccar
import gameobject

from log import Log

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
        
    def actor_tile_edgecollision(self, sprite, tile_rect):
        
        sprite_rect = sprite.get_rect()
        edge = {"left": False, "right": False, "top": False, "bottom": False}
        Log().debug('Coche: (' + str(sprite_rect.x) + ', ' + str(sprite_rect.y) + ', ' + str(sprite_rect.w) + ', ' + str(sprite_rect.h) + ')')
        Log().debug('Tile: (' + str(tile_rect.x) + ', ' + str(tile_rect.y) + ', ' + str(tile_rect.w) + ', ' + str(tile_rect.h) + ')')

        if sprite_rect.colliderect(tile_rect):
        
            if (sprite_rect.left - tile_rect.left) > 0:
                edge["right"] = True
                Log().debug("Collision por la derecha")

                
            if (sprite_rect.left - tile_rect.left) < 0:
                edge["left"] = True
                Log().debug("Collision por la izquierda")

            if (sprite_rect.top - tile_rect.top) > 0:
                edge["bottom"] = True
                Log().debug("Collision por abajo")

            if (sprite_rect.top - tile_rect.top) < 0:
                edge["top"] = True
                Log().debug("Collision por arriba")
                
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
        tile_rect = None
        
        #Colisiones verticales, con el eje x
        if sprite.go_left():
            tile_rect = self.__collision_ver(sprite, circ, "left")
            
        elif not tile_rect and sprite.go_right():
            tile_rect = self.__collision_ver(sprite, circ, "right")
            
        #Colision horizontales, con el eje y
        elif not tile_rect and sprite.go_up():
            tile_rect = self.__collision_hor(sprite, circ, "up")
            
        elif not tile_rect and sprite.go_down():
            tile_rect = self.__collision_hor(sprite, circ, "down")
            
        if tile_rect:
            
            edge = self.actor_tile_edgecollision(sprite, tile_rect)
                        
            collision = collision_top = collision_bottom = \
            collision_left = collision_right = False
                
            if edge['left'] and edge['bottom']:
                left_car = tile_rect.left - sprite.rect.left
                bottom_car = sprite.rect.bottom - tile_rect.bottom
                
                if left_car > bottom_car:
                    Log().info('Corregiriamos colision por la izquierda')
                    collision_left = True
                elif left_car < bottom_car:
                    Log().info('Corregiriamos colision por abajo')
                    collision_bottom = True
                    
            elif edge['left'] and edge['top']:
                left_car = tile_rect.left - sprite.rect.left
                top_car = tile_rect.top - sprite.rect.top
                
                if left_car > top_car:
                    Log().info('Corregiriamos colision por la izquierda')
                    collision_left = True
                elif left_car < top_car:
                    Log().info('Corregiriamos colision por arriba')
                    collision_top = True
                                    
            elif edge['right'] and edge['bottom']:
                right_car = sprite.rect.right - tile_rect.right
                bottom_car = sprite.rect.bottom - tile_rect.bottom
                
                if right_car > bottom_car:
                    Log().info('Corregiriamos colision por la derecha')
                    collision_right = True
                elif right_car < bottom_car:
                    Log().info('Corregiriamos colision por abajo')
                    collision_bottom = True
                
            elif edge['right'] and edge['top']:
                right_car = sprite.rect.right - tile_rect.right
                top_car = tile_rect.top - sprite.rect.top
                
                if right_car > top_car:
                    Log().info('Corregiriamos colision por la derecha')
                    collision_right = True
                elif right_car < top_car:
                    Log().info('Corregiriamos colision por arriba')
                    collision_top = True
            
            Log().info(str(sprite.actual_speed))
            
            if collision_right:
                sprite.rect.x = tile_rect.x + tile_rect.w
                collision = True
                
            elif collision_left:
                sprite.rect.x = tile_rect.x - sprite.rect.w
                collision = True
                
            elif collision_bottom:
                sprite.rect.y = tile_rect.y + tile_rect.h
                collision = True
                
            elif collision_top:
                sprite.rect.y = tile_rect.y - sprite.rect.h
                collision = True
            
            if collision:
                if sprite.get_state() == gameobject.REVERSE or \
                (sprite.get_state() == gameobject.NOACTION and sprite.get_old_state() == gameobject.REVERSE):
                    sprite.actual_speed = -sprite.get_max_speed()
                else:
                    sprite.actual_speed = sprite.get_max_speed()
                sprite.actual_speed *= -1
                
    def __collision_ver(self, sprite, circ, direction):

        tile_y0 = sprite.rect.y / circ.get_tile_height()
        tile_y1 = (sprite.rect.y + sprite.rect.h) / circ.get_tile_height()
        
        if direction == "left":
            tilecoordx = sprite.rect.x / circ.get_tile_width()
        else:
            tilecoordx = (sprite.rect.x + sprite.rect.w) / circ.get_tile_width()
        
        i = tile_y0
        
        while i <= tile_y1:
            if (circ.get_tile(1, tilecoordx, i).type == circuit.NOPASSABLE) or \
            (circ.get_tile(0, tilecoordx, i).type == circuit.NOPASSABLE):
                tilecoordx *= circ.get_tile_width()
                
                rect = pygame.Rect((tilecoordx, i * circ.get_tile_height(), \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return rect
            i += 1
        
        return False
            
    def __collision_hor(self, sprite, circ, direction):

        tile_x0 = sprite.rect.x / circ.get_tile_width()
        tile_x1 = (sprite.rect.x + sprite.rect.w) / circ.get_tile_width()
        
        if direction == "up":
            tilecoordy = sprite.rect.y /circ.get_tile_height()
        else:
            tilecoordy = (sprite.rect.y + sprite.rect.h) /circ.get_tile_height()
        
        i = tile_x0
        
        while i <= tile_x1:
            if (circ.get_tile(1, i, tilecoordy).type == circuit.NOPASSABLE) or \
            (circ.get_tile(0, i, tilecoordy).type == circuit.NOPASSABLE):
                tilecoordy *= circ.get_tile_height()
                
                rect = pygame.Rect((i * circ.get_tile_width(), tilecoordy, \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return rect
            i += 1
            
        return False
