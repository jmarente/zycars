#-*- encoding: utf-8 -*-

import pygame
import state
import collisionmanager
import playercar
import basiccar
import circuit


from pygame.locals import *

class GameControl(state.State):
    def __init__(self, game, path):
        state.State.__init__(self, game)
        
        #Coche del jugador.
        self.player = playercar.PlayerCar(self, 'coche_prueba.xml', 250, 300, 0)
        
        #Circuito actual que vamos a jugar.
        self.circuit = circuit.Circuit(self, path)
        
        #Grupo de sprites que contentrá los coches de la IA.
        self.ia_cars = pygame.sprite.Group()
        #Grupo de sprites que contendrá las cajas de items. 
        self.items_box = pygame.sprite.Group()
        #Grupo de sprite que contendrá las balas.
        self.bullets = pygame.sprite.Group()
        
        #Gestor de colisiones
        self.collision_manager = collisionmanager.CollisionManager()
        
    def update(self):
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
        
        ###Controlamos el scroll del jugador.###
        print self.player.get_rect()
        ###SCROLL HORIZONTAL###
        #Si le jugador se sale por la derecha, hacemos scroll hacia la derecha.
        if((self.player.get_x() - self.circuit.get_x()) + self.player.get_rect().w) >= (self.game.get_screen_width()/2):
            scroll_right_x = self.circuit.get_x() + self.player.get_speed()
            if (scroll_right_x + self.game.get_screen_width()) < self.circuit.get_real_width():
                self.circuit.move(scroll_right_x, self.circuit.get_y());
                
        #Si el jugador se sale por la izquierda, hacemos scroll hacia la izquierda
        elif (self.player.get_x() - self.circuit.get_x()) <= (self.game.get_screen_width()/2):
            scroll_left_x = self.circuit.get_x() - self.player.get_speed()
            if scroll_left_x > 0:
                self.circuit.move(scroll_left_x, self.circuit.get_y())
        
        ###SCROLL VERTICAL###
        '''if((self.player.get_y() - self.circuit.get_y()) + self.player.get_rect().h) > (self.game.get_screen_height()/2):
            scroll_down_y = self.circuit.get_y() + self.player.get_speed()
            if (scroll_down_y + self.game.get_screen_height()) < self.circuit.get_real_height():
                self.circuit.move(self.circuit.get_x(), scroll_down_y)
       
        elif(self.player.get_y() - self.circuit.get_y()) < (self.game.get_screen_height()/2):
            scroll_down_y = self.circuit.get_x() - self.player.get_speed()
            if scroll_down_y > 0:
                self.circuit.move(self.circuit.get_x(), scroll_down_y)'''
        self.check_collisions()



    def draw(self, screen):
        self.circuit.draw(screen, 0)
        self.circuit.draw(screen, 1)
        self.player.draw(screen)
        self.circuit.draw(screen, 2)
        
    def check_collisions(self):
        
        #colisiones jugador-escenario
        self.collision_manager.level_collision(self.player, self.circuit)
        
    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        
    def add_ia_car(self, ia_car):
        self.ia_car.add(ia_car)
        
    def add_item_box(self, item_box):
        self.items_box.add(item_box)
        
    def add_player(self, player):
        self.player = player
    
    def circuit_x(self):
        if self.circuit:
            return self.circuit.get_x()
        else:
            return 0
            
    def circuit_y(self):
        if self.circuit:
            return self.circuit.get_y()
        else:
            return 0
