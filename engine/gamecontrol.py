#-*- encoding: utf-8 -*-

import pygame
import time
import state
import collisionmanager
import playercar
import gameobject
import gameanimation
import basiccar
import circuit
import checkpoint
import resource
import countdown
import pausemenu
import keyboard
import start
import timer
import astar
import math
import copy
import config

from config import *
from pygame.locals import *

class Advice:
    '''
    @brief Encargada de mostrar mesajes en pantalla durante la carrera
    '''
    def __init__(self, message, font_code, max_size, increase, centerx, centery, color, time):
        '''
        @brief Constructor.
        
        @param message Cadena de texto con el mensaje a mostrar.
        @param font_code Codigo de la fuente a usar.
        @param max_size Tamaño máximo de la fuente.
        @param increase Incermento de la superficie
        @param centerx Posición central del mensaje en x.
        @param centery Posición central del mensaje en y.
        @param color Color del mensaje.
        @param time Duración del mensaje en pantalla.
        '''
        #Asignamos los distintos valores
        self.font = resource.get_font(font_code, max_size)
        self.message = self.font.render(message, True, color)
        self.actual_surface = self.message
        self.centerx = centerx
        self.centery = centery
        self.total_time = time
        self.start_time = None
        self.scale = 0
        self.increase_scale = increase
        self.complete_advice = False
        
        #Obtenemos la superficie inicial, con el tamaño mas pequeño de la escala
        self.actual_surface = pygame.transform.rotozoom(self.message, 0, self.scale)
        self.rect = self.actual_surface.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        
    def update(self):
        '''
        @brief Actualiza el mensaje y controla su finalización.
        '''
        #Si aún no habia empezado, recogemos el tiempo actual
        if not self.start_time:
            self.start_time = time.time()
        
        #Obtenemos el tiempo discurrido
        elapsed = time.time() - self.start_time
        
        #Si aun no ha pasado el tiempo total
        if elapsed < self.total_time:
            
            #Redimensinamos la imagen
            self.actual_surface = pygame.transform.rotozoom(self.message, 0 ,self.scale)
            
            #Actualizamos la posición
            self.rect = self.actual_surface.get_rect()
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery
            
            #Aumentamos la escala
            self.scale += self.increase_scale
        
        #Si no avisamo de que el tiempo ya ha terminado
        else:
            self.complete_advice = True
            
    def draw(self, screen):
        '''
        @brief Dibuja el mensaje en pantalla
        
        @param screen Superficie destino
        '''
        screen.blit(self.actual_surface, self.rect)
    
    def complete(self):
        '''
        @brief Indica si un mensaje se ha completado
        
        @return True si ha acabado, False en caso contrario
        '''
        return self.complete_advice 

class PositionBoard():
    '''
    @brief Encargada de controlar las posiciones de los jugadores.
    '''
    def __init__(self, x, y, image_name1, image_name2):
        '''
        @brief Contrustor.
        
        @param x Posición x
        @param y Posición y
        @parama image_name1 Nombre de la primera imagen
        @parama image_name2 Nombre de la segunda imagen
        '''
        #Cargamos las imagenes
        self.image1 = resource.get_image(image_name1)
        self.image2 = resource.get_image(image_name2)
        
        #Distancia entre imagen e imagen
        self.distance = 20
        self.x = x
        self.y = y
        
        #Lista con las posiciones
        self.list_position = []
        
    def update(self, player, ia_cars):
        '''
        @brief Actualiza las posiciones de los jugadores
        
        @param player Tupla de dos elementos con la referencia al jugador principal y sus checkpoints
        @param ia_cars Lista de tuplas con la ia y sus checkpoints
        '''
        #Lista auxiliar
        aux_positions = []
        
        #Introducimos los elementos
        aux_positions.append((player[1].get_total_checked(), player[0], True)) 
        for ia_car in ia_cars:
            aux_positions.append((ia_car[1].get_total_checked(), ia_car[0], False))
        
        #Ordenamos la lista al reves
        self.list_position = sorted(aux_positions, reverse = True)
        
    def draw(self, screen):
        '''
        @brief Dibuja el marcador con las posiciones
        
        @param screen Superficie destino
        '''
        #Obtenemos el número total de jugadores a mostrar
        total = 4 if len(self.list_position) >= 4 else len(self.list_position)
        
        #Recorremos los cuatro primeros coches
        for i in range(total):
            #Dibujamos una image un otra según la iteración en la que estemos
            #Junto con su separación
            if (i + 1) % 2:
                screen.blit(self.image2, (self.x, self.y + self.image2.get_height() * i + self.distance * i))
            else:
                screen.blit(self.image1, (self.x, self.y + self.image1.get_height() * i + self.distance * i))
            
            #Calculamos la posición donde se mostrara el avatar del jugador
            rect = self.list_position[i][1].get_avatar().get_rect()
            rect.centerx = self.x + self.image2.get_width() / 2
            rect.centery = self.y + self.image2.get_height() / 2 + self.image2.get_height() * i + self.distance * i - 5
            
            #Dibujamos el avatar del jugador sobre la imagen de fondo
            screen.blit(self.list_position[i][1].get_avatar(), rect)
    
    def get_player_position(self):
        '''
        @brief Devuelve la posición del jugador principal del juego.
        
        @return Posición del jugador.
        '''
        #Devolvemos la posición del jugador
        for i in range(len(self.list_position)):
            if self.list_position[i][2]:
                return i + 1
        
        return 1
    
    def get_all_players_position(self):
        '''
        @brief Consulta la posición de los jugadores
        
        @return lista con las posiciones de los jugadores en carrera
        '''
        return self.list_position

class GameControl(state.State):
    '''
    @brief Clase encargada de controlar los aspectos básicos de una carrera, desde
    las colisiones hasta el control de las vueltas
    '''
    def __init__(self, game, game_mode, path, best_total_time, best_lap, laps = 3):
        '''
        @brief Constructor
        
        @param game Referencia a game
        @param path archivo xml del circuito en cuestión
        '''
        state.State.__init__(self, game)
        
        self.game_mode = game_mode
        #Coche del jugador.
        #self.player = playercar.PlayerCar(self, 'cars/coche_prueba_yellow.xml', 0, 0, 0)
        #self.player = playercar.PlayerCar(self, 'cars/coche_prueba_yellow.xml', 500, 400, 0)

        #Grupo de sprites que contentrá los coches de la IA.
        self.ia_cars = []
        
        #Checkpoints para la ia
        self.ia_checkpoints = [checkpoint.CheckPoints(self),checkpoint.CheckPoints(self),checkpoint.CheckPoints(self),checkpoint.CheckPoints(self)]
        
        #Grupo de sprites que contendrá las cajas de items. 
        #self.items_box = pygame.sprite.Group()
        self.items_box = pygame.sprite.Group()
        
        #Checkpoints que posee el circuito
        self.checkpoints = checkpoint.CheckPoints(self)
        
        #Puntos objetivos por los que tienen que pasar la IA
        self.ia_checks = {}
        
        #Grupo de sprite que contendrá las balas.
        self.bullets = pygame.sprite.Group()
        
        #Grupo de sprite que contendrás las manchas de aceite
        self.oils = pygame.sprite.Group()
        
        #Grupo para las pelotas
        self.balls = pygame.sprite.Group()
        
        #Grupo para las pelotas
        self.gums = pygame.sprite.Group()
        
        #Animaciones que estarán en el juego
        self.static_animations = []
        
        self.advices = []
                
        #Gestor de colisiones
        self.collision_manager = collisionmanager.CollisionManager()
                
        #Linea de salida
        self.start = None
        self.complete = False
        
        #Vueltas al circuito
        self.max_laps = laps
        self.actual_laps = 0
                
        #Fuentes que usaremos
        self.font = resource.get_font('cheesebu', 35)
        self.font2 = resource.get_font('cheesebu', 70)
        
        #Contador de vuelta
        self.laps_counter = None
        self.laps_counter_rect = None
        
        #Obtenemos una superficie negra del mismo tamaño que la pantalla
        self.fade_surface = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()))
        self.fadein = True
        self.fadeout = False
        self.fade_speed = 5
        self.fadeout_speed = 5
        self.actual_alpha = 255
        
        #Actualizamos el contador
        self.update_laps_counter()
        
        #Cronómetros de carrera
        self.actual_time = timer.Timer('cheesebu', 20, (0, 0, 0), 725, 10, "Actual:")
        self.total_time = timer.Timer('cheesebu', 20, (0, 0, 0), 725, 80, "Total:")
        
        #Mejor tiempo total del circuito
        self.best_total_time = timer.Timer('cheesebu', 20, (0, 0, 0), 600, 80,
                                        "Mejor total:", best_total_time[0],
                                        best_total_time[1],best_total_time[2])
        
        #Mejor tiempo de vuelta del circuito
        self.best_time = timer.Timer('cheesebu', 20, (0, 0, 0), 600, 10, 
                                    "Mejor Vuelta:", best_lap[0], 
                                    best_lap[1], best_lap[2])
        
        #Circuito actual que vamos a jugar.
        self.circuit = circuit.Circuit(self, path)
        
        #Menú de pausa
        self.pause = pausemenu.PauseMenu(self.game, self, 'menu/pausemenu.xml')
        
        #Cuenta atras
        self.count_down = countdown.CountDown('cheesebu', 300, 0.02, 0.05, (221, 113, 5), 0)
        
        #Marcador de las posiciones de los jugadores
        self.position_board = PositionBoard(20, 10, 'image_position1', 'image_position2')
        
        #Pasamos al estado de cuenta atras
        self.actual_state = None
        
        self.position = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th'}
        self.player_position = 1
        
        #Actualizamos al jugador y la IA para posicionar bien la pantalla
        self.player.update()
        
        aux_ia_cars = []
        
        #Actualizamos a la IA una primera vez y le situamos los puntos objetivos
        for i in range(len(self.ia_cars)):
            self.ia_cars[i].update()
            self.ia_cars[i].set_targets(self.ia_checks)
            
            #Asociamos checkpoints con la IA
            aux_ia_cars.append((self.ia_cars[i], self.ia_checkpoints[i]))
        
        self.ia_cars = aux_ia_cars
        
        #Actualizamos por primera vez el marcador de posiciones
        self.position_board.update((self.player, self.checkpoints), self.ia_cars)
        
        #Posicionamos la pantalla
        self.scroll_control()
        
    def update(self):
        '''
        @brief Método encargado de actualizar todos los componentes del circuito
        '''
        
        if self.fadein:
            self.actual_alpha -= self.fade_speed
            self.fade_surface.set_alpha(self.actual_alpha)
            
            if self.actual_alpha <= 0:
                self.fadein = False
                self.actual_state = 'countdown'
                
        else:
            #Si estamos en la cuenta atrás actualizamos la cuenta atrás
            if self.actual_state == 'countdown':
                self.count_down.update()
                for animation in self.static_animations:
                    animation.update()
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
                
                if not self.complete:
                    #Actualizamos el tiempo actual
                    self.actual_time.update()
                    self.total_time.update()
                
                #Actualizamos al coche del jugador.
                self.player.update()
                
                #Actualizamos la IA.
                for ia_car in self.ia_cars:
                    #Actualizamos el coche de la IA
                    ia_car[0].update()
                    if not self.complete:
                        #Actualizamos los puntos de control para la IA dada
                        ia_car[1].update(ia_car[0])
                
                for ball in self.balls:
                    ball.update()
                            
                #Actualizamos las balas.
                for bullet in self.bullets:
                    bullet.update()

                #Actualizamos las balas.
                for oil in self.oils:
                    oil.update()
                
                for gum in self.gums:
                    gum.update()

                for i in range(len(self.advices)):
                    self.advices[i].update()
                
                i = 0
                deleted = False
                while i < len(self.advices) and not deleted:
                    if self.advices[i].complete():
                        del self.advices[i]
                        deleted = True
                        if self.complete:
                            self.fadeout = True
                    i += 1
                        
                #Controlamos el scroll de la pantalla
                self.scroll_control()
                
                #Controlamos posibles colisiones
                self.check_collisions()
                
                if not self.complete:
                    #Controlamos todos los puntos de control    
                    self.checkpoints.update(self.player, True)

                    #Obtenemos la posicion del jugador actualizando el marcador
                    self.position_board.update((self.player, self.checkpoints), self.ia_cars)
                
                #Si pulsamos el espacio o escape, cambiamos al estado pause
                if keyboard.pressed(K_ESCAPE) or keyboard.pressed(K_p) \
                    or not pygame.key.get_focused():
                        
                    self.actual_state = 'pause'
                    self.actual_time.pause()
                    self.player.set_state(gameobject.NOACTION)
            
            if self.fadeout:
                self.actual_alpha += self.fadeout_speed
                self.fade_surface.set_alpha(self.actual_alpha)
            
                if self.actual_alpha >= 255:
                    self.fadeout = False
                    if config.Config().get_mode() == config.TIMED:
                        self.game_mode.completed_race(self.player, self.total_time, self.best_time)
                    else:
                        self.game_mode.completed_race(self.position_board.get_all_players_position())


        for animation in self.static_animations:
            animation.update()
        
        if self.actual_state != 'pause':
            #Actualizamos las cajas de items
            for box in self.items_box:
                if self.on_screen(box):
                    box.update()
            
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
        
        for gum in self.gums:
            if self.on_screen(gum):
                gum.draw(screen)
            
        #Dibujamos al jugador
        self.player.draw(screen)

        #Dibujamos los coches controlados por la IA
        for ia_car in self.ia_cars:
            ia_car[0].draw(screen)

        #Dibujamos todas las cajas de items
        for box in self.items_box:
            if self.on_screen(box):
                box.draw(screen)
        
        #Dibujamoslos misiles
        for bullet in self.bullets:
            #if bullet.get_state() != gameobject.NORMAL and self.on_screen(bullet):
            if self.on_screen(bullet):
                bullet.draw(screen)

        #Dibujamos las bolas
        for ball in self.balls:
            if self.on_screen(ball):
                ball.draw(screen)
                
        for animation in self.static_animations:
            if self.on_screen(animation):
                animation.draw(screen)
        
        #Dibujamos la ultima capa del circuito
        self.circuit.draw(screen, 2)

        #Mostramos el hud del jugador con el item actual que posee
        self.player.draw_hud(screen)
        
        #Mostramos los dos cronómetros
        self.actual_time.draw(screen)
        self.best_time.draw(screen)
        self.total_time.draw(screen)
        self.best_total_time.draw(screen)
        
        #Mostramos el marcador de vueltas
        screen.blit(self.laps_counter, (self.laps_counter_rect))
        
        #Mostramos el marcador de posiciones
        self.position_board.draw(screen)
        
        #Actualizamos la posicion del jugador
        self.player_position = self.position_board.get_player_position()
        position = self.position[self.player_position]
        position_surface = self.font2.render(str(self.player_position), True, (0,0,0))
        ordinal_surface = self.font.render(position, True, (0,0,0))
        
        #Mostramos la posición del jugador
        screen.blit(position_surface, (15, 540))
        screen.blit(ordinal_surface, (15 + position_surface.get_width(), 540))
        
        for advice in self.advices:
            advice.draw(screen)

        #Si estamos en el estado de cuenta atras, mostramos la cuenta atrás
        if self.actual_state == 'countdown':
            self.count_down.draw(screen)
            
        #Si estamos en el estado de pause, mostramos el menú de pause
        elif self.actual_state == 'pause':
            self.pause.draw(screen)
        
        if self.fadein or self.fadeout:
            screen.blit(self.fade_surface, (0, 0))
            
        #Dibujamos rejilla de referencia
        #screen.blit(self.grid, (0, 0))
        
    def check_collisions(self):
        '''
        @brief Encargado de gestionar las distintas colisiones, de los 
        elemento del juego, entre ellos y el escenario
        '''
        #Colisiones jugador-escenario
        self.collision_manager.level_collision(self.player, self.circuit)
        
        #Colisiones de la IA
        for ia_car in self.ia_cars:
            #Con el nivel
            self.collision_manager.level_collision(ia_car[0], self.circuit)
            #Con el jugador
            self.collision_manager.actor_actor_collision(self.player, ia_car[0])
            
            #Con los otros coches de la IA
            for ia_car2 in self.ia_cars:
                if ia_car[0] != ia_car2[0]:
                    self.collision_manager.actor_actor_collision(ia_car[0], ia_car2[0])

        
        #Colisiones con las cajas de items
        for box in self.items_box:
            
            #Si está en la pantalla, no esta explotando y colisiona con el jugador
            if self.on_screen(box) and box.get_state() != gameobject.EXPLOSION and \
                self.collision_manager.actor_pixelperfectcollision(self.player, box):
                
                #Cambiamos su estado al de explosion
                box.set_state(gameobject.EXPLOSION)
                #Indicamos que el jugador a recogido un itwm
                self.player.collected_item()
                
            #Si no, lo comprobamos para cada uno de lso coches de la IA
            else:
                for ia_car in self.ia_cars:
                    if box.get_state() != gameobject.EXPLOSION and \
                        self.collision_manager.actor_pixelperfectcollision(ia_car[0], box):
                        if self.on_screen(box):
                            box.set_state(gameobject.EXPLOSION)
        
        #Colisiones de los misiles
        for bullet in self.bullets:
            if self.collision_manager.item_level_collision(bullet, self.circuit):
                bullet.set_state(gameobject.EXPLOSION)
            elif bullet.get_state() == gameobject.RUN and \
                self.collision_manager.actor_pixelperfectcollision(self.player, bullet):
                bullet.set_state(gameobject.EXPLOSION)
                self.player.set_state(gameobject.DAMAGED)
            else:
                for ball in self.balls:
                    if self.collision_manager.actor_pixelperfectcollision(ball, bullet):
                        bullet.set_state(gameobject.EXPLOSION)
                        ball.set_state(gameobject.EXPLOSION)
                if bullet.get_state() != gameobject.EXPLOSION:
                    for ia_car in self.ia_cars:
                        if self.collision_manager.actor_pixelperfectcollision(ia_car[0], bullet):
                            bullet.set_state(gameobject.EXPLOSION)
                            ia_car[0].set_state(gameobject.DAMAGED)
        
        #Colisiones de las bolas
        for ball in self.balls:
            if self.collision_manager.item_level_collision(ball, self.circuit):
                pass
            if ball.get_state() == gameobject.RUN and \
                self.collision_manager.actor_pixelperfectcollision(self.player, ball):
                ball.set_state(gameobject.EXPLOSION)
                self.player.set_state(gameobject.DAMAGED)
            elif ball.get_state() != gameobject.EXPLOSION:
                for ia_car in self.ia_cars:
                    if self.collision_manager.actor_pixelperfectcollision(ia_car[0], ball):
                        ball.set_state(gameobject.EXPLOSION)
                        ia_car[0].set_state(gameobject.DAMAGED)
                            
            self.collision_manager.control_limits(ball, self.circuit)
        
        #Colisiones con las manchas de aceite
        for oil in self.oils:
            if self.on_screen(oil) and oil.get_state() != gameobject.NORMAL \
                and self.player.get_old_state() != gameobject.DAMAGED \
                and self.collision_manager.actor_pixelperfectcollision(oil, self.player):
                self.player.set_state(gameobject.DAMAGED)
            for ia_car in self.ia_cars:
                if self.collision_manager.actor_pixelperfectcollision(ia_car[0], oil):
                    ia_car[0].set_state(gameobject.DAMAGED)

        #Colisiones con las manchas de aceite
        for gum in self.gums:
            if self.on_screen(gum) and gum.get_state() != gameobject.NORMAL \
                and self.player.get_old_state() != gameobject.DAMAGED \
                and self.collision_manager.actor_pixelperfectcollision(gum, self.player):
                    
                    if abs(self.player.actual_speed) >= abs(self.player.max_speed / 8):
                        if self.player.actual_speed > 0:
                            self.player.actual_speed = abs(self.player.max_speed / 8)
                        else:
                            self.player.actual_speed = -1 * abs(self.player.max_speed / 8)
                            
            for ia_car in self.ia_cars:
                if self.collision_manager.actor_pixelperfectcollision(ia_car[0], gum):
                    
                    if abs(ia_car[0].actual_speed) >= abs(ia_car[0].max_speed / 8):
                        if ia_car[0].actual_speed > 0:
                            ia_car[0].actual_speed = abs(ia_car[0].max_speed / 8)
                        else:
                            ia_car[0].actual_speed = -1 * abs(ia_car[0].max_speed / 8)
        
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
        '''
        @brief Añade una nueva mancha de aceite en el juego y actualiza el mapa de costes
        
        @param oil Mancha a añadir
        '''
        #Añadimos la nueva mancha
        self.oils.add(oil)
        
        #Actualizamos el mapa del A*
        self.update_astar_map(oil, astar.OIL)
    
    def add_gum(self, gum):
        '''
        @brief Añade un chicle en el juego y actualiza el mapa de costes
        
        @param gum Chicle a añadir
        '''
        #Añadimos el chicle
        self.gums.add(gum)
        
        #Actualizamos el mapa del A*
        self.update_astar_map(gum, astar.GUM)

    def add_ball(self, ball):
        '''
        @brief Añade una nueva bola al juego
        
        @param ball Bola a añadir en el juego
        '''
        self.balls.add(ball)
        
    def add_ia_car(self, ia_car):
        '''
        @brief Método que añade un nuevo coche controlado por la IA al grupo
        
        @param ia_car Nuevo coche
        '''
        self.ia_cars.append(ia_car)
        
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
        for ia_check in self.ia_checkpoints:
            ia_check.add_checkpoint(checkpoint, position)
    
    def add_animation(self, animation):
        '''
        @brief Añade una nueva animación al juego
        
        @param animation Animación a añadir
        '''
        self.static_animations.append(animation)
    
    def update_astar_map(self, sprite, type):
        '''
        @brief Actualiza el mapa de pesos del A*
        
        @brief sprite Sprite con el que actualizaremos el mapa.
        @brief type Tipo del sprite.
        '''
        
        #Obtenemos las coordenadas de los cuatro puntos del rectangulo que representa el sprite
        x = int(math.floor(sprite.rect.x / self.circuit.get_tile_width()))
        y = int(math.floor(sprite.rect.y / self.circuit.get_tile_height()))
        x2 = int(math.floor((sprite.rect.x + sprite.rect.w) / self.circuit.get_tile_width()))
        y2 = int(math.floor((sprite.rect.y + sprite.rect.h) / self.circuit.get_tile_height()))

        #Comprobamos para cada uno de las coordenada su valor en el mapa,
        #Si alguno de ellos es menor que que el valor del tipo de sprite
        #Actualizamos el mapa de costes
        if astar.values[astar.map[x][y]] < astar.values[type]:
            astar.map[x][y] = type       
        
        if astar.values[astar.map[x2][y]] < astar.values[type]:
            astar.map[x2][y] = type

        if astar.values[astar.map[x][y2]] < astar.values[type]:
            astar.map[x][y2] = type
        
        if astar.values[astar.map[x][y]] < astar.values[type]:
            astar.map[x2][y2] = type
    
    def order_checkpoints(self):
        self.checkpoints.order_checkpoints()
        for ia_check in self.ia_checkpoints:
            ia_check.order_checkpoints()

    def set_goal(self, goal):
        '''
        @brief Método que asigna la meta del circuito
        
        @param goal Meta a asignar
        '''
        self.checkpoints.set_goal(goal)
        for ia_check in self.ia_checkpoints:
            ia_check.set_goal(goal)
    
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
            self.advices.append(Advice(u'Vuelta Rápida', 'cheesebu', 100, 0.01, 400, 450,(189, 9, 38), 1))
        
        #Reiniciamos el cronometro principal
        self.actual_time.stop()
        self.actual_time.start()
        
        if self.actual_laps + 1 == self.max_laps:
            self.advices.append(Advice(u'Última vuelta', 'cheesebu', 100, 0.01, 400, 550,(189, 9, 38), 1))

        if self.actual_laps >= self.max_laps:
            print "Carrera Completada"
            self.advices.append(Advice('Carrera Completada', 'cheesebu', 100, 0.02, 400, 300,(189, 9, 38), 2))
            self.complete = True
    
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
        self.laps_counter_rect.x = 140
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
        
        x = int(math.floor(rect.centerx / self.circuit.get_tile_width()))
        y = int(math.floor(rect.centery / self.circuit.get_tile_height()))
        
        return (x, y)
