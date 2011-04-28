#-*- encoding: utf-8 -*-

import data
import resource
import basicmenu
import pygame
import button
import imagebutton
import charactermenu
import xml.dom.minidom

from config import *

class Times:
    '''
    @brief Clase encargada de mostrar los tiempos del circuito selecionado actualmente
    '''
    def __init__(self, x, y, path_xml):
        '''
        @brief Constructor
        
        @param x Posición en el eje x
        @param y Posición en el eje y
        @param path_xml Ruta del archivo xml con los tiempos de cada circuito
        '''
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Mapa que contendrá los tiempos de cada circuito
        self.circuits = {}
        
        #Fuente para los textos
        self.font = resource.get_font('cheesebu', 30)
        
        #Superfice con el texto de Mejor Carrera y posición
        self.best_text = self.font.render('Mejor Carrera', True, (194, 26, 26))
        self.best_text_position = (x, y)
        
        #Superficie con el texto de Vuelta Rapida y donde se almacenará la posición
        self.fasttest_text = self.font.render(u'Vuelta Rápida', True, (194, 26, 26))
        self.fasttest_text_position = None
        
        #Superficie que contendrá los tiempos de los circuitos
        self.best_race = None        
        self.fasttest_lap = None
        
        #Posiciones de cada uno de los tiempos
        self.best_race_position = None
        self.fasttest_lap_position = None

        #Recorremos los circuitos y obtener los tiempos de estos
        for circuit in parse.getElementsByTagName('circuit'):
            
            #Nombre del circuito para añadir al mapa
            name = circuit.getAttribute('name')
            self.circuits[name] = {}
            self.circuits[name]['fasttestlap'] = None
            self.circuits[name]['bestrace'] = None
            
            #Obtenemos el tiempo de la mejor carrera
            bestrace = circuit.getElementsByTagName('bestrace')[0]
            minutes = bestrace.getAttribute('minutes')
            seconds = bestrace.getAttribute('seconds')
            hseconds = bestrace.getAttribute('hseconds')
            self.circuits[name]['bestrace'] = (minutes, seconds, hseconds)
            
            #Obtenemos el tiempo de la mejor vuelta
            fasttestlap = circuit.getElementsByTagName('fasttestlap')[0]
            minutes = fasttestlap.getAttribute('minutes')
            seconds = fasttestlap.getAttribute('seconds')
            hseconds = fasttestlap.getAttribute('hseconds')
            self.circuits[name]['fasttestlap'] = (minutes, seconds, hseconds)
                
    def update(self, circuit_name):
        '''
        @brief Método que actualiza el estado de Times, segun el circuito que se le pase
        
        @param circuit_name Nombre del circuito para obtener los tiempos
        '''
        #Si tenemos tiempos del circuito que se pasa
        if self.circuits.has_key(circuit_name):
            #Renderizamos sus valores
            self.best_race = self.font.render(self.circuits[circuit_name]['bestrace'][0] \
                                                + ':' + self.circuits[circuit_name]['bestrace'][1] \
                                                + ':' + self.circuits[circuit_name]['bestrace'][2], True, (0,0,0))
            self.fasttest_lap = self.font.render(self.circuits[circuit_name]['fasttestlap'][0] \
                                                + ':' + self.circuits[circuit_name]['fasttestlap'][1] \
                                                + ':' + self.circuits[circuit_name]['fasttestlap'][2], True, (0,0,0))
        #Si el circuito que se pasa no esta en el mapa, motramos que no están disponible sus tiempos
        else:
            self.best_race = self.font.render('No Disponible', True, (0,0,0))
            self.fasttest_lap = self.font.render('No Disponible', True, (0,0,0))
        
        #Asignamos las posiciones para cada una de las superficie y queden todas alineadas
        self.best_race_position = (self.best_text_position[0], self.best_text.get_height() + self.best_text_position[1])
        self.fasttest_text_position = (self.best_text_position[0], self.best_race.get_height() + self.best_race_position[1])
        self.fasttest_lap_position = (self.best_text_position[0], self.fasttest_text.get_height() + self.fasttest_text_position[1])
        
    def draw(self, screen):
        '''
        @brief Dibuja los tiempos en pantalla
        
        @param screen Superficie destino
        '''
        #Dibujamos cada una de las superficies con sus posiciones obtenidas
        screen.blit(self.best_text, self.best_text_position)
        screen.blit(self.best_race, self.best_race_position)
        screen.blit(self.fasttest_text, self.fasttest_text_position)
        screen.blit(self.fasttest_lap, self.fasttest_lap_position)
    
    def get_best_time(self, circuit_name):
        pass
    
    def get_fattest_lap(self, circuit_name):
        pass

class CircuitMenu(basicmenu.BasicMenu):
    '''
    @brief Clase encargada de representar el menú de selección de circuito, se usará
    la misma clase tanto para carrera rapida como para el modo contrarreloj
    '''
    def __init__(self, game, path_xml):
        '''
        @brief Constructor.
        
        @param game Referencia a Game
        @param path_xml Archivo xml con la configuración del menú
        '''
        basicmenu.BasicMenu.__init__(self, game)
        
        #Cambiamos el título de la ventana
        pygame.display.set_caption("Zycars: Circuitos")

        #Parseamos la información básica del circuito(botones, imagenes...)
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        self.parser_basic_info(parse)
        
        #Mapa que contendrá los botones de cada capa
        self.buttons_layers = {}
        
        #Mapa que contendrá la imagen de un circuito dado la capa y el nombre del circuito
        self.images_circuits = {}
        
        #Mapa que contendrá los primeros circuitos de cada campeonato
        self.first_circuit = {}
        
        #Mapa con los archivos xml
        self.circuit_files = {}
        
        #Obtenemos los parametros para la posición del título de los circuitos
        self.centerx_name = 400
        self.y_name = 300
        self.rect_name = None
        self.actual_name = None
        
        self.font = resource.get_font('cheesebu', 30)
        
        #Booleanos auxiliares
        first = True
        new_layer = True
        first_layer = True
        
        #Texto a mostrar cuando no hay circuito disponible
        font = resource.get_font('cheesebu', 30)
        message = font.render('Lo sentimos, Circuito no disponible', True, (0,0,0))
        
        #Obtenemos la posicion de la imagen que representará al circuito
        image_pos = parse.getElementsByTagName('circuit_position')[0]
        x = int(image_pos.getAttribute('x'))
        y = int(image_pos.getAttribute('y'))
        self.circuit_position = (x, y)
        
        self.times = None
        
        if Config().get_mode() == TIMED:
            #Obtenemos la posición del marcador de los tiempos
            time_pos = parse.getElementsByTagName('times_position')[0]
            x = int(time_pos.getAttribute('x'))
            y = int(time_pos.getAttribute('y'))
            #Creamos el marcador de los tiempos
            self.times = Times(x, y, 'times.xml')
        
        #Recorremos las capas a mostrar, de los distintos campeonatos
        for element in parse.getElementsByTagName('layer'):
            
            #Obtenemos el nombre de la capa, debe coincidir con el del botón
            #Que hace referencia a ella
            name_layer = element.getAttribute('name')
            
            #Creamos una lista para todos los botones de esa capa
            self.buttons_layers[name_layer] = []
            
            #Creamos un mapa para cada una de las capas
            self.images_circuits[name_layer] = {}
            self.circuit_files[name_layer] = {}
            
            #Si es la primera capa que parseamos, nos quedamos con ella, para
            #mostrarla la primera
            if first_layer:
                self.actual_layer = name_layer
                first_layer = False
            
            #Obtenemos los botones de cada una de las capas
            for option in element.getElementsByTagName('button'):
                
                #Archivo xml con la configuración del botón
                xml_file = str(option.getAttribute('xml_file'))
                
                #Fuente y texto que apareceran en el boton
                font_code = str(option.getAttribute('font'))
                text = option.getAttribute('text')
                
                #Posición del botón
                x = int(option.getAttribute('x'))
                y = int(option.getAttribute('y'))
                show_text = True
                
                #Miramos si se indica si se debe mostrar o no el texto en el botón
                if option.hasAttribute('show_text'):
                    show_text = option.getAttribute('show_text')
                    show_text = button.strTobool(show_text)      
                    
                #Obtenemos el tipo de boton
                if option.hasAttribute('type'):
                    type_button = str(option.getAttribute('type'))
                
                #Según el tipo de boton obtendremos un boton u otro
                if type_button == 'normal':
                    
                    #Si es un botón normal sin imagen significa que el circuito no está disponible.
                    aux_button = button.Button(self, xml_file, text, x, y, font_code, show_text, True)
                    
                    #Si que le asociamos como imagen el mensaje de que no está disponible
                    self.images_circuits[name_layer][text] = message

                elif type_button == 'image_button':
                    
                    #Obtenemos la información necesaria para ImageButton
                    image_code = str(option.getAttribute('image'))
                    image_x = int(option.getAttribute('image_x'))
                    image_y = int(option.getAttribute('image_y'))
                    
                    aux_button = imagebutton.ImageButton(self, xml_file, text, x, y, font_code, image_code, image_x, image_y, show_text, True)

                    #Obtenemos el archivo de configuración del circuito
                    circuit_file = str(option.getAttribute('circuit_file'))
                    
                    #Obtenemos la imagen que representará al circuito
                    image_circuit = str(option.getAttribute('image_circuit'))
                    
                    #Introducimos la imagen en el doble diccionario
                    self.images_circuits[name_layer][text] = resource.get_image(image_circuit)
                    #Hacemos lo mismo con el archivo xml
                    self.circuit_files[name_layer][text] = circuit_file
                
                #Nos quedamos con el primer circuito de la capa actual
                if first:
                    self.actual_circuit = text
                    
                    #También renderizamos el título del circuito
                    self.actual_name = self.font.render(text, True, (255, 255, 255))
                    self.rect_name = self.actual_name.get_rect()
                    self.rect_name.y = self.y_name
                    self.rect_name.centerx = self.centerx_name
                    
                    if self.times:
                        #Nos quedamos en un principio con los tiempos del primer circuito
                        self.times.update(text)
                    
                    #Indicamos que el siguiente no será el primero
                    first = False
                
                #Nos quedamos con el primer circuito de cada una de las capas
                #para mostrarlos cuando cambiemos de capa
                if new_layer:
                    self.first_circuit[name_layer] = text
                    new_layer = False

                #Por último añadiemos el botón a la lista de botones por capa
                self.buttons_layers[name_layer].append(aux_button)
            
            new_layer = True
                
    def update(self):
        '''
        @brief Método que actualiza lógicamente el menú
        Solo actualiza los elementos de la capa actual
        '''
        self.actual_option = None
        #Actualizamos cada uno de los botones, por defecto del menú
        for button in self.buttons:
            button.update()
            #Si el cursor está sobre alguno de los botones
            if button.get_selected():
                #Obtenemos su opción
                self.actual_option = button.get_option()
        
        #Actualizamos los botones de las capas
        for button in self.buttons_layers[self.actual_layer]:
            button.update()
            if button.get_selected():
                self.actual_option = button.get_option()
        
        #Si hay algun botón seleccionado
        if self.actual_option:
            #Cambiamos el cursor
            self.cursor.over()
                
        #Si no, lo dejamos normal
        else:
            self.cursor.normal()
        
        #Actualizamos el cursor
        self.cursor.update()
                    
    def draw(self, screen):
        '''
        @brief Método que dibuja todo los componentes del menú en pantalla.
        Solo dibuja los elementos de la capa actual
        
        @param screen Supeficie destino
        '''
        #Dibujamos los elementos basicos del juego
        self.draw_basic_elements(screen) 
        
        #Dibujamos los botones de la capa actual
        for button in self.buttons_layers[self.actual_layer]:
            button.draw(screen)
        
        #Dibujamos la imagen del circuito de la imagen actual
        screen.blit(self.images_circuits[self.actual_layer][self.actual_circuit], self.circuit_position)
        screen.blit(self.actual_name, self.rect_name)
        
        if self.times:
            #Dibujamos los tiempos del circuito actual
            self.times.draw(screen)
        
        #Por ultimo dibujamos el cursor 
        self.cursor.draw(screen)
        
    def treat_option(self, option):
        '''
        @brief Método que es llamado por los botones pertenecientes al menú cuando
        se pulsa sobre alguno de ellos
        
        @param option La opción del boton que se acaba de pulsar
        '''
        if option == "Aceptar":
            print "Aceptar"
            #Si hemo pulsado aceptar y el circuito está disponible.
            if self.actual_circuit != 'No Disponible':
                Config().set_circuit(self.circuit_files[self.actual_layer][self.actual_circuit])
                print 'Ha elegido ', self.circuit_files[self.actual_layer][self.actual_circuit]
                Config().start_game(self.game)
        #Si pulsamos cancelar, volvemos al menú anterior
        elif option == 'Cancelar':
            print "Cancelar"
            self.game.change_state(charactermenu.CharacterMenu(self.game, 'menu/charactermenu.xml'))
        
        #Si pulsamos sobre alguna de los campeonatos opcionales, debemos cambiar la capa
        elif option == "Copa Chancla" or option == 'Copa Arbusto' or option == 'Copa Rodillo':
            print option
            #Si la capa pulsada es distinta que la actual
            if self.actual_layer != option:
                #Cambiamos la imagen del circuito actual, a el primero de la capa
                self.actual_circuit = self.first_circuit[option]
                
                if self.times:
                    #Actualizamos los tiempos del primer circuito del camponato al que pasamos
                    self.times.update(self.actual_circuit)
                
                #Renderizamos el nombre del nuevo circuito y asignamos posición
                self.actual_name = self.font.render(self.first_circuit[option], True, (255, 255, 255))
                self.rect_name = self.actual_name.get_rect()
                self.rect_name.y = self.y_name
                self.rect_name.centerx = self.centerx_name
                
            #Situamos la nueva capa
            self.actual_layer = option
            
        #Si no se a cumplido ninguna anterior, es que  hemos pulsado sobre un botom de circuito
        else:
            print option
            #Si la opción es distinta que la ya seleccionada
            if self.actual_circuit != option:
                #Indicamos el nuevo circuito
                self.actual_circuit = option
                
                if self.times:
                    #Actualizamos los tiempos el circuito actual
                    self.times.update(option)
                
                #Renderizamos el nombre del nuevo circuito y asignamos posición
                self.actual_name = self.font.render(option, True, (255, 255, 255))
                self.rect_name = self.actual_name.get_rect()
                self.rect_name.y = self.y_name
                self.rect_name.centerx = self.centerx_name

