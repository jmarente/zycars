#-*- encoding: utf-8 -*-

#import gamecontrol
import data
import resource
import checkpoint
import xml.dom.minidom
import sys
import pygame
import math

#Distintos tipos de tiles
PASSABLE, NOPASSABLE, LAG = range(3)

class Tile:
    '''
    Clase que guarda la informacion de un tile del escenario
    '''
    def __init__(self, frame = 0, type = PASSABLE):
        self.type = type
        self.frame = frame

class Circuit:
    '''
    Clase que maneja los circuitos del juego
    '''
    def __init__(self, game_control, xml_path):
        '''
        Game_control objeto GameControl con el que se asocia.
        Xml_path ruta del archivo del circuito en cuestión.
        
        Parseamos el archivo xml y cargamos las distintas propiedades
        de los tiles, así como la posicion de estos, su capa y el tipo.
        '''
        self.game_control = game_control
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_path, False))
        
        #Parseamos los distintos componentes necesarias para el circuito.
        for element in parser.getElementsByTagName('map'):
            self.width = int(element.getAttribute('width'))
            self.height = int(element.getAttribute('height'))
            self.tile_width = int(element.getAttribute('tilewidth'))
            self.tile_height = int(element.getAttribute('tileheight'))
        
        print "Width: " + str(self.width) + " Height: " + str(self.height) \
        + " tile_width: " + str(self.tile_width) + ' tile_height: ' + str(self.tile_height)
            
        image_name = None
        for element in parser.getElementsByTagName('image'):
            image_name = str(element.getAttribute('source'))
            
        tileset_width = 1
        tileset_height = 1
        collision_map_name = None
        self.circuit_width = 0
        self.elements_map = {}
        self.car_angle = 0
        
        #Parseamos las distintas propiedades editadas para el mapa, como
        #el número de tiles en el ancho del tileset y en el alto,
        #así como el mapa de colisiones correspondiente
        for element in parser.getElementsByTagName('property'):
            name = element.getAttribute('name')
            if name == 'tileset_ancho':
                tileset_width = int(element.getAttribute('value'))
            elif name == 'tileset_alto':
                tileset_height = int(element.getAttribute('value'))
            elif name == 'collision_map':
                collision_map_name = str(element.getAttribute('value'))
            elif name == 'ancho_pista':
                self.circuit_width = int(element.getAttribute('value'))
            elif name == 'checkpointH':
                frame = int(element.getAttribute('value'))
                self.elements_map[frame] = name
            elif name == 'checkpointV':
                frame = int(element.getAttribute('value'))
                self.elements_map[frame] = name            
            elif name == 'goalV':
                frame = int(element.getAttribute('value'))
                self.elements_map[frame] = name
            elif name == 'goalH':
                frame = int(element.getAttribute('value'))
                self.elements_map[frame] = name
            elif name == 'grado_coche':
                self.car_angle = int(element.getAttribute('value'))


                
        print "Tileset_height: " + str(tileset_height) + ' Tileset_width: ' + str(tileset_width)
        
        self.tileset = data.load_sprite(image_name, tileset_height, tileset_width)
        collision_map = data.load_image(collision_map_name)#, tileset_height, tileset_width)

        #Suponiendo que 4 sera el numero de capas que tendrá el mapa
        #Self.map sera la matriz logica que indicara donse se posiciona
        #cada tile y de que tipo son.
        self.map = range(4) 
        #Por cada elemento:
        for n in range(4):
            self.map[n] = range(self.height) #reservamos para el alto.
            for m in range(self.height):
                self.map[n][m] = range(self.width) #y para el ancho.
                for o in range(self.width):
                    self.map[n][m][o] = Tile()

                    
        #Cargamos la imagen con los distinto tipos de tiles
        tile_types = data.load_image('tile_types.png')
        
        #Obtenemos un array de pixeles tanto de los distintos tipos de tiles.
        pxarray_tile_types = pygame.PixelArray(tile_types)
        #Como del mapa de colisiones, para poder hacer comprobaciones
        pxarray = pygame.PixelArray(collision_map)

        num_layer = 0
        num_row = 0
        num_column = 0
        n = 0
        frame = None
        for layer in parser.getElementsByTagName('layer'):
            for tile in layer.getElementsByTagName('tile'):
                
                num_row = int(n / self.width)
                num_column = (n % self.width) % self.width
                frame = int(tile.getAttribute('gid'))
                
                self.map[num_layer][num_row][num_column].frame = frame
                
                if frame == 0:
                    self.map[num_layer][num_row][num_column].type = PASSABLE
                else:
                    p_x = (((frame - 1) % tileset_width) % tileset_width) * self.tile_height;
                    p_y = ((frame - 1) / tileset_width) * self.tile_width
                    
                    if pxarray[p_x][p_y] == pxarray_tile_types[0]:
                        self.map[num_layer][num_row][num_column].type = PASSABLE
                        #print "El tile: " + str(self.map[num_layer][num_row][num_column].frame - 1) + " es pasable."
                        
                    elif pxarray[p_x][p_y] == pxarray_tile_types[1]:
                        self.map[num_layer][num_row][num_column].type = NOPASSABLE
                        #print "El tile: " + str(self.map[num_layer][num_row][num_column].frame - 1) + " NO es pasable."
                        
                    elif pxarray[p_x][p_y] == pxarray_tile_types[2]:
                        self.map[num_layer][num_row][num_column].type = LAG
                        
                    else:
                        self.map[num_layer][num_row][num_column].type = PASSABLE
                        
                n += 1
            #print n
            num_layer += 1
            n = 0
        
        self.x = 0
        self.y = 1
        #self.y = self.height * self.tile_height - pygame.display.get_surface().get_height()
        #y = alto_ * tile_alto_ - juego_->univ()->pantalla_alto();
        
        print str(num_layer)
        self.load_elements()            
        
    def draw(self, screen, layer):
        '''
        Screen superficie destino.
        Layer capa del mapa a dibujar.
        
        Dibuja la capa indicada sobre la superficie.
        '''                
        if layer < 0 or layer > 3:
            print "Error: nÃºmero de capa incorrecto" 
            sys.exit(1)
            
        screen_w = screen.get_width()
        screen_h = screen.get_height()
        
        #Posiciones
        lx = int(self.x / self.tile_width)
        ly = int(self.y / self.tile_height)
        
        #Numero total de bloques que tenemos que dibujar
        num_blocks_x = int(screen_w / self.tile_width)
        num_blocks_y = int(screen_h / self.tile_height)
        '''num_blocks_x = self.width
        num_blocks_y = self.height'''
        
        #Si aun sobra pixeles, si el modulo es 0 no es necesario dibujar mas
        margin_x = self.x % self.tile_width
        margin_y = self.y % self.tile_height
        
        #AÃ±adimos un bloque mas de relleno
        if margin_x:
            num_blocks_x += 1
            #print "Entra x"
        if margin_y:
            # or ((self.y + screen_h) < self.height * self.tile_height):
            num_blocks_y += 1
            #print "Entra y"
                    
        #print num_blocks_x
        #print num_blocks_y
        
        row = 0
        column = 0
        
        suma = 0
        suma_x = 0
        
        if self.y >= self.height * self.tile_height - pygame.display.get_surface().get_height() - self.tile_height or self.y == 0:
            suma = 0
        else:
            suma = 1

        if self.x >= self.width * self.tile_width - pygame.display.get_surface().get_width() - self.tile_width:
            suma_x = 0
        else:
            suma_x = 1
        
        for row in range(num_blocks_y + suma):
            for column in range(num_blocks_x + suma_x):
                frame = self.map[layer][row + ly][column + lx].frame - 1
                if frame > -1:
                    pos_x = column * self.tile_width - margin_x
                    pos_y = row * self.tile_width - margin_y
                    screen.blit(self.tileset[frame], (pos_x, pos_y))
            #print row
            #print num_blocks_y
        
    def move(self, x, y):
        '''
        x nueva coordenada en el eje x en píxeles.
        y nueva coordenada en el eje y en píxeles.
        '''
        self.x = x
        
        if y == 0:
            self.y = 1
        else:
            self.y = y
         
    def load_elements(self):
        '''
        Función encargada de cargar los objetos del juego.
        '''
        cp = None
        for i in range(0, self.height):
            for j in range(0, self.width):
                frame = self.map[3][i][j].frame
                
                if self.elements_map.has_key(frame):
                     x = j * self.tile_height
                     y = i * self.tile_width
                                          
                     if self.elements_map[frame] == 'checkpointH':
                        #cp = checkpoint.CheckPoint(self.game_control, x, y, self.tile_width * self.circuit_width, self.tile_height)
                        cp = checkpoint.CheckPoint(self.game_control, x, y, self.tile_width * self.circuit_width, 2)
                        self.game_control.add_checkpoint(cp)
                    
                     elif self.elements_map[frame] == 'checkpointV':
                        #cp = checkpoint.CheckPoint(self.game_control, x, y, self.tile_width, self.tile_height * self.circuit_width)
                        cp = checkpoint.CheckPoint(self.game_control, x, y, 2, self.tile_height * self.circuit_width)
                        self.game_control.add_checkpoint(cp)
                        
                     elif self.elements_map[frame] == 'goalV':
                        #cp = checkpoint.CheckPoint(self.game_control, x, y, self.tile_width, self.tile_height * self.circuit_width)
                        cp = checkpoint.CheckPoint(self.game_control, x, y, 2, self.tile_height * self.circuit_width)
                        self.game_control.set_goal(cp)
                        self.game_control.set_start(self, x, y, 'goal', 'vertical', self.car_angle)

                     elif self.elements_map[frame] == 'goalH':
                        #cp = checkpoint.CheckPoint(self.game_control, x, y, self.tile_width, self.tile_height * self.circuit_width)
                        cp = checkpoint.CheckPoint(self.game_control, x, y, self.tile_width * self.circuit_width, 2)
                        self.game_control.set_goal(cp)
                        self.game_control.set_start(self, x, y, 'goal', 'horizontal', self.car_angle)
        
    def get_tile(self, layer, x, y):
        '''
        x Coordenada del eje x del tile a consultar.
        y Coordenada del eje y del tile a consultar.
        
        Devuelve el Tile() de esa posición.
        '''
        #Si el tile que se pide no esta en la pantalla, ni el tileset, 
        #suponemos que este es pasable.
        if x < 0 or x > self.width or y < 0 or y > self.height:
            print "WARNING: tile fuera de rango"
            tile = Tile()
            return tile
            
        #Dado que despues de añadir las capas a self.map, añadimos el 
        #tamaño del ancho se entiende [y][x]
        return self.map[layer][y][x]
        
    def get_tile_height(self):
        '''
        Devuelve el alto de un tile en píxeles
        '''
        return self.tile_height 
        
    def get_tile_width(self):
        '''
        Devuelve el ancho de un tile en píxeles
        '''
        return self.tile_width 
        
    def get_width(self):
        '''
        Devuelve el ancho del circuito en tiles
        '''
        return self.width 
        
    def get_height(self):
        '''
        Devuelve el alto de circuito en tiles
        '''
        return self.height
        
    def get_x(self):
        '''
        Coordenada actual en x del circuito en píxeles
        '''
        return self.x
        
    def get_y(self):
        '''
        Coordenada actual en y del circuito en píxeles 
        '''
        return self.y
    
    def get_real_width(self):
        return self.width * self.tile_width
    
    def get_real_height(self):
        return self.height * self.tile_height
    
    def get_circuit_width(self):
        return self.circuit_width
