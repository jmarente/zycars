#-*- encoding: utf-8 -*-

#import gamecontrol
import data
import resource
import xml.dom.minidom
import sys
import pygame

PASSABLE, NOPASSABLE, LAG = range(3)

class Tile:
    def __init__(self, frame = 0, type = PASSABLE):
        self.type = type
        self.frame = frame

class Circuit:
    def __init__(self, game_control, xml_path):
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
        
        #Parseamos las distintas propiedades editadas para el mapa, como
        #el número de tiles en el ancho del tileset y en el alto,
        #así como el mapa de colisiones correspondiente
        for element in parser.getElementsByTagName('property'):
            name = element.getAttribute('name')
            if name == 'tileset_ancho':
                tileset_width = int(element.getAttribute('value'))
            elif name == 'tileset_alto':
                tileset_height = int(element.getAttribute('value'))
                '''elif name == 'collision_map':
                collision_map_name = str(element.getAttribute('value'))'''
                
        print "Tileset_height: " + str(tileset_height) + ' Tileset_width: ' + str(tileset_width)
        
        self.tileset = data.load_sprite(image_name, tileset_width, tileset_height, )
        #self.collision_map = data.load_image(collision_map_name)#, tileset_height, tileset_width)

        #Suponiendo que 4 sera el numero de capas que tendrá el mapa
        #Self.map sera la matriz logica que indicara donse se posiciona
        #cada tile y de que tipo son
        self.map = range(4) 
        #Por cada elemento
        for n in range(4):
            self.map[n] = range(self.height) #reservamos para el alto
            for m in range(self.height):
                self.map[n][m] = range(self.width) #y para el ancho
                for o in range(self.width):
                    self.map[n][m][o] = Tile()

                    
        #Cargamos la imagen con los distinto tipos de tiles
        '''tile_types = data.get_image('tile_types.png')
        
        #Obtenemos un array de pixeles tanto de los distintos tipos de tiles.
        pxarray_tile_types = pygame.PixelArray(tile_types)
        #Como del mapa de colisiones, para poder hacer comprobaciones
        pxarray = pygame.PixelArray(collision_map)'''

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
                
                '''if frame == 0:
                    self.map[num_layer][num_row][num_column].type = PASSABLE
                else:
                    p_x = (((frame - 1) % tileset_width) % tileset_width) * self.tile_height;
                    p_y = ((frame - 1) / tileset_width) * self.tile_width
                    
                    if pxarray[p_x][p_y] == pxarray_tile_types[0]:
                        self.map[num_layer][num_row][num_column].type = PASSABLE
                    elif pxarray[p_x][p_y] == pxarray_tile_types[1]:
                        self.map[num_layer][num_row][num_column].type = NOPASSABLE
                    elif pxarray[p_x][p_y] == pxarray_tile_types[2]:
                        self.map[num_layer][num_row][num_column].type = LAG
                    else:
                        self.map[num_layer][num_row][num_column].type = PASSABLE'''
                                        
                n += 1
            print n
            num_layer += 1
            n = 0
        
        self.x = 0
        self.y = 0
        #y = alto_ * tile_alto_ - juego_->univ()->pantalla_alto();
        
        print str(num_layer)
        self.load_actors()            
        
    def draw(self, screen, layer):
                
        if layer < 0 or layer > 3:
            print "Error: número de capa incorrecto" 
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
        
        #Añadimos un bloque mas de relleno
        if margin_x:
            num_blocks_x += 1
            #print "Entra x"
        if margin_y:
            # or ((self.y + screen_h) < self.height * self.tile_height):
            num_blocks_y += 1
            #print "Entra y"
            
        print num_blocks_x
        print num_blocks_y
            
        for row in range(num_blocks_y):
            for column in range(num_blocks_x):
                frame = self.map[layer][row + ly][column + lx].frame - 1
                if frame > -1:
                    pos_x = column * self.tile_width - margin_x
                    pos_y = row * self.tile_width - margin_y
                    screen.blit(self.tileset[frame], (pos_x, pos_y))
        
    def move(self, x, y):
        self.x = x
        self.y = y
         
    def load_actors(self):
        pass
        
    def get_tile(self, layer, x, y):
        
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
        return self.tile_height 
        
    def get_tile_width(self):
        return self.tile_width 
        
    def get_width(self):
        return self.width 
        
    def get_height(self):
        return self.height
        
    def get_x(self):
        return self.x
        
    def get_y(self):
        return self.y
