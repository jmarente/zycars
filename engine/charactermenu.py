#-*- encoding: utf-8 -*-

import basicmenu
import data
import resource
import imagebutton
import mainmenu
import xml.dom.minidom
import pygame
import math
import circuitmenu
import random

from config import *
from collections import deque

class CarFeatures:
    '''
    @brief Clase CarFeatures, encargada de mostrar por pantalla las distintas 
    características del coche actual seleccionado
    '''
    def __init__(self, x, y, font_code, image_code):
        '''
        @brief Consturctor de CarFeatures
        
        @param x posición de las características en el eje x
        @param y posición en el eje y
        @param font_code código de la fuente a usar
        @param image_code código de la imagen a usar
        '''
        #Asignamos posición en la pantalla
        self.x = x
        self.y = y
        
        #Cargamos los nombres de cada carcterísticas
        self.text_speed = resource.get_font(font_code, 30).render('Velocidad', True, (0,0,0))
        
        #Situamos la posición de cada una de ellas
        self.text_speed_y = y
        self.text_aceleration = resource.get_font(font_code, 30).render(u'Aceleración', True, (0,0,0))
        self.text_aceleration_y = self.y + self.text_speed.get_height() + 15
        self.text_rotation = resource.get_font(font_code, 30).render('Giro', True, (0,0,0))
        self.text_rotation_y = self.text_aceleration_y + self.text_aceleration.get_height() + 15
        
        #Cargamos la imagen 
        self.indicator = resource.get_image(image_code)
        
        #Inicializamos los valores de cada una de las características
        self.speed = 0
        self.aceleration = 0
        self.rotation = 0
        
    def update_values(self, speed, aceleration, rotation):
        '''
        @brief Función encargada de actualizar los distintos valores
        
        @param speed velocidad del nuevo coche
        @param aceleration aceleración del nuevo coche
        @param rotation angulo de giro del coche
        '''
        self.speed = int(math.floor(speed))
        self.aceleration = int(math.floor(aceleration))
        self.rotation = int(math.floor(rotation))
        
    def draw(self, screen):
        '''
        @brief Función encargada de pintar los componentes
        
        @param screen superficie destino
        '''
        screen.blit(self.text_speed, (self.x, self.text_speed_y)) 
        
        #Acumulación del desplazamiento de la x
        plus_x = self.x + 150
        #Dibujamos una raya por cada calor de speed
        for i in range(0, self.speed):
            screen.blit(self.indicator, (plus_x, self.text_speed_y - 5))
            #Obtenemos el desplazamiento de la siguiente imagen
            plus_x += self.indicator.get_width() + 3
            
        screen.blit(self.text_aceleration, (self.x, self.text_aceleration_y))
        
        plus_x = self.x + 150
        #Dibujamos una raya por cada calor de aceleration
        for i in range(0, self.aceleration):
            screen.blit(self.indicator, (plus_x, self.text_aceleration_y - 5))
            #Obtenemos el desplazamiento de la siguiente imagen
            plus_x += self.indicator.get_width() + 3
            
        screen.blit(self.text_rotation, (self.x, self.text_rotation_y))
        
        plus_x = self.x + 150
        #Dibujamos una raya por cada calor de rotation
        for i in range(0, self.rotation):
            screen.blit(self.indicator, (plus_x, self.text_rotation_y - 5))       
            #Obtenemos el desplazamiento de la siguiente imagen
            plus_x += self.indicator.get_width() + 3
            
class GroupOption:
    '''
    @brief Clase que representa distintas opciones en forma de cola
    '''
    def __init__(self, father, parse_xml, image_normal_code, image_selected_code, x, y, image_y):
        '''
        @brief Constructor de GroupOption
        
        @param father referencia al menu al que pertenece
        @param parse_xml fragmento de xml que contiene las distintas opciones
        @param image_normal_code codigo de la imagen que representa a la opción no elegida
        @param image_selected_code codigo de la imagen qye representa a la opcion actual
        @param x posicion en el eje x
        @param y posicion en el eje y
        @param image_y posicion de la imagen en el eje y, en el eje x sera la misma que la del objeto
        '''
        #Asignamos los distintos componentes
        self.x = x
        self.y = y
        self.image_y = image_y
        self.father = father
        self.normal_image = resource.get_image(image_normal_code)
        self.option1_x = x
        self.option2_x = self.normal_image.get_width() + self.option1_x + 50
        self.selected_image = resource.get_image(image_selected_code)
        self.option3_x = self.normal_image.get_width() + self.option2_x + 50
        
        #Declaramos dos colas
        #Izquierda representara las opciones de estarían a la izquierda que no se están mostrando
        self.left_options = deque()
        #Derecha representara las opciones de estarían a la derecha que no se están mostrando
        self.right_options = deque()
        
        #Las tres opciones actuales mostradas
        self.actual_option = None
        self.actual_right = None
        self.actual_left = None
        
        #Recorremos el parser para obtener las distintas opciones
        for element in parse_xml.getElementsByTagName('character'):
            image_code = element.getAttribute('image')
            name = element.getAttribute('name')
            
            result = {}
            result['name'] = name
            result['image'] = resource.get_image(image_code)
            self.right_options.append(result)
        
        #Situamos opcion actual como la primera que se encontraba en las opciones de la derecha
        self.actual_option = self.right_options.popleft()
        
        #La siguiente sera la opción de la derecha
        self.actual_right = self.right_options.popleft()

    def update(self):
        pass
        
    def draw(self, screen):
        '''
        @brief Método encargado de dibujar los elementos.
        
        @param screen superficie destino
        '''
        #Si hay alguna opción a la izquierda
        if self.actual_left:
            #Mostramos fondo e imagen
            screen.blit(self.normal_image, (self.option1_x, self.y))
            rect = self.actual_left['image'].get_rect()
            rect.centerx = self.option1_x + self.normal_image.get_width() / 2
            rect.y = self.image_y
            #screen.blit(self.actual_left['image'], (self.option1_x, self.image_y))
            screen.blit(self.actual_left['image'], rect)
        
        #Mostramos la opcion actual en el centro
        screen.blit(self.selected_image, (self.option2_x, self.y))
        rect = self.actual_option['image'].get_rect()
        rect.centerx = self.option2_x + self.selected_image.get_width() / 2
        rect.y = self.image_y
        #screen.blit(self.actual_option['image'], (self.option2_x, self.image_y))
        screen.blit(self.actual_option['image'], rect)
        
        #Si hay alguna opción a la derecha
        if self.actual_right:
            #Mostramos fondo e imagen
            screen.blit(self.normal_image, (self.option3_x, self.y))
            rect = self.actual_right['image'].get_rect()
            rect.centerx = self.option3_x + self.normal_image.get_width() / 2
            rect.y = self.image_y
            #screen.blit(self.actual_right['image'], (self.option3_x, self.image_y))
            screen.blit(self.actual_right['image'], rect)
        
    def actual_selected(self):
        '''
        @brief Método que devuelve el nombre de la opción seleccionada actualmente
        
        @return devuelve la opción seleccionada
        '''
        return self.actual_option['name']
        
    def move_left(self):
        '''
        @brief Metodo que desplaza las opciones hacia la izquierda
        '''
        #Si hay alguna opción a la derecha
        if self.actual_right:
            
            #Insertamos la izquierda actual en la lista de la izquierda
            self.left_options.append(self.actual_left)
            
            #La opción actual pasa a la izquierda
            self.actual_left = self.actual_option
            
            #La opción de la derecha pasa a ser la actual
            self.actual_option = self.actual_right
                        
            #Si aún hay opciones en la lista de la derecha
            if len(self.right_options) > 0:
                #La primera de ella pasa a la opcion derecha actual
                self.actual_right = self.right_options.popleft()
            #Si no, pasa a estar vacía
            else:
                self.actual_right = None
                
    def move_right(self):
        '''
        @brief Método que desplaza las opciones a la derecha
        '''
        #Si hay alguna opción en la izquierda
        if self.actual_left:
            
            #Insertamos la de la derecha en la lista de las opciones de la derecha
            self.right_options.appendleft(self.actual_right)
            
            #Actualizamos las distintas opciones 
            self.actual_right = self.actual_option
            self.actual_option = self.actual_left
            
            #Si aún quedan opciones en la izquierda
            if len(self.left_options) > 0:
                #La primera de ellas pasa a ser la izquierda actual
                self.actual_left = self.left_options.pop()
            else:
                self.actual_left = None
                
    def add_option(self, new_option):
        '''
        @brief Método que añade una nueva opcion a lista
        
        @param new_option nueva opción a añadir
        '''
        #Si aun no hemos añadido ningun opción
        if not self.actual_option:
            #Pasa a ser la actual
            self.actual_option = new_option
        #Si no la añadimos en las opciones de la derecha
        else:
            self.right_options.append(new_option)

class CharacterMenu(basicmenu.BasicMenu):
    '''
    @brief CharacterMenu es la clase que representará la elección de un personaje deteminado
    '''
    def __init__(self, game, path_xml):
        '''
        @brief Constructor de CharacterMenu
        
        @param game referencia a game
        @param path_xml ruta del archivo xml con los distintos elementos
        '''
        basicmenu.BasicMenu.__init__(self, game)
        
        #Cambiamos el título de la pantalla
        pygame.display.set_caption("Zycars: Selección de personaje")
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Parseamos la informacion básica de los menus
        self.parser_basic_info(parse)
        
        #Inicializamos car_features para representar las caracteristicas de los personajes
        self.car_features = CarFeatures(500, 350 , 'cheesebu', 'slider_controler')
        
        #Obtenemos el fragmento de los personajes 
        characters_parse = parse.getElementsByTagName('characters')[0]
        #Inicializmaos el grupo de opciones
        self.group_option = GroupOption(self, characters_parse, characters_parse.getAttribute('normal_image'), \
                                        characters_parse.getAttribute('selected_image'),150, 110, 90)
                
        self.cars = {}
        first = True
        
        #Obtenemos las distintas caracterísitcas del personaje
        for element in parse.getElementsByTagName('character'):
            
            character_name = element.getAttribute('name')
            image_car_code = element.getAttribute('image_car')
            path_xml = element.getAttribute('path_xml')
            rotation = float(element.getAttribute('rotation'))
            aceleration = float(element.getAttribute('aceleration'))
            speed = float(element.getAttribute('speed'))

            self.cars[character_name] = {}
            self.cars[character_name]['image_car'] = resource.get_image(image_car_code)
            self.cars[character_name]['name_character'] = resource.get_font('cheesebu', 40).render(character_name, True, (255, 255, 255))
            self.cars[character_name]['path_xml'] = path_xml
            self.cars[character_name]['speed'] = speed
            self.cars[character_name]['aceleration'] = aceleration
            self.cars[character_name]['rotation'] = rotation
            
            if first:
                self.car_features.update_values(speed, aceleration, rotation)
                first = False

        self.new_pressed = True
    
    def draw(self, screen):
        '''
        @brief Método que dibuja los elementos del menú en pantalla
        '''
        #Dibujamos los elementos básicos
        self.draw_basic_elements(screen)
        
        #Dibujamos todos y cada uno de los botones
        for button in self.buttons:
            button.draw(screen)
        
        self.group_option.draw(screen)
        
        #Mostramos el coche del personaje actual
        screen.blit(self.cars[self.group_option.actual_selected()]['image_car'], (50, 325))
        
        #Mostramos el nombre del personaje
        position_name = self.cars[self.group_option.actual_selected()]['name_character'].get_rect()
        position_name.y = 270
        position_name.centerx = 400
        screen.blit(self.cars[self.group_option.actual_selected()]['name_character'], position_name)
        
        #Mostramos las caracteristicas del coche
        self.car_features.draw(screen)
        
        #Dibujamos el cursor sobre todo
        self.cursor.draw(screen)
    
    def treat_option(self, option):
        '''
        @brief Método que se llama cuando se pulsa algun boton
        '''
        #Si pulsamos el botón de aceptar
        if option == "Aceptar":
            #Guardamos el coche seleccionado
            selected_player = self.group_option.actual_selected()
            print "Aceptar"
            print "Jugador Elegido:" + self.cars[selected_player]['path_xml']
            Config().set_player(self.cars[selected_player]['path_xml'])
            
            Config().clear_competitors()
            #Si el modo de juego no es Contrarreloj, obtenemos los rivales
            if Config().get_mode() != TIMED:
                #Obtenemos los rivales
                rivals = self.get_rivals(selected_player)
                
                #Los añadimos a la configuracion
                for rival in rivals:
                    Config().add_competitor(self.cars[rival]['path_xml'])
                    
                print "Rivales :", Config().get_competitors()
            
            #Si estamos en modo contrarreloj cargamos el menu Contrarreloj
            if Config().get_mode() == TIMED:
                self.game.change_state(circuitmenu.CircuitMenu(self.game, 'menu/cronomenu.xml'))
            
            #Si estamos en Carrera Rápida cargamos el menú de Carrera Rápida
            elif Config().get_mode() == FASTRACE:
                self.game.change_state(circuitmenu.CircuitMenu(self.game, 'menu/fastracemenu.xml'))
            
            elif Config().get_mode() == CHAMPIONSHIP:
                self.game.change_state(circuitmenu.CircuitMenu(self.game, 'menu/fastracemenu.xml'))
                
        #Si pulsamos cancelar
        elif option == "Cancelar":
            #Volveriamos al menú anterior
            print "Cancelar"
            self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))

        #Si pulsamos la felcha hacia la izquierda
        elif option == "Izquierda":
            
            #Y no estaba el ratón pulsado anteriormente
            if self.new_pressed:
                print "Izquierda"
                #Movemos hacia la izquierda el grupo de opciones
                self.group_option.move_right()
                
                #Coche actual
                selected_car = self.group_option.actual_selected()
                
                self.update_car_features(selected_car)
        
        #Si pulsamos la flecha hacia la derecha
        elif option == "Derecha":
            #Y no estaba el ratón pulsado anteriormente
            if self.new_pressed:
                print "Derecha" 
                #Movemos el grupo de opciones
                self.group_option.move_left()
                
                #Coche actual
                selected_car = self.group_option.actual_selected()
                
                self.update_car_features(selected_car)

    def update_car_features(self, selected_car):
        '''
        @brief Método para actualizar las características del coche
        '''
        #Obtenemos las características del coche actual
        speed = self.cars[selected_car]['speed']
        aceleration = self.cars[selected_car]['aceleration']
        rotation = self.cars[selected_car]['rotation']
        
        #Actualizamos las características
        self.car_features.update_values(speed, aceleration, rotation)
                    
    def get_rivals(self, selected):
        
        rivals_selected = []
        all_rivals = []
        
        for key in self.cars.keys():
            all_rivals.append(key)
        
        while len(rivals_selected) < 3:
            rival = all_rivals[random.randint(0, len(all_rivals) - 1)]
            if rival != selected and rival not in rivals_selected:
                rivals_selected.append(rival)
        
        return rivals_selected
                
            
