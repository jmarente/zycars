#-*- encoding: utf-8 -*-

import pygame
import circuit
import basiccar
import gameobject
import pixelperfect
import item

from log import Log

class CollisionManager:
    '''
    @brief Clase encargada de comprobar si se a producido algun tipo de colision,
    tanto entre objetos, como objetos con los elemento del circuito.
    '''
    def __init__(self):
        '''
        @brief Constructor
        '''
        pass
        
    def actor_perfectcollision(self, sprite1, sprite2):
        '''
        @brief Comprueba la colision pixel por pixel enter dos sprites.
        
        @param sprite1 Sprite a comprobar
        @param sprite2 Sprite a comprobar
        
        @return True si existe colisión, False en caso contrario
        '''
        return self.actor_rectanglecollision(sprite1, sprite2) \
                and pygame.sprite.collide_mask(sprite1, sprite2)

    def actor_pixelperfectcollision(self, sprite1, sprite2):
        '''
        @brief Comprueba la colision pixel por pixel enter dos sprites.
        
        @param sprite1 Sprite a comprobar
        @param sprite2 Sprite a comprobar
        
        @return True si existe colisión, False en caso contrario
        '''
        return self.actor_rectanglecollision(sprite1, sprite2) \
                and pixelperfect.check_collision(sprite1, sprite2)
        
    def actor_rectanglecollision(self, sprite1, sprite2):
        '''
        @brief Comprueba la colision de los rectangulos de los sprites
        
        @param sprite1 Sprite a comprobar
        @param sprite2 Sprite a comprobar
        
        @return True si existe colisión, False en caso contrario
        '''
        return pygame.sprite.collide_rect(sprite1, sprite2)
        
    def actor_edgecollision(self, sprite1, sprite2):
        '''
        @brief  Devuelve un diccionario indicando por que lados han colisionado los sprites.
       
        @param sprite1 Sprite a comprobar
        @param sprite2 Sprite a comprobar
        
        @return Diccionario indicando por que lados han colisionado los sprites.
        '''
        
        #Obtenemos los rectagulos de cada uno de los sprites
        rect1 = sprite1.get_rect()
        rect2 = sprite2.get_rect()
        
        #Inicializmaos el diccionario
        edge = {"left": False, "right": False, "top": False, "bottom": False}
        
        if self.actor_perfectcollision(sprite1, sprite2):
            
            #Comprobamos por que lados colisiona
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
        '''
        @brief Función que comprueba si un sprite colisiona con un rectangulo y 
        devuelve por que lados se produce la colisión.
        
        @param sprite Sprite a comprobar
        @param tile_rect Rectangulo a comprobar
        
        @return Diccionario indicando por que lados han colisionado los sprites.
        '''
        #Obtenemos el rectangulo del sprite
        sprite_rect = sprite.get_rect()
        
        #Inicializamos el diccionario
        edge = {"left": False, "right": False, "top": False, "bottom": False}
        #Log().debug('Coche: (' + str(sprite_rect.x) + ', ' + str(sprite_rect.y) + ', ' + str(sprite_rect.w) + ', ' + str(sprite_rect.h) + ')')
        #Log().debug('Tile: (' + str(tile_rect.x) + ', ' + str(tile_rect.y) + ', ' + str(tile_rect.w) + ', ' + str(tile_rect.h) + ')')

        if sprite_rect.colliderect(tile_rect):
        
            #Vemos por que lados se produce la colisión
            if (sprite_rect.left - tile_rect.left) > 0:
                edge["right"] = True
                #Log().debug("Collision por la derecha")

            if (sprite_rect.left - tile_rect.left) < 0:
                edge["left"] = True
                #Log().debug("Collision por la izquierda")

            if (sprite_rect.top - tile_rect.top) > 0:
                edge["bottom"] = True
                #Log().debug("Collision por abajo")

            if (sprite_rect.top - tile_rect.top) < 0:
                edge["top"] = True
                #Log().debug("Collision por arriba")
                
        return edge
        
    def tile_collision():
        pass
        
    def level_collision(self, sprite, circ):
        '''
        @brief Comprueba la colision de un sprite con los elementos del circuito,
        si se produce alguna colisión, se corrige la posicion del objeto.
        
        @param sprite Sprite a comprobar
        @param circ Circuito a comprobar
        '''
        #Comprobamos el eje X.
        x_collision = False
        y_collision = False
        result = None
        tile_pos = None
        tile_rect = None

        #Colisiones verticales, con el eje x
        if sprite.go_left():
            result = self.__collision_ver(sprite, circ, "left")
            
        elif not result and sprite.go_right():
            result = self.__collision_ver(sprite, circ, "right")
            
        #Colision horizontales, con el eje y
        elif not result and sprite.go_up():
            result = self.__collision_hor(sprite, circ, "up")
            
        elif not result and sprite.go_down():
            result = self.__collision_hor(sprite, circ, "down")
            
        #Si hemos obtenido algún resultado y es de tipo colisionable
        if result and result['type'] == circuit.NOPASSABLE:
            
            tile_rect = result['rect']
            #Vemos por que lados colisiona
            edge = self.actor_tile_edgecollision(sprite, tile_rect)
    
            collision = self.side_collision(sprite, tile_rect, edge)
            #Según la colisión corregiremos de una forma u otra el rectangulo del sprite   
            col = False
            
            if sprite.get_state() == gameobject.DAMAGED:
                sprite.set_state(gameobject.NOACTION)
                sprite.start = None
                
            if sprite.dx < 0:         
                if collision['right']:
                    #sprite.rect.x = tile_rect.x + tile_rect.w
                    sprite.x = tile_rect.x + tile_rect.w + (sprite.rect.w / 2)
                    sprite.actual_speed *= -1
                    col = True
            else:
                if collision['left'] and not col:
                    #sprite.rect.x = tile_rect.x - sprite.rect.w
                    sprite.x = tile_rect.x - (sprite.rect.w / 2)
                    sprite.actual_speed *= -1
                    col = True
                    
            if sprite.dy < 0:
                if collision['bottom'] and not col:
                    sprite.y = tile_rect.y + tile_rect.w + (sprite.rect.h / 2)
                    sprite.actual_speed *= -1
                    col = True
                    #sprite.rect.y = tile_rect.y + tile_rect.h
            else:
                if collision['top'] and not col:
                    sprite.y = tile_rect.y - (sprite.rect.h / 2)
                    sprite.actual_speed *= -1
                    col = True
                    #sprite.rect.y = tile_rect.y - sprite.rect.h
                
        #Si hemos obtenido colisión y es de tipo lag
        elif result and (result['type'] == circuit.LAG or result['type'] == circuit.HOLE):
            
            #Si el coche va mas rapido que la mitad de su velocidad maxima
            if(abs(sprite.actual_speed) > (abs(sprite.get_max_speed()) / 2)):
                
                #Reducimos su velocidad a la mitad de su máximo
                if sprite.actual_speed > 0:
                    sprite.actual_speed = abs(sprite.get_max_speed()) / 2
                else:
                    sprite.actual_speed = -1 * (abs(sprite.get_max_speed()) / 2)
        
        '''elif result and result['type'] == circuit.HOLE and sprite.get_state() != gameobject.FALL and sprite.old_state != gameobject.FALL:
            sprite.set_state(gameobject.FALL)'''
    
    def item_level_collision(self, it, circ):
        '''
        @brief Función encargada de gestionar la colisión de los items con el escenario
        
        @param it Item a comprobar
        @param circ Circuito en el que se encuentra el item
        '''
        result = None

        #Colisiones verticales, con el eje x
        if it.go_left():
            result = self.__collision_ver(it, circ, "left")
            
        elif not result and it.go_right():
            result = self.__collision_ver(it, circ, "right")
            
        #Colision horizontales, con el eje y
        elif not result and it.go_up():
            result = self.__collision_hor(it, circ, "up")
            
        elif not result and it.go_down():
            result = self.__collision_hor(it, circ, "down")
        
        #Si existe algun tipo de colision, el tile no es transpasable
        #Y el item es de tipo misil devolvemos true
        if result and result['type'] == circuit.NOPASSABLE and it.type == item.MISSILE:
            return True

        #Si existe algun tipo de colision, el tile no es transpasable
        #Y el item es de tipo bola, gestionamos el rebote
        elif result and result['type'] == circuit.NOPASSABLE and it.type == item.BALL:
            
            tile_rect = result['rect']
            
            #Obtenemos los lados por los que habria que corregir el rebote
            edge = self.actor_tile_edgecollision(it, tile_rect)
            collision = self.side_collision(it, tile_rect, edge)
                        
            col = False
            if it.dx > 0:
                if collision['left']:
                    it.x = tile_rect.x - (it.rect.w / 2)
                    if it.go_down():
                        it.actual_angle += 70
                    elif it.go_up():
                        it.actual_angle -= 70
                    col = True
            else:
                if collision['right'] and not col:
                    it.x = tile_rect.x + tile_rect.w + (it.rect.w / 2)
                    if it.go_down():
                        it.actual_angle -= 70
                    elif it.go_up():
                        it.actual_angle += 70
                    col = True
            if it.dy > 0:
                if collision['top'] and not col:
                    it.y = tile_rect.y - (it.rect.h / 2)
                    if it.go_left():
                        it.actual_angle += 70
                    elif it.go_right():
                        it.actual_angle -= 70
                    col = True
            else:
                if collision['bottom'] and not col:
                    it.y = tile_rect.y + tile_rect.w + (it.rect.h / 2)
                    if it.go_left():
                        it.actual_angle -= 70
                    elif it.go_right():
                        it.actual_angle += 70
                    col = True
                    
            return True
        
        #Si no se cumple nada de lo anterior devolvemos false
        return False
                
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
                
                result = {}
                result['type'] = circuit.NOPASSABLE
                result['rect'] = pygame.Rect((tilecoordx, i * circ.get_tile_height(), \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result
                
            i += 1
            
        i = tile_y0
        
        while i <=tile_y1:
            if (circ.get_tile(1, tilecoordx, i).type == circuit.LAG) or \
            (circ.get_tile(0, tilecoordx, i).type == circuit.LAG):
                tilecoordx *= circ.get_tile_width()
                
                result = {}
                result['type'] = circuit.LAG
                result['rect'] = pygame.Rect((tilecoordx, i * circ.get_tile_height(), \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result

            elif (circ.get_tile(1, tilecoordx, i).type == circuit.HOLE) or \
            (circ.get_tile(0, tilecoordx, i).type == circuit.HOLE):
                tilecoordx *= circ.get_tile_width()

                result = {}
                result['type'] = circuit.HOLE
                result['rect'] = pygame.Rect((tilecoordx, i * circ.get_tile_height(), \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result
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
                
                result = {}
                result['type'] = circuit.NOPASSABLE
                result['rect'] = pygame.Rect((i * circ.get_tile_width(), tilecoordy, \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result

            elif (circ.get_tile(1, i, tilecoordy).type == circuit.LAG) or \
            (circ.get_tile(0, i, tilecoordy).type == circuit.LAG):
                tilecoordy *= circ.get_tile_height()
                
                result = {}
                result['type'] = circuit.LAG
                result['rect'] = pygame.Rect((i * circ.get_tile_width(), tilecoordy, \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result

            elif (circ.get_tile(1, i, tilecoordy).type == circuit.HOLE) or \
            (circ.get_tile(0, i, tilecoordy).type == circuit.HOLE):
                tilecoordy *= circ.get_tile_height()

                result = {}
                result['type'] = circuit.HOLE
                result['rect'] = pygame.Rect((i * circ.get_tile_width(), tilecoordy, \
                circ.get_tile_width(), circ.get_tile_height()))
                
                return result
                
            i += 1
                        
        return False
    
    def side_collision(self, sprite, tile_rect, edge):
        '''
        @brief Función que determina por que lado del tile se deberia corregir 
        la posición del sprite
        
        @param sprite Objeto del juego
        @param tile_rect Rectangulo que representa el tile
        @param edge Lista con los filos por los que colisiona el sprite con el tile
        '''
        collision = {'left': False, 'right': False, 'top': False, 'bottom': False}
        
        #Comprobamos que lado debemos corregir, viendo que parte del sprite
        #Esta mas superpuesto con el tile
        if edge['left'] and edge['bottom']:
            left_car = tile_rect.left - sprite.rect.left
            bottom_car = sprite.rect.bottom - tile_rect.bottom
            
            if left_car > bottom_car:
                #Log().info('Corregiriamos colision por la izquierda')
                collision['left'] = True
            elif left_car < bottom_car:
                #Log().info('Corregiriamos colision por abajo')
                collision['bottom'] = True
                
        if edge['left'] and edge['top']:
            left_car = tile_rect.left - sprite.rect.left
            top_car = tile_rect.top - sprite.rect.top
            
            if left_car > top_car:
                #Log().info('Corregiriamos colision por la izquierda')
                collision['left'] = True
            elif left_car < top_car:
                #Log().info('Corregiriamos colision por arriba')
                collision['top'] = True
                                
        if edge['right'] and edge['bottom']:
            right_car = sprite.rect.right - tile_rect.right
            bottom_car = sprite.rect.bottom - tile_rect.bottom
            
            if right_car > bottom_car:
                #Log().info('Corregiriamos colision por la derecha')
                collision['right'] = True
            elif right_car < bottom_car:
                #Log().info('Corregiriamos colision por abajo')
                collision['bottom']  = True
            
        if edge['right'] and edge['top']:
            right_car = sprite.rect.right - tile_rect.right
            top_car = tile_rect.top - sprite.rect.top
            
            if right_car > top_car:
                #Log().info('Corregiriamos colision por la derecha')
                collision['right'] = True
            elif right_car < top_car:
                #Log().info('Corregiriamos colision por arriba')
                collision['top'] = True
        
        return collision

    def side_collision2(self, sprite, tile_rect):
        collision = {'left': False, 'right': False, 'top': False, 
                    'bottom': False, 'horizontal':False, 'vertical': False}
                    
        left = right = top = bottom = 0
        
        if sprite.rect.x < tile_rect.x and tile_rect.x < sprite.rect.right \
        and sprite.rect.right < tile_rect.right:
            left = tile_rect.x - sprite.rect.x
        
        if tile_rect.x < sprite.rect.x and sprite.rect.x < tile_rect.right \
        and tile_rect.right < sprite.rect.right:
            right = sprite.rect.right - tile_rect.right
        
        if sprite.rect.y < tile_rect.y and tile_rect.y < sprite.rect.bottom \
        and sprite.rect.bottom < tile_rect.bottom:
            top = tile_rect.y - sprite.rect.y

        if tile_rect.y < sprite.rect.y and sprite.rect.y < tile_rect.bottom \
        and tile_rect.bottom < sprite.rect.bottom:
            bottom = sprite.rect.bottom < tile_rect.bottom
            
        horizontal = left if left > right else right
        vertical = top if top > bottom else bottom
        
        if horizontal > vertical:
            collision['horizontal'] = True
            if left > right:
                collision['left'] = True  
            else: 
                collision['right'] = True
        else:
            collision['vertical'] = True
            if top > bottom:
                collision['top'] = True  
            else:
                collision['bottom'] = True
        
        return collision
    
    def control_limits(self, sprite, circ):
        '''
        @brief Función encargada de controlar que un sprite no se salga 
        de los limites del circuito, en tal caso se eliminará dicho sprite
        
        @param sprite Sprite a comprobar
        @param circ Circuito donde se encuentra el sprite
        '''
        
        #Si se sale por la izquierda, derecha, arriba o abajo, lo eliminamos
        if sprite.rect.x < circ.get_tile_width() \
            or sprite.rect.y < circ.get_tile_height() \
            or sprite.rect.y + sprite.rect.h > circ.get_real_height() - circ.get_tile_height() \
            or sprite.rect.x + sprite.rect.w > circ.get_real_width() - circ.get_tile_width():
            sprite.kill()
            Log().critical('Item fuera de limites, con angulo ' + str(sprite.actual_angle))
            if sprite.go_left():
                Log().critical('Hacia la izquierda')
            if sprite.go_right():
                Log().critical('Hacia la derecha')
            if sprite.go_up():
                Log().critical('Hacia arriba')
            if sprite.go_down():
                Log().critical('Hacia abajo')
            Log().critical('Dx: ' + str(sprite.dx))
            Log().critical('Dy: ' + str(sprite.dy))
        
                
