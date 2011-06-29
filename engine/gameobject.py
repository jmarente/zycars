# -*- encoding: utf-8 -*-
 
import pygame
import animation
import resource
import pixelperfect
#import gamecontrol
import math

#Distinos estado que pueden tener los objetos del juego.
NORMAL, NOACTION, RUN, FORWARD, REVERSE, DAMAGED, ERASE, YAW, EXPLOSION, FALL, TURBO = range(11)

class GameObject(pygame.sprite.Sprite):
    '''
    @brief Clase "virtual pura" que abstrae las características básicas de los 
    objetos y actores que intervienen en el juego
    '''
    def __init__(self, game_control):
        '''
        @brief Constructor
        
        @param game_control Referencia a GameControl
        '''
        pygame.sprite.Sprite.__init__(self)
        self.game_control = game_control
        self.image = None
        self.rect = None
        self.mask = None
        self.hitmask = None
        self.original_sprite = None
        self.actual_angle = 0
        self.rotation_angle = None

        #Distintos atributos del objeto
        self.max_speed = 0
        self.actual_speed = 0
        self.min_speed = 0
        #self.__angle_rotation = None
        self.aceleration = 0
        self.desaceleration = 0
        
        #Estado inicial es el normal
        self.state = self.previous_state = self.old_state = NORMAL
        
        #Lista de animaciones
        self.animations = {}
        
        #Posiciones del coche
        self.dx = self.dy = self.x = self.y = self.old_x = self.old_y = self.previous_x = self.previous_y = None
        
        #Dirección hacia la que va el objeto
        self.right_direction = self.left_direction = self.up_direction = self.down_direction = False
        
    def parser_basic_info(self, parse):
        '''
        @brief Método que parsea la información basica de un objeto del juego.
        
        @param parse Parse a Archivo xml con xml.dom.minidom
        '''
        parent_node = parse.firstChild
        sprite_name = str(parent_node.getAttribute('sprite_code'))
        self.original_sprite = resource.get_new_sprite(sprite_name)
        
        #Cargamos las distintas animaciones del objeto
        for element in parse.getElementsByTagName('animation'):
            animation_name = str(element.getAttribute('name'))
            animation_frames = str(element.getAttribute('frames'))
            animation_delay = int(element.getAttribute('delay'))
            
            #Vemos que tipo de animación es y lo añadimos al mapa de imagenes
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
            elif animation_name == 'fall':
                self.animations[FALL] = animation.Animation(animation_frames, animation_delay)
            elif animation_name == 'turbo':
                self.animations[TURBO] = animation.Animation(animation_frames, animation_delay)
                
        #Inicializamos la imagen, el rectangulo y la mascara de pixeles
        self.image = self.original_sprite.get_frame(self.animations[NORMAL].get_frame())
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)

                
    def update(self):
        '''
        #brief Método que actualiza lógicamente al objeto
        Debe ser implementada por los descendientes de GameObject
        '''
        raise NotImplemented("La funcion update de GameObject debe ser implementada por sus descendientes")
    
    def update_direction(self):
        '''
        @brief Método que controla hacia que dirección se dirige el coche
        '''
        if self.old_x < self.x:
            self.right_direction = True
            self.left_direction = False
        elif self.old_x > self.x:
            self.right_direction = False
            self.left_direction = True
            
        self.old_x = self.x
        
        if self.old_y < self.y:
            self.down_direction = True
            self.up_direction = False
        elif self.old_y > self.y:
            self.down_direction = False
            self.up_direction = True

            
        self.old_y = self.y
    
    def draw(self, screen):
        '''
        @brief Método encargado de dibujar el objeto sobre una superficie
        
        @param screen Superficie destino
        '''
        screen.blit(self.image, (self.rect.x - self.game_control.circuit_x(), self.rect.y - self.game_control.circuit_y()))
        #pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - self.game_control.circuit_x(), self.rect.y - self.game_control.circuit_y(), self.rect.w, self.rect.h), 1)

    def move(self, delta):
        '''
        @brief Movemos el objeto en el sentido dado 
        
        @param delta Entero +1 hacia delante, -1 hacia atras
        '''
        #Actualizamos la velocidad actual
        self.actual_speed += self.aceleration * delta
        
        #Controlamos los limites de velocidad del coche
        if self.actual_speed > self.max_speed:
            self.actual_speed = self.max_speed
        elif self.actual_speed < -self.min_speed:
            self.actual_speed = -self.min_speed
        
        if delta == 0:
            self.actual_speed = 0

    def update_position(self):
        '''
        @brief Actualiza la posición del objeto.
        '''
        self.previous_x = self.x
        self.previous_y = self.y
        self.rect.x = int(self.x) - self.rect.w / 2
        self.rect.y = int(self.y) - self.rect.h / 2
        self.x += self.dx
        self.y += self.dy

    def trigonometry(self):
        '''
        @brief Aplica la rotación del objeto segun el angulo de este
        '''
        angle = math.radians(self.actual_angle)
        self.dx = math.cos(angle) * self.actual_speed
        self.dy = math.sin(angle) * self.actual_speed

    def update_image(self):
        '''
        @bnief Actualiza la imagen, según el estado actual de la animación y el angulo del objeto
        '''
        #Rotamos la imagen actual de la animación
        self.image = pygame.transform.rotate(self.original_sprite.get_frame(self.animations[self.state].get_frame()), -self.actual_angle)
        
        #Actualizamos tanto el alto como el ancho 
        self.rect.w = self.image.get_width()
        self.rect.h = self.image.get_height()
        
        #Obtenemos la nueva mascara de pixeles
        self.mask = pygame.mask.from_surface(self.image)
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
    
    def update_angle(self):
        if self.actual_angle < 0:
            self.actual_angle += 360
        if self.actual_angle > 360:
            self.actual_angle -= 360
        
    def get_rect(self):
        '''
        @brief Método consultor
        
        @return Rectangulo con las dimensiones de la imagen actual.
        '''
        return self.rect
        
    def get_mask(self):
        '''
        @brief Método consultor
        
        @return Mascara de pixeles de la imagen actual.
        '''
        return self.mask   
        
    def get_state(self):
        '''
        @brief Método consultor
        
        @return Estado actual del objeto.
        '''
        return self.state
        
    def set_state(self, new_state):
        '''
        @brief Método que modifica el estado actual del objeto
        
        @param new_state Nuevo estado para el objeto
        '''
        self.state = new_state
    
    def get_x(self):
        '''
        @brief Método consultor
        
        @return Posición x del objeto
        '''
        return self.rect.x
        
    def get_y(self):
        '''
        @brief Método consultor
        
        @return Posición y del objeto
        '''
        return self.rect.y
        
    def get_width(self):
        '''
        @brief Método consultor
        
        @return Ancho del objeto
        '''
        return self.rect.w
        
    def get_height(self):
        '''
        @brief Método consultor
        
        @return Alto del objeto
        '''
        return self.rect.h
    
    def go_right(self):
        '''
        @brief Método consultor
        
        @return True si el objeto va hacia la derecha, Falso en caso contrario
        '''
        return self.right_direction
    
    def go_left(self):
        '''
        @brief Método consultor
        
        @return True si el objeto va hacia la izquierda, Falso en caso contrario
        '''
        return self.left_direction
    
    def go_up(self):
        '''
        @brief Método consultor
        
        @return True si el objeto va hacia arriba, Falso en caso contrario
        '''
        return self.up_direction
    
    def go_down(self):
        '''
        @brief Método consultor
        
        @return True si el objeto va hacia abajo, Falso en caso contrario
        '''
        return self.down_direction
    
    def get_old_state(self):
        '''
        @brief Método consultor
        
        @return Estado anterior al actual
        '''
        return self.previous_state

        
    def get_angle(self):
        '''
        @brief Métodod Consultor
        
        @return Ángulo actual del objetos.
        '''
        return self.actual_angle
        
    def set_angle(self, new_angle):
        '''
        @brief Método encargado de modificar el angulo del objeto.
        
        @param new_angle Nuevo ángulo para el objetos
        '''
        self.actual_angle = new_angle
    
