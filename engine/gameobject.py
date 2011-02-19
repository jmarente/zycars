# -*- encoding: utf-8 -*-
 
import pygame
import animation
import resource
#import gamecontrol
import xml.dom.minidom

#Distinos estado que pueden tener los objetos del juego.
NORMAL, NOACTION, RUN, FORWARD, REVERSE, DAMAGED, ERASE, YAW, EXPLOSION = range(9)

class GameObject(pygame.sprite.Sprite):
    '''
    Clase "virtual pura" que abstrae las características básicas de los 
    objetos y actores que intervienen en el juego
    '''
    def __init__(self, game_control):
        '''
        Obtiene como parametro la referencia a GameControl al que pertenece
        el objeto.
        Define las principales variables.
        '''
        pygame.sprite.Sprite.__init__(self)
        self.game_control = game_control
        self.image = None
        self.rect = None
        self.mask = None
        self.original_sprite = None
        self.state = self.previous_state = self.old_state = NORMAL
        self.animations = {}
        self.dx = self.dy = self.x = self.y = self.old_x = self.old_y = None
        self.right_direction = self.left_direction = self.up_direction = self.down_direction = False
        
    def parser_basic_info(self, parse):
        '''
        Parsea la informacián básica que tendran todos los objetos del juego.
        '''
        parent_node = parse.firstChild
        sprite_name = str(parent_node.getAttribute('sprite_code'))
        self.original_sprite = resource.get_sprite(sprite_name)
        
        for element in parse.getElementsByTagName('animation'):
            animation_name = str(element.getAttribute('name'))
            animation_frames = str(element.getAttribute('frames'))
            animation_delay = int(element.getAttribute('delay'))
            
            if animation_name == 'normal':
                self.animations[NORMAL] = animation.Animation(animation_frames, animation_delay)
            elif animation_name == 'noaction':
                self.animations[NOACTION] = animation.Animation(animation_frames, animation_delay)
            elif animation_name == 'run':
                self.animations[RUN] = animation.Animation(animation_frames, animation_delay)
            elif animation_name == 'forward':
                self.animations[FORWARD] = animation.Animation(animation_frames, animation_delay)
            elif animation_name == 'reverse':
                self.animations[REVERSE] = animation.Animation(animation_frames, animation_delay)
            elif animation_name == 'damaged':
                self.animations[DAMAGED] = animation.Animation(animation_frames, animation_delay)
            elif animation_name == 'erase':
                self.animations[ERASE] = animation.Animation(animation_frames, animation_delay)
            elif animation_name == 'yaw':
                self.animations[YAW] = animation.Animation(animation_frames, animation_delay)
                
            self.image = self.original_sprite[self.animations[NORMAL].get_frame()]
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
                
    def update(self):
        '''
        Función que debe ser implementada por cualquier objeto de juego descendiente.
        '''
        raise NotImplemented("La funcion update de GameObject debe ser implementada por sus descendientes")
    
    def update_direction(self):
        
        if self.old_x < self.x:
            self.right_direction = True
            self.left_direction = False
        elif self.old_x > self.x:
            self.right_direction = False
            self.left_direction = True
        '''else:
            self.right_direction = False
            self.left_direction = False'''
            
        self.old_x = self.x
        
        if self.old_y < self.y:
            self.down_direction = True
            self.up_direction = False
        elif self.old_y > self.y:
            self.down_direction = False
            self.up_direction = True
        '''else:
            self.down_direction = False
            self.up_direction = False'''
            
        self.old_y = self.y
    
    def draw(self, screen):
        '''
        Dibuja al objeto sobre la superficie dada.
        '''
        screen.blit(self.image, (self.rect.x - self.game_control.circuit_x(), self.rect.y - self.game_control.circuit_y()))
        #pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - self.game_control.circuit_x(), self.rect.y - self.game_control.circuit_y(), self.rect.w, self.rect.h), 1)
        
    def get_rect(self):
        '''
        Devuelve el rectangulo con las dimensiones de la imagen actual.
        '''
        return self.rect
    def get_mask(self):
        '''
        Devuelve la mascara de la imagen actual.
        '''
        return self.mask   
    def get_state(self):
        '''
        Devuelve el estado actual del objeto.
        '''
        return self.state
    def set_state(self, new_state):
        '''
        Establece un nuevo estado para el objeto.
        '''
        self.state = new_state
    
    def get_x(self):
        return self.rect.x
        
    def get_y(self):
        return self.rect.y
        
    def get_width(self):
        return self.rect.w
        
    def get_height(self):
        return self.rect.h
    
    def go_right(self):
        return self.right_direction
    
    def go_left(self):
        return self.left_direction
    
    def go_up(self):
        return self.up_direction
    
    def go_down(self):
        return self.down_direction
    
    def get_old_state(self):
        return self.old_state
    

