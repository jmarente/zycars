#-*- encoding: utf-8 -*-

import pygame
import state
import collisionmanager
import playercar
import gameobject
import basiccar
import circuit
import checkpoint
import resource
import countdown
import pausemenu
import keyboard
import start
import timer
import math

from pygame.locals import *

class GameControl(state.State):
    '''
    @brief Clase encargada de controlar los aspectos básicos de una carrera, desde
    las colisiones hasta el control de las vueltas
    '''
    def __init__(self, game, path, laps = 3):
        '''
        @brief Constructor
        
        @param game Referencia a game
        @param path archivo xml del circuito en cuestión
        '''
        state.State.__init__(self, game)
        
        #Coche del jugador.
        #self.player = playercar.PlayerCar(self, 'cars/coche_prueba_yellow.xml', 0, 0, 0)
        #self.player = playercar.PlayerCar(self, 'cars/coche_prueba_yellow.xml', 500, 400, 0)

        #Grupo de sprites que contentrá los coches de la IA.
        self.ia_cars = pygame.sprite.Group()
        
        #Grupo de sprites que contendrá las cajas de items. 
        #self.items_box = pygame.sprite.Group()
        self.items_box = pygame.sprite.Group()
        
        #Checkpoints que posee el circuito
        self.checkpoints = checkpoint.CheckPoints(self)
        
        self.ia_checks = {}
        
        #Grupo de sprite que contendrá las balas.
        self.bullets = pygame.sprite.Group()
        
        #Grupo de sprite que contendrás las manchas de aceite
        self.oils = pygame.sprite.Group()
        
        #Grupo para las pelotas
        self.balls = pygame.sprite.Group()
                
        #Gestor de colisiones
        self.collision_manager = collisionmanager.CollisionManager()
                
        #Linea de salida
        self.start = None
        
        #Vueltas al circuito
        self.max_laps = laps
        self.actual_laps = 0
        
        #Contador de vueltas
        self.font = resource.get_font('cheesebu', 30)
        self.laps_counter = None
        self.laps_counter_rect = None
        self.update_laps_counter()
        
        #Cronómetros de carrera
        self.actual_time = timer.Timer('cheesebu', 30, (0, 0, 0), 700, 10, "Actual:")
        self.best_time = timer.Timer('cheesebu', 30, (0, 0, 0), 700, 80, "Mejor:")
        self.best_time.set_minutes(10)
        self.total_time = timer.Timer('cheesebu', 30, (0, 0, 0), 700, 150, "Total:")
                
        #Circuito actual que vamos a jugar.
        self.circuit = circuit.Circuit(self, path)
        
        #Rejilla
        self.grid = resource.get_image("rejilla")
        
        #Menú de pausa
        self.pause = pausemenu.PauseMenu(self.game, self, 'menu/pausemenu.xml')
        
        #Cuenta atras
        self.count_down = countdown.CountDown('cheesebu', 300, 0.02, 0.05, (221, 113, 5), 0)
        
        #Pasamos al estado de cuenta atras
        self.actual_state = 'countdown'
        
        #Actualizamos el estado en carrera para posicionar bien la pantalla
        #self.update()
        
        self.player.update()
        
        for ia_car in self.ia_cars:
            ia_car.update(self.player.rect.x, self.player.rect.y)
            ia_car.set_points(self.ia_checks)
            
        self.scroll_control()
        
        
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
                self.actual_time.start()
                self.total_time.start()

        #Si estamos en pause, actualizamos el menú de pause
        elif self.actual_state == 'pause':
            self.pause.update()
        
        #Si estamos el estado en carrera, actualizamos todos los estado de carrera
        elif self.actual_state == 'race':
                        
            #Actualizamos el tiempo actual
            self.actual_time.update()
            self.total_time.update()
            
            #Actualizamos al coche del jugador.
            self.player.update()
            
            #Actualizamos la IA.
            for ia_car in self.ia_cars:
                ia_car.update(self.player.rect.x, self.player.rect.y)
            
            #Actualizamos las cajas de items
            for box in self.items_box:
                if self.on_screen(box):
                    box.update()
            
            for ball in self.balls:
                ball.update()
                        
            #Actualizamos las balas.
            for bullet in self.bullets:
                bullet.update()

            #Actualizamos las balas.
            for oil in self.oils:
                oil.update()
                    
            #Controlamos el scroll de la pantalla
            self.scroll_control()
            
            #Controlamos posibles colisiones
            self.check_collisions()
            
            #Controlamos todos los puntos de control    
            self.checkpoints.update(self.player)

            #Si pulsamos el espacio o escape, cambiamos al estado pause
            if keyboard.pressed(K_ESCAPE) or keyboard.pressed(K_p) \
                or not pygame.key.get_focused():
                    
                self.actual_state = 'pause'
                self.actual_time.pause()
                self.player.set_state(gameobject.NOACTION)
            
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
        
        #Dibujamos linea de meta
        self.start.draw(screen)
            
        #Dibujamos los Puntos de control en pantalla
        self.checkpoints.draw(screen)
        
        #Dibujamos todas las manchas de aceite
        for oil in self.oils:
            if self.on_screen(oil):
                oil.draw(screen)
            
        #Dibujamos todas las cajas de items
        for box in self.items_box:
            if self.on_screen(box):
                box.draw(screen)
            
        #Dibujamos al jugador
        self.player.draw(screen)

        for bullet in self.bullets:
            #if bullet.get_state() != gameobject.NORMAL and self.on_screen(bullet):
            if self.on_screen(bullet):
                bullet.draw(screen)

        for ball in self.balls:
            if self.on_screen(ball):
                ball.draw(screen)
        
        for ia_car in self.ia_cars:
            ia_car.draw(screen)
        
        self.player.draw_hud(screen)
        
        #Dibujamos la ultima capa del circuito
        self.circuit.draw(screen, 2)
        
        #Mostramos los dos cronómetros
        self.actual_time.draw(screen)
        self.best_time.draw(screen)
        self.total_time.draw(screen)
        
        #Mostramos el marcador de vueltas
        screen.blit(self.laps_counter, (self.laps_counter_rect))

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
        #Colisiones jugador-escenario
        self.collision_manager.level_collision(self.player, self.circuit)
        
        #Colisiones con las cajas de items
        for box in self.items_box:
            if self.on_screen(box) and box.get_state() != gameobject.EXPLOSION and \
                self.collision_manager.actor_pixelperfectcollision(self.player, box):
                box.set_state(gameobject.EXPLOSION)
                self.player.collected_item()
        
        #Colisiones de los misiles
        for bullet in self.bullets:
            if self.collision_manager.item_level_collision(bullet, self.circuit):
                bullet.set_state(gameobject.EXPLOSION)
            if bullet.get_state() == gameobject.RUN and \
                self.collision_manager.actor_pixelperfectcollision(self.player, bullet):
                bullet.set_state(gameobject.EXPLOSION)
                self.player.set_state(gameobject.DAMAGED)
            for ball in self.balls:
                if self.collision_manager.actor_pixelperfectcollision(ball, bullet):
                    bullet.set_state(gameobject.EXPLOSION)
                    ball.set_state(gameobject.EXPLOSION)
        
        #Colisiones de las bolas
        for ball in self.balls:
            if self.collision_manager.item_level_collision(ball, self.circuit):
                pass
            if ball.get_state() == gameobject.RUN and \
                self.collision_manager.actor_pixelperfectcollision(self.player, ball):
                ball.set_state(gameobject.EXPLOSION)
                self.player.set_state(gameobject.DAMAGED)
            self.collision_manager.control_limits(ball, self.circuit)
        
        #Colisiones con las manchas de aceite
        for oil in self.oils:
            if self.on_screen(oil) and oil.get_state() != gameobject.NORMAL \
                and self.player.get_old_state() != gameobject.DAMAGED \
                and self.collision_manager.actor_pixelperfectcollision(oil, self.player):
                self.player.set_state(gameobject.DAMAGED)
        
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
    
    def add_oil(self, oil):
        self.oils.add(oil)
    
    def add_ball(self, ball):
        self.balls.add(ball)
        
    def add_ia_car(self, ia_car):
        '''
        @brief Método que añade un nuevo coche controlado por la IA al grupo
        
        @param ia_car Nuevo coche
        '''
        self.ia_cars.add(ia_car)
        
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

    def add_checkpoint(self, checkpoint, position):
        '''
        @brief Método que añade un nuevo punto de control al circuito
        
        @param checkpoint Nuevo punto de control a añadir
        '''
        self.checkpoints.add_checkpoint(checkpoint, position)
    
    def order_checkpoints(self):
        self.checkpoints.order_checkpoints()

    def set_goal(self, goal):
        '''
        @brief Método que asigna la meta del circuito
        
        @param goal Meta a asignar
        '''
        self.checkpoints.set_goal(goal)
    
    def set_start(self, circuit, x, y, image_code, orientation, car_angle):
        '''
        @brief Método que situa la linea de salida y los coches en meta
        
        @param x Posición x
        @param y Posición y
        @param image_code Código de la imagen
        @param orientation Orientación de la linea de salida
        @param circuit_width Ancho del circuito
        @param car_angle Angulo de los coches
        '''
        self.start = start.Start(self, circuit, x, y, image_code, orientation, car_angle)
    
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
        if self.actual_state == 'pause' and new_state == 'race':
            self.actual_time.start()
            
        self.actual_state = new_state
    
    def get_state(self):
        return self.actual_state
    
    def lap_complete(self):
        '''
        @brief Método que es llamado cuando el jugador  ha dado una vuelta al circuito
        '''
        #Aumentamos el número de vueltas dadas
        self.actual_laps += 1
        self.update_laps_counter()
        
        #Comprobamos si el tiempo ha mejorado
        if self.actual_time.less_than(self.best_time):
            
            self.best_time.assign(self.actual_time)
        
        #Reiniciamos el cronometro principal
        self.actual_time.stop()
        self.actual_time.start()
        
        if self.actual_laps == self.max_laps:
            print "Terminado carrera"
    
    def update_laps_counter(self):
        '''
        @brief Método que se llama para actualizar el contador visible de las vueltas
        '''
        #Obtenemos la cadena
        laps = 'Vuelta ' + str(self.actual_laps) + '/' + str(self.max_laps)
        
        #Renderizamos
        self.laps_counter = self.font.render(laps, True, (0, 0, 0))
        
        #Indicamos la posicion
        self.laps_counter_rect = self.laps_counter.get_rect()
        #self.laps_counter_rect.centerx = pygame.display.get_surface().get_width() / 2
        self.laps_counter_rect.x = 50
        self.laps_counter_rect.y = 10
    
    def on_screen(self, element):
        '''
        @brief Método que comprueba si un elemento del juego se encuentra en pantalla
        
        @param element Elemento a comprobar si se encuentra en pantalla o no
        
        @return True si está en pantalla, False en caso contrario
        '''
        #Obtenemos las distintas variables necesarias
        x = element.get_rect().x
        y = element.get_rect().y
        w = element.get_rect().w
        h = element.get_rect().h
        circuit_x = self.circuit_x()
        circuit_y = self.circuit_y()
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        
        #Realizamos la comprobación
        if x + w > circuit_x and y + h > circuit_y and \
            x < circuit_x + screen_width and y < circuit_y + screen_height:
            return True
        
        return False

    def current_tile(self, rect):
        '''
        @brief Calcula el tile actual que se encuentra el sprite.
        
        @param sprite Sprite del que deseamos averiguar en que tile se encuentra
        '''
        
        x = int(math.floor(rect.x / self.circuit.get_tile_width()))
        y = int(math.floor(rect.y / self.circuit.get_tile_height()))
        
        return (x, y)
        
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
    
        

