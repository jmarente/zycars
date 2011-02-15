#-*- encoding: utf-8 -*-

import pygame
import state
import collisionmanager
import playercar
import basiccar
import circuit
import checkpoint
import resource
import countdown
import pausemenu
import keyboard

from pygame.locals import *

class GameControl(state.State):
    '''
    @brief Clase encargada de controlar los aspectos básicos de una carrera, desde
    las colisiones hasta el control de las vueltas
    '''
    def __init__(self, game, path):
        '''
        @brief Constructor
        
        @param game Referencia a game
        @param path archivo xml del circuito en cuestión
        '''
        state.State.__init__(self, game)
        
        #Coche del jugador.
        #self.player = playercar.PlayerCar(self, 'cars/coche_prueba_red.xml', 300, 300, 0)
        self.player = playercar.PlayerCar(self, 'cars/coche_prueba_yellow.xml', 500, 400, 0)

        #Grupo de sprites que contentrá los coches de la IA.
        self.ia_cars = pygame.sprite.Group()
        
        #Grupo de sprites que contendrá las cajas de items. 
        self.items_box = pygame.sprite.Group()
        
        #Checkpoints que posee el circuito
        self.checkpoints = checkpoint.CheckPoints(self)
        
        #Grupo de sprite que contendrá las balas.
        self.bullets = pygame.sprite.Group()
                
        #Gestor de colisiones
        self.collision_manager = collisionmanager.CollisionManager()

        #Circuito actual que vamos a jugar.
        self.circuit = circuit.Circuit(self, path)
        
        #Rejilla
        self.grid = resource.get_image("rejilla")
        
        #Menú de pausa
        self.pause = pausemenu.PauseMenu(self.game, self, 'menu/pausemenu.xml')
        #Cuenta atras
        self.count_down = countdown.CountDown('cheesebu', 300, 0.002, 0.025, (221, 113, 5), 3)
        
        #Indicamos el estado
        self.actual_state = 'race'
        
        #Actualizamos el estado en carrera para posicionar bien la pantalla
        self.update()
        
        #Pasamos al estado de cuenta atras
        self.actual_state = 'countdown'
        
    def update(self):
        '''
        @brief Método encargado de actualizar todos los componentes del circuito
        '''
        
        #Si estamos en la cuenta atrás actualizamos la cuenta atrás
        if self.actual_state == 'countdown':
            self.count_down.update()
            #Si se ha completado cambiamos el estado del juego
            if self.count_down.complete():
                self.actual_state = 'race'

        #Si estamos en pause, actualizamos el menú de pause
        elif self.actual_state == 'pause':
            self.pause.update()
        
        #Si estamos el estado en carrera, actualizamos todos los estado de carrera
        elif self.actual_state == 'race':
            
            #Si pulsamos el espacio o escape, cambiamos al estado pause
            if keyboard.pressed(K_SPACE) or keyboard.pressed(K_ESCAPE):
                self.actual_state = 'pause'
            #Actualizamos al coche del jugador.
            self.player.update()
            
            #Actualizamos la IA.
            for ia_car in self.ia_cars:
                ia_car.update()
            
            #Actualizamos las cajas de items
            for box in self.items_box:
                box.update()
            
            #Actualizamos las balas.
            for bullet in self.bullets:
                bullet.update()
                    
            #Controlamos el scroll de la pantalla
            self.scroll_control()
            
            #Controlamos posibles colisiones
            self.check_collisions()
            
            #Controlamos todos los puntos de control    
            self.checkpoints.update(self.player)

    def draw(self, screen):
        '''
        @brief Método encargado de dibujar todos los elementos en pantalla
        
        @param screen Superficie destino
        '''
        #Siempre dibujamos todos los elementos de juego, ya que estarán de 
        #fondo aunque cambiemos de estado
        
        #Dibujamos las dos primeras capas del circuito
        self.circuit.draw(screen, 0)
        self.circuit.draw(screen, 1)
        
        #Dibujamos al jugador
        self.player.draw(screen)
        
        #Dibujamos los Puntos de control en pantalla
        self.checkpoints.draw(screen)
        
        #Dibujamos la ultima capa del circuito
        self.circuit.draw(screen, 2)
        
        #Si estamos en el estado de cuenta atras, mostramos la cuenta atrás
        if self.actual_state == 'countdown':
            self.count_down.draw(screen)
            
        #Si estamos en el estado de pause, mostramos el menú de pause
        elif self.actual_state == 'pause':
            self.pause.draw(screen)
            
        #Dibujamos rejilla de referencia
        #screen.blit(self.grid, (0, 0))
        
    def check_collisions(self):
        '''
        @brief Método encargada de gestionar las distintas colisiones, de los 
        elemento del juego, entre ellos y el escenario
        '''
        #colisiones jugador-escenario
        self.collision_manager.level_collision(self.player, self.circuit)
        
    def scroll_control(self):
        '''
        @brief Método encargado de controlar el scroll de la pantalla según la posición del coche
        '''
        ###SCROLL HORIZONTAL###
        #Si le jugador se sale por la derecha, hacemos scroll hacia la derecha.
        #Si el centro del coche con respecto a la pantalla es mayor que el ancho de esta
        car_position_x = self.player.get_rect().centerx - self.circuit.get_x()
        if car_position_x > (self.game.get_screen_width()/2):
            #Calculamos el movimiento de la pantalla que tenemos que hacer.
            scroll_right_x = self.player.get_rect().centerx - (self.game.get_screen_width()/2)
            #Si la nueva posicion no se sale del circuito
            if (scroll_right_x + self.game.get_screen_width()) < self.circuit.get_real_width():
                #movemos el mapa
                self.circuit.move(scroll_right_x, self.circuit.get_y());
                
        #Si el jugador se sale por la izquierda, hacemos scroll hacia la izquierda
        #Si el centro del coche con respecto a la pantalla es menor que el ancho de esta
        elif car_position_x < (self.game.get_screen_width()/2):
            scroll_left_x = self.player.get_rect().centerx - (self.game.get_screen_width()/2)
            if scroll_left_x > 0:
                self.circuit.move(scroll_left_x, self.circuit.get_y())

        ###SCROLL VERTICAL###
        #Obtenemos la posicion y del centro del coche con respecto a la pantalla
        car_position_y  = self.player.get_rect().centery - self.circuit.get_y()
        
        #Si el centro y del coche es mayor que el alto de la mita de la pantalla
        if car_position_y > (self.game.get_screen_height()/2):
            #Calculamos la nueva posicion y del circuito
            scroll_down_y = self.player.get_rect().centery - (self.game.get_screen_height()/2)
            #Si la posicion se encuentra dentro de los limites
            if (scroll_down_y + self.game.get_screen_height()) < self.circuit.get_real_height():
                #Hacemos scroll
                self.circuit.move(self.circuit.get_x(), scroll_down_y)
                
        #Si el centro y del coche es mayor que el alto de la mita de la pantalla
        elif car_position_y < (self.game.get_screen_height()/2):
            #Calculamos la nueva posicion y del circuito
            scroll_down_y = self.player.get_rect().centery - (self.game.get_screen_height()/2)
            #Si la posicion se encuentra dentro de los limites
            if scroll_down_y > 0:
                #Hacemos scroll
                self.circuit.move(self.circuit.get_x(), scroll_down_y)
        
    def add_bullet(self, bullet):
        '''
        @brief Método que añade una nueva bala al grupo de balas
        
        @param bullet Bala a añadir
        '''
        self.bullets.add(bullet)
        
    def add_ia_car(self, ia_car):
        '''
        @brief Método que añade un nuevo coche controlado por la IA al grupo
        
        @param ia_car Nuevo coche
        '''
        self.ia_car.add(ia_car)
        
    def add_item_box(self, item_box):
        '''
        @brief Método que añade una nueva caja de items al grupo
        
        @param item_box Caja a añadir
        '''
        self.items_box.add(item_box)
        
    def add_player(self, player):
        '''
        @Método que define quien es el jugador principal
        
        @param player Jugador
        '''
        self.player = player
        
    def add_checkpoint(self, checkpoint):
        '''
        @brief Método que añade un nuevo punto de control al circuito
        
        @param checkpoint Nuevo punto de control a añadir
        '''
        self.checkpoints.add_checkpoint(checkpoint)

    def set_goal(self, goal):
        '''
        @brief Método que asigna la meta del circuito
        
        @param goal Meta a asignar
        '''
        self.checkpoints.set_goal(goal)
    
    def circuit_x(self):
        '''
        @brief Método que devuelve la x actual del circuito
        
        @return posicion x del circuito
        '''
        if self.circuit:
            return self.circuit.get_x()
        else:
            return 0
            
    def circuit_y(self):
        '''
        @brief Método que devuelve la y actual del circuito
        
        @return posicion y del circuito
        '''
        if self.circuit:
            return self.circuit.get_y()
        else:
            return 0
    
    def set_state(self, new_state):
        '''
        @brief Función que cambia el estado actual de juego
        
        @param new_state Nuevo estado para el juego
        '''
        self.actual_state = new_state
            
    def horizontal_speed(self):
        '''Sin uso'''
        angle = self.player.get_angle()
        cien = 90.0
        
        if angle > 0 and angle <= 90:
            new_angle = 1 - (angle / cien)
            return (self.player.get_speed() * new_angle)
        elif angle > 90 and angle <= 180:
            angle -= 90
            return (self.player.get_speed() * (angle / cien))
        elif angle > 180 and angle <= 270:
            angle -= 180
            new_angle = 1 - (angle / cien)
            return (self.player.get_speed() * new_angle)
        elif angle > 270 and angle <= 360:
            angle -=270
            return (self.player.get_speed() * (angle / cien))
        elif angle == 360 or angle == 0:
            return self.player.get_speed()

