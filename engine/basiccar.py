# -*- encoding: utf-8 -*-

'''
@file basicar.py
@brief Implementa la clase Hud y Basicar
@author José Jesús Marente Florín
@date Octubre 2010.
'''

import gameobject
import resource
import data
import xml.dom.minidom
import math
import random
import item
import config

class Hud:
    '''
    @brief Clase que representa la casilla del item actual del jugador
    '''
    def __init__(self, player, path_xml, is_ia = False):
        '''
        @brief Constructor.
        
        @param player Referencia al jugador.
        @param path_xml Ruta del archivo xml
        '''
        self.player = player
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Obtenemos la imagen de fondo
        image = parse.getElementsByTagName('image')[0]
        image_code = image.getAttribute('image_code')
        self.image = resource.get_image(image_code)
        
        #Controla los misiles restantes
        self.missile = 0
        
        #Fuente para mostrar los misiles restantes
        self.font = resource.get_font('cheesebu', 40)
        
        #Posicion de la imagen de fondo
        self.centerx = int(image.getAttribute('centerx'))
        self.centery = int(image.getAttribute('centery'))
        self.position_image = self.image.get_rect()
        self.position_image.centerx = self.centerx
        self.position_image.centery = self.centery
                
        #Mapa para los items
        self.items = {}
        self.is_ia = is_ia
        
        #Recorremos cada uno de los items
        for element in parse.getElementsByTagName('item'):
            code = element.getAttribute('code')
            
            self.items[code] = {}
            self.items[code]['image'] = None
            self.items[code]['xml'] = None
            
            #Nos quedamos con su imagen de muestra
            image_code = element.getAttribute('image_code')
            self.items[code]['image'] = resource.get_image(image_code)
            
            #Y con su archivo xml de configuración
            path_xml = element.getAttribute('path_xml')
            self.items[code]['xml'] = path_xml
        
        if self.is_ia and 'turbo' in self.items.keys():
            del self.items['turbo']
        
        #En un principio no tenemos ningun item
        self.actual_item = None
        
        self.temp_angle = None
                
    def draw(self, screen):
        '''
        @brief Método encargado de dibujar en pantalla el hud
        
        @param screen Superficie destino
        '''
                
        #Si hay algun item actualmente lo mostramos
        if self.actual_item:
            #Obtenemos posicion
            self.position_image = self.items[self.actual_item]['image'].get_rect()
            self.position_image.centerx = self.centerx
            self.position_image.centery = self.centery
            
            #Mostramos
            screen.blit(self.items[self.actual_item]['image'], self.position_image)
            
            #Si el item es del tipo de 3 misiles, mostramos los misiles restantes
            if self.actual_item == "3missile":
                surface = self.font.render(str(self.missile), True, (0, 0, 0))
                screen.blit(surface, self.position_image)
        
        #Si no, mostramos el casillero vacio
        else:
            #Obtenemos la posicion
            self.position_image = self.image.get_rect()
            self.position_image.centerx = self.centerx
            self.position_image.centery = self.centery
            
            #Pintamos
            screen.blit(self.image, self.position_image)

            
    def release_item(self):
        '''
        @brief Método llamado cuando se a lanzado un item
        '''
        #Si tenemos algun item, lo lanzamos
        if self.actual_item:
            self.player.release_item(self.actual_item, self.items[self.actual_item]['xml'])
            
            #Si es del tipo 3 misiles, restamos los misiles restantes
            if self.actual_item == "3missile":
                self.missile -= 1
                
            #Si no tenemos mas misiles o el item es disinto de 3 misiles
            #Indicamos que no nos quedan misiles
            if self.missile == 0 or self.actual_item != "3missile":
                self.actual_item = None
            
    def collected_item(self):
        '''
        @brief Método llamado cuando recogemos algun item
        '''
        #Si no tenemos actualmente un item
        if not self.actual_item:
            
            if config.Config().get_mode() == config.TIMED:
                self.actual_item = 'turbo'
            else:
                #Obtenemos uno aleatorio de la lista
                self.actual_item = self.items.keys()[random.randint(0, len(self.items.keys()) - 1)]
                
            #self.actual_item = 'turbo'
            print "Jugador ", self.player, " recoge: ", self.actual_item
            if self.actual_item == '3missile':
                self.missile = 3
    
    def get_current_item(self):
        '''
        @brief Consulta el item actual
        
        @return Item actual
        '''
        return self.actual_item
                
class BasicCar(gameobject.GameObject):
    '''
    @brief Clase "virtual pura" que abstrae el comportamiento y las características 
    básicas de los vehiculos en el juego
    '''
    def __init__(self, game_control, xml_file, x, y, angle = 0):
        '''
        @brief Constructor.
        
        @param game_control Referencia a Gamecontrol
        @param xml_file Archivo xml con la configuración del objeto
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param angle Ángulo del objeto, por defecto será 0.
        '''
        gameobject.GameObject.__init__(self, game_control)
        
        self.break_force = None
        self.avatar = None
        self.racer_image = None
        self.name_character = ""

        #Parseamos la información básica
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_file))
        self.parser_car_info(parser)
        self.parser_basic_info(parser)
        
        #Definimos la posición del objeto
        self.x = self.old_x = x
        self.y = self.old_y = y
        
        self.start = None
        self.turbo_state = None
        self.turbo_sound = resource.get_sound('turbo')
        self.turbo_sound.set_volume(config.Config().get_sound_volume())
        
        self.old_max_speed = self.max_speed

        self.front_line = gameobject.Line(1, 1, 1, 1)
        self.back_line = gameobject.Line(1, 1, 1, 1)
        
        #Si el angulo es 0, no hacemos nada
        if angle == 0:
            self.dx = 0
            self.dy = 0
        #Si es 0 actualizamos el angulo del coche
        else:
            self.actual_angle = angle
            self.dx = math.cos(angle) * self.actual_speed
            self.dy = math.sin(angle) * self.actual_speed
        
        #Actualizamos la posicion del coche según su angulo
        self.update_position()
        #Actualizamos la rotación de la imagen del coche
        self.update_image()

    def draw(self, screen):
        '''
        @brief Método encargado de dibujar el objeto sobre una superficie
        
        @param screen Superficie destino
        '''
        gameobject.GameObject.draw(self, screen)
        #pygame.draw.line(screen, (0, 0, 0), (self.front_line.x1 - self.game_control.circuit_x(), self.front_line.y1 - self.game_control.circuit_y()),(self.front_line.x2 - self.game_control.circuit_x(), self.front_line.y2 - self.game_control.circuit_y()))
        #pygame.draw.line(screen, (255, 0, 0), (self.back_line.x1 - self.game_control.circuit_x(), self.back_line.y1 - self.game_control.circuit_y()),(self.back_line.x2 - self.game_control.circuit_x(), self.back_line.y2 - self.game_control.circuit_y()))
        
    def parser_car_info(self, parse):
        '''
        @brief Método que parsea la información básica de los coches.
        '''
        parent_node = parse.firstChild
        self.name_character = parent_node.getAttribute('name_character')
        self.avatar = resource.get_image(parent_node.getAttribute('avatar'))
        self.racer_image = resource.get_image(parent_node.getAttribute('racer_image'))
        self.max_speed = float(parent_node.getAttribute('max_speed'))
        self.min_speed = float(parent_node.getAttribute('min_speed'))
        self.rotation_angle = float(parent_node.getAttribute('rotation_angle'))
        self.aceleration = float(parent_node.getAttribute('aceleration'))
        self.desaceleration = float(parent_node.getAttribute('desaceleration'))
        
    def update(self):
        '''
        @brief Método que debe ser implementado por sus descendientes
        '''
        raise NotImplementedError("La funcion update de GameObject debe ser implementada por sus descendientes")
        
    def get_speed(self):
        '''
        @brief Método consultor.
        
        @return La velocidad actual del vehículo.
        '''
        return self.actual_speed
        
    def set_speed(self, new_speed):
        '''
        @brief Método que modifica la velocidad actual.
        
        @param new_speed Nueva velocidad actual para el vehículo.
        '''
        self.actual_speed = new_speed
        
    def get_max_speed(self):
        '''
        @brief Métodod consultor
        
        @return Velocidad máxima del vehículo.
        '''
        return self.max_speed
        
    def set_max_speed(self, new_max_speed):
        '''
        @brief Método que modifica la velocidad maxima del vehiculo
        
        @param new_max_speed Nueva velocidad máxima del vehículo.
        '''
        self.max_speed = abs(new_max_speed)
        
    def get_min_speed(self):
        '''
        @brief Método consultor
        
        @return Velocidad mínima(marcha atrás) del vehículo.
        '''
        return self.min_speed
        
    def set_min_speed(self, new_min_speed):
        '''
        @brief Metodo encargado de modificar la velocidad minima del vehiculo
        
        @param new_min_speed Nueva velocidad mínima del vehículo.
        '''
        self.min_speed = abs(new_min_speed)
    
    def get_avatar(self):
        '''
        @brief Consultor de la imagen de avatar
        
        @return Imagen avatar del jugador
        '''
        return self.avatar
    
    def get_name(self):
        '''
        @brief Consultor del nombre del personaje.
        
        @return nombre del personaje
        '''
        return self.name_character
    
    def get_racer_image(self):
        '''
        @brief Consultor de la imagen de corredor
        
        @return Imagen de corredor
        '''
        return self.racer_image

    def release_item(self, item_type, path_xml):
        '''
        @brief Encargado de añadir el item al juego.
        
        @param item_type Tipo del item
        @param path_xml Archivo xml del item
        '''

        if item_type == 'missile' or item_type == '3missile':
            missile = item.Missile(self.game_control, self, path_xml, self.x, 
                                self.y, self.actual_angle)
            self.game_control.add_bullet(missile)
            
        elif item_type == 'oil':
            oil = item.Oil(self.game_control, self, path_xml, self.x, self.y, 
                        self.actual_angle)
            self.game_control.add_oil(oil)
            
        elif item_type == 'gum':
            gum = item.Oil(self.game_control, self, path_xml, self.x, self.y, 
                        self.actual_angle, True)
            self.game_control.add_gum(gum)
            
        elif item_type == 'ball':
            ball = item.Ball(self.game_control, self, path_xml, self.x, 
                        self.y, self.actual_angle)
            self.game_control.add_ball(ball)
            
        elif item_type == 'turbo':
            self.turbo_sound.play()
            self.state = gameobject.TURBO
    
    def update_lines(self):
        '''
        @brief Actualiza los segmentos del coche
        '''
        angle = math.radians(self.actual_angle)
        frontx = math.cos(angle) * (300)
        fronty = math.sin(angle) * (300)
        backx = math.cos(angle) * (-200)
        backy = math.sin(angle) * (-200)
        self.front_line = gameobject.Line(self.rect.centerx, self.rect.centery, 
                                        self.rect.centerx + frontx, 
                                        self.rect.centery + fronty)
        self.back_line = gameobject.Line(self.rect.centerx, self.rect.centery, 
                                        self.rect.centerx + backx, 
                                        self.rect.centery + backy)

    def get_front_line(self):
        '''
        @brief Consulta la linea delantera
        
        @return Linea delantera
        '''
        return self.front_line
        
    def get_back_line(self):
        '''
        @brief Consulta la linea trasera
        
        @return Linea trasera
        '''
        return self.back_line
