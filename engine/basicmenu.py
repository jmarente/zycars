#-*- encoding: utf-8 -*-

import state
import cursor
import data
import resource
import button
import imagebutton
import xml.dom.minidom
import pygame

class BasicMenu(state.State):
    '''
    @brief Clase que abstrae los elementos basicos de un Menú
    '''
    def __init__(self, game):
        '''
        @brief Constructor
        
        @param game Referencia a game
        '''
        state.State.__init__(self, game)
        
        #Definimos los atributos 
        self.buttons = []
        self.background = None
        self.cursor = None
        self.title = None
        self.images = []
        self.actual_option = None
        
    def update(self):
        '''
        @brief Método que actualizara al menú, debe ser implementado por sus descendientes
        '''
        pass
        
    def draw(self):
        '''
        @brief Método que dibujara el menú, debe ser implementado por sus descendientes
        '''
        pass
        
    def draw_basic_elements(self, screen):
        '''
        @brief Método que dibujara los elementos basico en pantalla
        
        @param screen Superficie destino 
        '''
        #Dibujamos el fondo
        screen.blit(self.background, (0, 0))
        
        #Dibujamos el titulo
        screen.blit(self.title, self.title_rect)
        
        #Dibujamos las imagenes
        for image in self.images:
            screen.blit(image[1], image[2])
        
        #Dibujamos los botones
        for button in self.buttons:
            button.draw(screen)
    
    def parser_basic_info(self, parse):
        '''
        @brief Método que parsea los componentes básicos del menú
        
        @param parse Archivo xml parsea com xml.dom.minidom
        '''
        parent = parse.firstChild
        
        #Obtenemos la imagen de fondo
        image_code = str(parent.getAttribute('background'))
        self.background = resource.get_image(image_code)
        
        #Obtenemos el cursor del menú
        cursor_xml = str(parent.getAttribute('cursor'))
        self.cursor = cursor.Cursor(data.get_path_xml(cursor_xml))
        
        #Obtenemos el titulo del menú
        for element in parse.getElementsByTagName('title'):
            #Obtenemos tamaño y fuente
            font_code = str(element.getAttribute('font'))
            font_size = int(element.getAttribute('size'))
            self.font = resource.get_font(font_code, font_size)
            text = element.getAttribute('text')
            
            #Colores
            r = int(element.getAttribute('r'))
            g = int(element.getAttribute('g'))
            b = int(element.getAttribute('b'))
            color = (r, g, b)
            
            #Renderizamos
            self.title = self.font.render(text, True, color)
            
            #Obtenemos la posición
            self.title_rect = self.title.get_rect()
            self.title_rect.x = int(element.getAttribute('x'))
            self.title_rect.y = int(element.getAttribute('y'))
        
        #Obtenemos todas las imagenes que aparecen
        for element in parse.getElementsByTagName('image'):
            
            #Obtenemos la imagen
            image_code = str(element.getAttribute('image_code'))
            image = resource.get_image(image_code)
            
            #Si la imagen tiene el atributo scale
            if element.hasAttribute('scale'):
                #Escalamos la imagen
                scale = float(element.getAttribute('scale'))
                if scale != 1:
                    temporal = image.copy()
                    image = pygame.transform.rotozoom(temporal, 0, scale)
            
            #Obtenemos la posición de la imagen
            rect = image.get_rect()
            rect.x = int(element.getAttribute('x'))
            rect.y = int(element.getAttribute('y'))
            
            #La incluimos en la lista de imagenes
            self.images.append((image_code, image, rect))
        
        #Obtenemos los distintos botones del menú
        for element in parse.getElementsByTagName('option'):
            
            #Ruta del archivo xml con la configuración
            xml_file = str(element.getAttribute('xml_file'))
            
            #Fuente y texto que apareceran en el boton
            font_code = str(element.getAttribute('font'))
            text = element.getAttribute('text')
            
            
            x = int(element.getAttribute('x'))
            y = int(element.getAttribute('y'))
            show_text = True
            
            #Miramos si se indica si se debe mostrar o no el texto en el botón
            if element.hasAttribute('show_text'):
                show_text = element.getAttribute('show_text')
                show_text = button.strTobool(show_text)
            
            type_button = 'normal'
            
            #Obtenemos el tipo de boton
            if element.hasAttribute('type'):
                type_button = str(element.getAttribute('type'))
            
            image_button = None
            
            #Según el tipo de boton obtendremos un boton u otro
            if type_button == 'normal':
                aux_button = button.Button(self, xml_file, text, x, y, font_code, show_text, True)
            elif type_button == 'image_button':
                image_code = str(element.getAttribute('image'))
                image_x = int(element.getAttribute('image_x'))
                image_y = int(element.getAttribute('image_y'))
                aux_button = imagebutton.ImageButton(self, xml_file, text, x, y, font_code, image_code, image_x, image_y, show_text, True)
            
            #Lo añadimos a la lista de botones
            self.buttons.append(aux_button)
            
    def treat_option(self, option):
        '''
        @brief Método que tratará el comportamiento del menu según las distintas opciones seleciconadas
        Se debe implementar en los descendientes de BasicMenu
        '''
        #raise NotImplemented('Esta función debe ser implementada por todos los descendientes de BasicMenu')
        pass
