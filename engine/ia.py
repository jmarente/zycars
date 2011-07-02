#-*- encoding: utf-8 -*-

'''
@file Implementación de los coches controlados por la IA
@author José Jesús Marente Florín
@date Abril 2011
'''

import gameobject
import basiccar
import math
import astar
import time
import pygame

from collections import deque

class Point:
    '''
    @brief Representa un punto intermedio por el que el vehiculo debe pasar
    '''
    def __init__(self, x, y, width, height):
        '''
        @brief Constructor.
        
        @param x Posición x según posición del tile y NO coordenada
        @param y Posición y según posición del tile y NO coordenada
        @param width Ancho del tile donde está el punto
        @param height Alto del tile donde está el punto
        '''
        self.rect = pygame.Rect((x * width, y * height, width, height))
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
    
    def __str__(self):
        '''
        @brief Conversor a cadena
        '''
        return str(self.rect)

class IA(basiccar.BasicCar):
    '''
    @brief Controla el comportamiento del vehículo
    '''
    def __init__(self, game_control, xml_file, x, y, angle = 0):
        '''
        @brief Constructor.
        
        @brief game_control Referencia a GameControl
        @brief xml_file Archivo xml con las características
        @brief x Posición x
        @brief y Posición y
        @brief angle Ángulo inicial del vehículo
        '''
        
        basiccar.BasicCar.__init__(self, game_control, xml_file, x, y, angle)
        
        #Simulación se Switch de C o C++.
        #Según el estado llamaremos a una función u otra.
        self.states = {
                    gameobject.NORMAL: self.__normal_state,
                    gameobject.TURBO: self.__turbo_state,
                    gameobject.NOACTION: self.__normal_state,
                    gameobject.RUN: self.__run_state,
                    gameobject.DAMAGED : self.__damaged_state
                    }
                                    
        self.falling = False
        self.min_scale = 0.3
        self.count_scale = 0.02
        self.actual_scale = 1
        self.target_angle = 0
        
        #Donde almacenaremos los objetivos a los que queremos llegar
        self.left_targets = self.passed_targets = deque()
        self.actual_target = None
        
        #Donde almacenaremos los puntos intermedios para llegar a los objetivos
        self.passed_points = self.left_points = deque()
        self.actual_point = None

        #Instancia del algoritmo A* del vehiculo
        self.astar = astar.Astar()
        
        #Hacemos trampas.
        self.rotation_angle = 0.75
        self.hud = basiccar.Hud(self, 'hud.xml')
        self.turbo_time = None
    
    def control_path(self):
        '''
        @brief Calcula el angulo necesario para llegar a un punto intermedio
        '''
        
        if self.actual_point:
            #Calculamos la posición hasta el le punto actual que queremos llegar
            x = self.actual_point.centerx - self.rect.centerx
            y = self.actual_point.centery - self.rect.centery
            
            #Actualizamos el angulo obtenido para que esté en el rando 0-360
            self.target_angle = self.update_angle2(math.degrees(math.atan2(y, x)))
        
            #Angulo actual del coche
            #TO-DO:Rotar el coche suavemente hasta el punto objetivo
            if self.target_angle < self.actual_angle:
                left = self.actual_angle - self.target_angle
                right = 360 - self.actual_angle + self.target_angle
            else:
                left = self.actual_angle + 360 - self.target_angle
                right = self.target_angle - self.actual_angle
                
            if abs(left) < abs(right) and abs(self.target_angle - self.actual_angle) > abs(self.max_speed * self.rotation_angle):
                self.actual_angle -= self.rotation_angle * self.max_speed
            elif abs(self.target_angle - self.actual_angle) > 5:
                self.actual_angle += self.rotation_angle * self.max_speed
        
        self.control_points()

    def control_points(self):
        #Si el coche colisiona con el rectangulo en el que esta el punto
        #Actualizamos la lista de puntos
        if self.actual_point and self.rect.colliderect(self.actual_point.rect):
            
            current_tile = self.game_control.current_tile(self.actual_point.rect)
            if astar.map[current_tile[0]][current_tile[1]] == astar.SELECTED:
                astar.map[current_tile[0]][current_tile[1]] = astar.PASSABLE
            
            #si aún quedán puntos por pasar, obtenemos el siguiente de la lista
            if len(self.left_points) > 0:
                self.actual_point = self.left_points.popleft()
            
            #Si no, indicamos que no queda ninguno
            else:
                self.actual_point = None
    
    def draw(self, screen):
        '''
        @brief Dibuja el coche por pantalla y los puntos por los que tiene que pasar
        '''
        basiccar.BasicCar.draw(self, screen)

        #Mostramos cada uno de los puntos 
        for point in self.left_points:
            pygame.draw.rect(screen, (0, 0, 0), 
                (point.rect.x - self.game_control.circuit_x(), 
                point.rect.y - self.game_control.circuit_y(), 
                point.rect.w, point.rect.h), 1)

    def update(self):
        '''
        @brief Actualiza logicamente
        '''
        #Si hemos cambiado de estado
        if self.state != self.previous_state:
            self.previous_state = self.state
            #Reiniciamos el estado
            self.animations[self.state].restart()
        
        #Llamamos a la función encargada de actualizar segun el estado
        self.states[self.state]()
        
        self.update_position()
        self.update_direction()
        self.update_image()
        
        self.update_angle()
    
    def __normal_state(self):
        '''
        @brief Estado NORMAL
        '''
        #Mientras no comience la carrera el coche permanecerá quieto
        if self.game_control.get_state() == 'race':
            self.state = gameobject.RUN
    
    def __run_state(self):
        '''
        @brief Comportamiento en el estado RUN
        '''
        
        #Si ya no queda ningún punto intermedio
        if len(self.left_points) == 0 and not self.actual_point:
            #print "No hay puntos objetivos, calculando"
            
            '''print "ACTUAL: ", self.rect
            print "OBJETIVO: ", self.actual_target'''
            
            #Si ya hemos pasado un objetivo
            if self.actual_target:
                #introducimos el objetivo en la lista de pasados
                self.passed_targets.append(self.actual_target)
            
            #Si ya no quedan objetivos por los que pasar
            if len(self.left_targets) == 0:
                self.left_targets = self.passed_targets
                self.passed_targets = deque()
            
            #Obtenemos el primero actualmente en la lista de objetivos
            self.actual_target = self.left_targets.popleft()
            
            #Vaciamos la lista de puntos pasados
            self.passed_points = deque()
            
            #Obtenemos la lista de puntos por los que tenemos que pasr
            self.left_points = self.decode_road(self.astar.get_road(self.game_control.current_tile(self.rect), self.game_control.current_tile(self.actual_target)))
            
            #El primero de ellos será el objetivo
            if len(self.left_points) > 0:
                self.actual_point = self.left_points.popleft()
            
            #print "RESULTADO: "
            #for point in self.left_points:
                #print point
        
        #Estimamos el angulo para el punto actual
        self.control_path()
        
        #Movemos el coche
        self.move(+1)
        
        #Aplicamos la trigonometria
        self.trigonometry()
        
        self.control_release_item()
    
    def __turbo_state(self):
        
        #Si es la primera llamada
        if not self.turbo_state:
            #Obtenemos el tiempo de inicio
            self.turbo_state = time.time()
            #Aumentamos la velocidad
            self.max_speed *= 2
        
        #Calculamos el tiempo transcurrido
        elapsed = time.time() - self.turbo_state
        
        #Si a pasado mas de un segundo, volvemos al estado normal
        if elapsed > 1:
            self.state = gameobject.NOACTION
            self.turbo_state = None
            #self.max_speed = self.old_max_speed
            self.max_speed = self.max_speed / 2
        
        self.__normal_state()
    
    def __damaged_state(self):
        
        if not self.start:
            self.start = time.time()
            #self.temp_angle = self.actual_angle
            #self.actual_speed = self.actual_speed / 2
            
        actual = time.time() - self.start
        
        #self.temp_angle += self.rotation_angle * (self.max_speed * 2)
        self.actual_angle += self.rotation_angle * (self.max_speed * 2)
        
        self.control_points()
        
        if actual >= 1:
            self.state = gameobject.RUN
            self.start = None
            self.actual_speed -= 0.5
            self.left_points = deque()
            self.actual_point = None
            
            if len(self.passed_targets) > 0:
                self.left_targets.appendleft(self.actual_target)
                self.actual_target = self.passed_targets.pop()
            else:
                self.left_targets.appendleft(self.actual_target)
                self.actual_target = None

            
    def update_angle2(self, angle):
        '''
        @brief Actualiza un angulo para que esté en el intervalo 0-360
        
        @return Angulo resultante
        '''
        if angle < 0:
            angle += 360
        if angle > 360:
            angle -= 360
        
        return angle
    
    def set_targets(self, points):
        '''
        @brief Inserta los puntos objetivos del vehiculo
        
        @param points Lista de rectangulos con los objetivos
        '''
        for key in points.keys():
            self.left_targets.append(points[key])
        
        #self.actual_target = self.left_targets.popleft()
    
    def decode_road(self, road):
        '''
        @brief Decodifica el camino recibido por A*
        '''
        result = deque()
        
        tile_width = self.game_control.circuit.get_tile_width()
        tile_height = self.game_control.circuit.get_tile_height()
        
        for point in road:
            result.append(Point(point.row, point.column, tile_width, tile_height))
        
        return result
    
    def collected_item(self):
        self.hud.collected_item() 
    
    def control_release_item(self):
        current = self.hud.get_current_item()
        
        released = False
        if current == 'oil' or current == 'gum':
            
            for ia_car in self.game_control.get_ia_cars():
                if ia_car[0] != self:
                    distance = self.distance(ia_car[0])
                    print "DISTANCIA ", distance
                    if distance <= 90:
                        self.hud.release_item()
                        released = True
                        break
            
            if not released:
                distance = self.distance(self.game_control.get_player())
                print "DISTANCIA ", distance
                if distance <= 90:
                    self.hud.release_item()
                    released = True
                
        elif current == 'turbo':
            self.hud.release_item()
        
        else:
            pass
    
    def distance(self, sprite):
        return ((self.rect.centerx - sprite.rect.centerx) ** 2 + (self.rect.centery - sprite.rect.centery) ** 2) ** 0.5

