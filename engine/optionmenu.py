#-*- encoding: utf-8 -*-

import basicmenu
import data
import resource
import button
import imagebutton
import slider
import mainmenu
import xml.dom.minidom
import pygame
import checkbox

class OptionMenu(basicmenu.BasicMenu):
    '''
    @brief Clase que representa el Menú de opciones
    '''
    def __init__(self, game, path_xml):
        '''
        @brief Constructor.
        
        @param game Referencia a game
        @param path_xml Ruta del archivo xml con la configuración
        '''
        basicmenu.BasicMenu.__init__(self, game)
        
        #Cambiamos el título de la ventana
        pygame.display.set_caption("Zycars: Opciones")

        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        #Obtenemos los elementos básicos del menú
        self.parser_basic_info(parse)
        
        #Declaramos distintos atributos de la clase
        self.text_layers = {}
        self.elements_layers = {}
        self.actual_layer = None
        
        #Recorremos las distintas capas que tendrá el menú
        for element in parse.getElementsByTagName('layer'):
            
            #Obtenemos el nombre de la capa que la indetificará
            name_layer = str(element.getAttribute('name'))
            self.text_layers[name_layer] = []
            self.elements_layers[name_layer] = []
            
            #Fuente que se usará y tamaño de esta
            font_code = str(element.getAttribute('font_code'))
            size = int(element.getAttribute('size'))
            font_temp = resource.get_font(font_code, size)
            
            #Obtenemos los distintos texto que aparecerán por capa
            for text in element.getElementsByTagName('text'):
                
                #Obtenemos texto y posición
                value = text.getAttribute('value')
                posx = int(text.getAttribute('x'))
                posy = int(text.getAttribute('y'))
                
                #Renderizamos
                text_render = font_temp.render(value, True, (0,0,0))
                text_render_rect = text_render.get_rect()
                text_render_rect.x = posx
                text_render_rect.y = posy
                
                #Insertamos en la lista de textos por capa
                self.text_layers[name_layer].append((text_render, text_render_rect))
            
            #Obtenemos los distintos objetos que tendrán cada capa
            #En primer lugar obtenemos los slider
            for slider_option in element.getElementsByTagName('slider'):
                
                #Obtenemos archivo de configuración
                xml_path = str(slider_option.getAttribute('xml_file'))
                
                #Posición
                x = int(slider_option.getAttribute('x'))
                y = int(slider_option.getAttribute('y'))
                
                #Obtenemos el slider
                new_slider = slider.Slider(xml_path, 50, 100, x, y)
                
                #Lo introducimos en la lista de sliders
                self.elements_layers[name_layer].append(new_slider)
            
            for check_box in element.getElementsByTagName('checkbox'):
                
                xml_file = str(check_box.getAttribute('xml_file'))
                font_code = str(check_box.getAttribute('font'))
                show_text = False
                text = check_box.getAttribute('text')
                image_code = str(check_box.getAttribute('image_code'))
                image_x = int(check_box.getAttribute('image_x'))
                image_y = int(check_box.getAttribute('image_y'))
                x = int(check_box.getAttribute('x'))
                y = int(check_box.getAttribute('y'))
                
                new_checkbox = checkbox.CheckBox(xml_file, text, x, y, font_code, image_code, image_x, image_y, show_text, True)
                self.elements_layers[name_layer].append(new_checkbox)
        
        #La capa inicial será la de sonido
        self.actual_layer = "Sonido"
                            
    def update(self):
        '''
        @brief Método encargado de actualizar todos los elementos del menú
        '''
        
        #Actualizamos cada uno de los botones
        self.actual_option = None
        for button in self.buttons:
            button.update()
            #So el cursor está sobre alguno de los botones
            if button.get_selected():
                #Obtenemos su opción
                self.actual_option = button.get_option()
        
        #Si hay alguna opción
        if self.actual_option:
            
            #Cambiamos el cursor
            self.cursor.over()
            
            #Si se ha pulsado el raton, tratamos la opción actual
            if pygame.mouse.get_pressed()[0]:
                self.treat_option()
                
        #Si no, lo dejamos normal
        else:
            self.cursor.normal()
        
        #Actualizamos todos los elementos de la capa actual
        for element in self.elements_layers[self.actual_layer]:
            element.update()
        
        #Actualizamos el cursor
        self.cursor.update()
                    
    def draw(self, screen):
        '''
        @brief Método que dibuja todos los elementos del menú en pantalla
        
        @param screen Superficie destino
        '''
        
        #Dibujamos los elementos basicos del juego
        self.draw_basic_elements(screen)
        
        #Dibujamos los texto de la capa actual
        for element in self.text_layers[self.actual_layer]:
            screen.blit(element[0], element[1])

        #Dibujamos los elementos de la capa actual
        for element in self.elements_layers[self.actual_layer]:
            element.draw(screen)
        
        #Dibujamos el cursor
        self.cursor.draw(screen)
        
    def treat_option(self):
        '''
        @brief Función encargada de tratar la opción actual del menú seleccionada
        '''
        if self.actual_option == "Aceptar":
            print "Aceptar"
            self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))
            
        elif self.actual_option == "Cancelar":
            print "Cancelar"
            self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))

        elif self.actual_option == "Sonido":
            self.actual_layer = "Sonido"
            
        elif self.actual_option == "Pantalla":
            self.actual_layer = "Pantalla"
            
        elif self.actual_option == "Controles":
            self.actual_layer = "Controles"
