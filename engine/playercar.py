#-*- encoding: utf-8 -*-

import basiccar
import gameobject
import resource
import keyboard
import data
import item
import pygame
import xml.dom.minidom
import random
import time

class Hud:
    '''
    @brief Clase que representa la casilla del item actual del jugador
    '''
    def __init__(self, player, path_xml):
        '''
        @brief Constructor.
        
        @param player Referencia al jugador.
        @param path_xml Ruta del archivo xml donde se encuentra toda las características
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
                surface = self.font.render(str(self.missile), True, (0,0,0))
                screen.blit(surface, self.position_image)
        
        #Si no, mostramos el casillero vacio
        else:
            #Obtenemos la posicion
            self.position_image = self.image.get_rect()
            self.position_image.centerx = self.centerx
            self.position_image.centery = self.centery
            
            #Pintamos
            screen.blit(self.image, self.position_image)

            
    def released_item(self):
        '''
        @brief Método llamado cuando se a lanzado un item
        '''
        #Si tenemos algun item, lo lanzamos
        if self.actual_item:
            self.player.released_item(self.actual_item, self.items[self.actual_item]['xml'])
            
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
            #Obtenemos uno aleatorio de la lista
            self.actual_item = self.items.keys()[random.randint(0, len(self.items.keys()) - 1)]
            if self.actual_item == '3missile':
                self.missile = 3

class PlayerCar(basiccar.BasicCar):
    '''
    @brief Clase que modela el comportamiento y las características del vehículo del jugador
    '''
    def __init__(self, game_control, xml_file, x, y, angle = 0, player = 1):
        '''
        @brief Consturtor
        
        @param game_control Referencia a GameControl.
        @param xml_file Ruta de archivo xml con ls características del coche.
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param angle Angulo del coche, por defecto 0
        @param player Indica el jugador para los controles
        '''
        basiccar.BasicCar.__init__(self, game_control, xml_file, x, y, angle)
        
        self.__assing_controls(player)
        
        #Simulación se Switch de C o C++.
        #Según el estado llamaremos a una función u otra.
        self.states = {
                    gameobject.NORMAL: self.__normal_state, 
                    gameobject.NOACTION: self.__noaction_state, 
                    gameobject.RUN: self.__run_state, 
                    gameobject.FORWARD: self.__forward_state, 
                    gameobject.REVERSE: self.__reverse_state, 
                    gameobject.DAMAGED: self.__damaged_state, 
                    gameobject.ERASE: self.__erase_state, 
                    gameobject.YAW: self.__yaw_state,
                    gameobject.FALL: self.__fall_state,
                    gameobject.TURBO: self.__turbo_state
                    }
        
        self.falling = False
        self.min_scale = 0.3
        self.count_scale = 0.02
        self.actual_scale = 1
        
        #HUD del coche
        self.hud = Hud(self, 'hud.xml')
    
    def update(self):
        '''
        @brief Método encargado de actualizar lógicamente el coche.
        '''
        #Si hemos cambiado de estado
        if self.state != self.previous_state:
            self.previous_state = self.state
            #Reiniciamos el estado
            self.animations[self.state].restart()
        
        #Llamamos a la función encargada de actualizar segun el estado
        self.states[self.state]()
        
        #Si pulsamos espacio, lanzamos el item que tengamos actualmente
        if keyboard.newpressed(pygame.K_SPACE):
            self.hud.released_item()
        
        #Si el coche no se encuentra cayendo
        if self.state != gameobject.FALL:
            #Actualizmaos posicion. imagen y dirección
            self.update_position()
            self.update_direction()
            self.update_image()
        
        self.update_angle()
        
    def __normal_state(self):
        '''
        @brief Método que actualiza al coche en su estado normal
        '''
        #Según la tecla pulsada cambiamos de estado o no
        if keyboard.pressed(self.UP):
            self.old_state = gameobject.NORMAL
            self.state = gameobject.RUN
        elif keyboard.pressed(self.DOWN):
            self.old_state = gameobject.NORMAL
            self.state = gameobject.REVERSE
            
    def __run_state(self):
        '''
        @brief Método que actualiza al coche en su estado run(en marcha)
        '''
        self.move(+1)
        
        #Según la tecla pulsada cambiamos de estado o no
        if keyboard.release(self.UP):
            self.old_state = gameobject.RUN
            self.state = gameobject.NOACTION
        if keyboard.pressed(self.DOWN):
            self.old_state = gameobject.RUN
            self.state = gameobject.REVERSE
        
        #Controlamos la rotación del coche
        self.control_rotation()
        
        #Y la trigonometria del mismo
        self.trigonometry()
    
    def __turbo_state(self):
        '''
        @brief Coche en turbo
        '''
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
        
        #Movemos el coche
        self.move(+1)
            
        #Controlamos la rotación del coche
        self.control_rotation()
        
        #Y la trigonometria del mismo
        self.trigonometry()

    def __noaction_state(self):
        '''
        @brief Método que actualiza al coche en su estado 
        noaction(En marcha sin pulsar ningun boton de direccion)
        '''
        #Según la tecla pulsada cambiamos de estado o no
        if keyboard.pressed(self.UP):
            self.old_state = gameobject.NOACTION
            self.state = gameobject.RUN
        if keyboard.pressed(self.DOWN):
            self.old_state = gameobject.NOACTION
            self.state = gameobject.REVERSE
        
        #Controlamos la desaceleración del mismo
        if self.actual_speed > self.desaceleration:
            self.actual_speed -= self.desaceleration
        elif self.actual_speed < -self.desaceleration:
            self.actual_speed += self.desaceleration
        else:
            self.actual_speed = 0
            self.state = gameobject.NORMAL
                    
        #Controlamos la rotación del coche
        self.control_rotation()
        
        #Y la trigonometria del mismo
        self.trigonometry()
            
    def __reverse_state(self):
        '''
        @brief Método que actualiza al coche en su estado de marcha atras 
        '''
        self.move(-1)
        
        #Controlamos la desaceleración del mismo
        if keyboard.release(self.DOWN):
            self.old_state = gameobject.REVERSE
            self.state = gameobject.NOACTION
        if keyboard.pressed(self.UP):
            self.old_state = gameobject.REVERSE
            self.state = gameobject.RUN
        
        #Controlamos la rotación del coche
        self.control_rotation()
        
        #Y la trigonometria del mismo
        self.trigonometry()
    
    def __fall_state(self):
        '''
        @brief Método que actualiza al coche en su estado cayendo por algun hoyo
        '''
        if not self.falling:
            self.image = self.original_sprite[self.animations[self.state].get_frame()]
            self.falling = True
        
        self.image = pygame.transform.rotozoom(self.image, -5, self.actual_scale)
        
        #Actualizamos tanto el alto como el ancho 
        self.rect.w = self.image.get_width()
        self.rect.h = self.image.get_height()
        
        self.actual_scale -= self.count_scale
        
        if self.actual_scale < self.min_scale:
            self.actual_speed = 0
            self.state = gameobject.NOACTION
            self.old_state = gameobject.FALL
            self.falling = False
            self.actual_scale = 1
            self.x += 90

    def __damaged_state(self):
        
        if not self.start:
            self.start = time.time()
            #self.temp_angle = self.actual_angle
            #self.actual_speed = self.actual_speed / 2
            
        actual = time.time() - self.start
        
        #self.temp_angle += self.rotation_angle * (self.max_speed * 2)
        self.actual_angle += self.rotation_angle * (self.max_speed * 2)
        
        if actual >= 1:
            self.state = gameobject.NOACTION
            self.start = None
            self.actual_speed -= 0.5
            #self.old_angle = None
            #self.actual_angle = self.temp_angle
            #self.temp_angle = None
        
    def __forward_state(self):
        pass
        
    def __erase_state(self):
        pass
        
    def __yaw_state(self):
        pass
    
    def control_rotation(self):
        '''
        @brief Método que actualiza la rotación del coche
        '''
        if keyboard.pressed(self.LEFT):
            self.actual_angle -= self.rotation_angle * self.max_speed
        elif keyboard.pressed(self.RIGHT):
            self.actual_angle += self.rotation_angle * self.max_speed
        
    def __assing_controls(self, player):
        '''
        @brief Método que asigna los controles segun el tipo de jugador.
        '''
        if player == 1:
            self.UP = pygame.K_UP
            self.DOWN = pygame.K_DOWN
            self.RIGHT = pygame.K_RIGHT
            self.LEFT = pygame.K_LEFT
        elif player == 2:
            self.UP = pygame.K_w
            self.DOWN = pygame.K_s
            self.RIGHT = pygame.K_d
            self.LEFT = pygame.K_a
    
    def collected_item(self):
        '''
        @brief Método llamado cuando recogemos algún item.
        '''
        self.hud.collected_item()
    
    def released_item(self, item_type, path_xml):

        if item_type == 'missile' or item_type == '3missile':
            missile = item.Missile(self.game_control, self, path_xml, self.x, self.y, self.actual_angle)
            self.game_control.add_bullet(missile)
        elif item_type == 'oil':
            oil = item.Oil(self.game_control, self, path_xml, self.x, self.y, self.actual_angle)
            self.game_control.add_oil(oil)
        elif item_type == 'gum':
            gum = item.Oil(self.game_control, self, path_xml, self.x, self.y, self.actual_angle, True)
            self.game_control.add_gum(gum)
        elif item_type == 'ball':
            ball = item.Ball(self.game_control, self, path_xml, self.x, self.y, self.actual_angle)
            self.game_control.add_ball(ball)
        elif item_type == 'turbo':
            self.state = gameobject.TURBO
    
    def draw_hud(self, screen):
        self.hud.draw(screen)
