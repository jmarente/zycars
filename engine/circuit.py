#-*- encoding: utf-8 -*-

#import gamecontrol
import data
import checkpoint
import itembox
import astar
import xml.dom.minidom
import sys
import pygame
import gameanimation

#Distintos tipos de tiles
PASSABLE, NOPASSABLE, LAG, HOLE = range(4)

class Tile:
    '''
    @brief Clase que guarda la informacion básica de un tile del escenario
    '''
    def __init__(self, frame = 0, type = PASSABLE):
        '''
        @brief Constructor
        
        @param frame Número del frame del tile
        @param type Indica de que tipo es el tile
        '''
        self.type = type
        self.frame = frame

class Circuit:
    '''
    @brief Clase encargada de cargar los circuitos
    '''
    def __init__(self, game_control, xml_path):
        '''
        @brief Constructor
        
        @param game_control Referencia a GameControl.
        @param xml_path Ruta del archivo del circuito.
        '''
        self.game_control = game_control
        
        parser = xml.dom.minidom.parse(data.get_path_xml(xml_path, False))
        
        #Parseamos los distintos componentes necesarios para el circuito.
        for element in parser.getElementsByTagName('map'):
            self.width = int(element.getAttribute('width'))
            self.height = int(element.getAttribute('height'))
            self.tile_width = int(element.getAttribute('tilewidth'))
            self.tile_height = int(element.getAttribute('tileheight'))
        
        
        #print "Width: " + str(self.width) + " Height: " + str(self.height) \
        #+ " tile_width: " + str(self.tile_width) + ' tile_height: ' + str(self.tile_height)
         
        #Obtenemos el nombre de la imagen con el tileset del circuito
        image_name = None
        for element in parser.getElementsByTagName('image'):
            image_name = str(element.getAttribute('source'))
        
        #Variables auxiliares
        tileset_width = 1
        tileset_height = 1
        collision_map_name = None
        
        self.circuit_width = 0
        self.goal_width = 0
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
                frame = int(element.getAttribute('value'))
                self.elements_map[frame] = name 
            elif name == 'ancho_meta':
                self.goal_width = int(element.getAttribute('value'))
            elif name == 'grado_coche':
                self.car_angle = int(element.getAttribute('value'))
            elif name == 'item_box':
                frame = int(element.getAttribute('value'))
                self.elements_map[frame] = name
                
        #print "Tileset_height: " + str(tileset_height) + ' Tileset_width: ' + str(tileset_width)
        
        #Cargamos el tileset del circuito
        self.tileset = data.load_sprite(image_name, tileset_height, tileset_width)
        
        #Cargamos el mampa de colisiones para el circuito
        collision_map_prueba = data.load_sprite(collision_map_name, tileset_height, tileset_width)#, tileset_height, tileset_width)

        #Suponiendo que 4 sera el numero de capas que tendrá el mapa
        #Self.map sera la matriz logica que indicara donse se posiciona
        #cada tile y de que tipo son.
        self.map = range(4)
        #Por cada elemento:
        for n in range(4):
            self.map[n] = range(self.height) #reservamos para el alto.
            #astar.map = range(self.height)
            for m in range(self.height):
                self.map[n][m] = range(self.width) #y para el ancho.
                #astar.map[m] = range(self.width)
                for o in range(self.width):
                    self.map[n][m][o] = Tile()
                    #astar.map[m][o] = astar.PASSABLE
        
        astar.map = range(self.width)
        for m in range(self.width):
            astar.map[m] = range(self.height)
            for o in range(self.height):
                astar.map[m][o] = astar.PASSABLE

        num_layer = 0
        num_row = 0
        num_column = 0
        n = 0
        frame = None
        
        #Recorremos cada una de las capas 
        for layer in parser.getElementsByTagName('layer'):
            for tile in layer.getElementsByTagName('tile'):
                
                #Obtenemos el numero de la fila y de la columna del tile
                num_row = int(n / self.width)
                num_column = (n % self.width) % self.width
                
                #Obtenemos el frame referente al tileset
                frame = int(tile.getAttribute('gid'))
                
                #Asignamos el frame
                self.map[num_layer][num_row][num_column].frame = frame
                
                #Si el frame es 0 quiere decir que es un tile vacio, por lo que
                #Lo pondemos como pasabel
                if frame == 0:
                    self.map[num_layer][num_row][num_column].type = PASSABLE
                else:
                    
                    #Comprobamos el color del tile correspondiente en el mapa de colisiones
                    #Segun el color de este indicará que el tile es de un tipo u otro
                    if collision_map_prueba[frame - 1].get_at((0,0)) == (255, 0, 0):
                        self.map[num_layer][num_row][num_column].type = PASSABLE
                        #print "El tile: " + str(self.map[num_layer][num_row][num_column].frame - 1) + " es pasable."
                        
                    #elif pxarray[p_x][p_y] == pxarray_tile_types[1]:
                    elif collision_map_prueba[frame - 1].get_at((0,0)) == (0, 255, 0):
                        self.map[num_layer][num_row][num_column].type = NOPASSABLE
                        astar.map[num_column][num_row] = astar.NOPASSABLE
                        #print "El tile: " + str(self.map[num_layer][num_row][num_column].frame - 1) + " NO es pasable."
                        
                    #elif pxarray[p_x][p_y] == pxarray_tile_types[2]:
                    elif collision_map_prueba[frame - 1].get_at((0,0)) == (0, 0, 255):
                        self.map[num_layer][num_row][num_column].type = LAG
                        astar.map[num_column][num_row] = astar.LAG

                    
                    elif collision_map_prueba[frame - 1].get_at((0,0)) == (0, 0, 0):
                        self.map[num_layer][num_row][num_column].type = HOLE
                        astar.map[num_column][num_row] = astar.LAG

                    #Si no es ninguno de los anteriores lo seleccionamos como pasable
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
        
        #Parseamos los objetos que se introducirán en el mapa
        for element in parser.getElementsByTagName('objectgroup'):
            
            #Comprobamos si estamos enla capa de los checkpoints
            if element.getAttribute('name') == 'checkpoints':
                
                #Parseamos cada uno de los checkpoints
                for cp in element.getElementsByTagName('object'):
                    
                    #Obtenemos las caracteristicas
                    position = int(cp.getAttribute('name'))
                    type = str(cp.getAttribute('type'))
                    x = int(cp.getAttribute('x'))
                    y = int(cp.getAttribute('y'))
                    
                    new_checkpoint = None
                    
                    #Segun el tipo añadiremos un chekpoint 
                    if type == 'Horizontal' or type == 'Vertical':
                        if type == 'Horizontal':
                            new_checkpoint = checkpoint.CheckPoint(self.game_control, x, y, self.tile_width * self.circuit_width, 2)
                        elif type == 'Vertical':
                            new_checkpoint = checkpoint.CheckPoint(self.game_control, x, y, 2, self.tile_height * self.circuit_width)
                        
                        #Añadimos un nuevo checkpoint
                        self.game_control.add_checkpoint(new_checkpoint, position)
                    
                    #O la meta
                    else:
                        if type == 'GoalH':
                            new_checkpoint = checkpoint.CheckPoint(self.game_control, x, y, self.tile_width * self.circuit_width, 2)
                            self.game_control.set_start(self, x, y, 'goal', 'horizontal', self.car_angle)

                        elif type == 'GoalV':
                            new_checkpoint = checkpoint.CheckPoint(self.game_control, x, y, 2, self.tile_height * self.circuit_width)
                            self.game_control.set_start(self, x, y, 'goal', 'vertical', self.car_angle)
                            
                        #Añadimos la meta    
                        self.game_control.set_goal(new_checkpoint)
                
                #Tras obtener todos los checpoints, los ordernamos para su gestión
                self.game_control.order_checkpoints()

            if element.getAttribute('name') == 'objetos':
                
                for ob in element.getElementsByTagName('object'):
                    
                    #Obtenemos las caracteristicas
                    name = str(ob.getAttribute('name'))
                    type = str(ob.getAttribute('type'))
                    x = int(ob.getAttribute('x'))
                    y = int(ob.getAttribute('y'))    
                    
                    if type == 'Item_box':
                        item_box = itembox.ItemBox(self.game_control, 'elements/itembox.xml', x, y)
                        self.game_control.add_item_box(item_box)
                    
                    if type == 'check':
                        
                        position = int(name)
                        rect = pygame.Rect(x, y, self.tile_width, self.tile_height)
                        print rect
                        
                        self.game_control.ia_checks[position] = rect
                    if type == 'animation':
                        path_xml = "animations/" + name
                        #self.game_control.add_animation(gameanimation.GameAnimation(self.game_control, path_xml, x, y))
        
        #print str(num_layer)
        #Cargamos los distintos elementos indicados en el mapa
        #self.load_elements()            
        
    def draw(self, screen, layer):
        '''
        @brief Método encargado de dibujar el circuito
        
        @param Screen superficie destino.
        @param Layer capa del mapa a dibujar.
        '''       
        #Comprobamos que la capa es correcta         
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
        
        #Por precaución siempre dibujaremos un tile de más para evitar bandas negras
        if self.y >= self.height * self.tile_height - pygame.display.get_surface().get_height() - self.tile_height or self.y == 0:
            suma = 0
        else:
            suma = 1

        if self.x >= self.width * self.tile_width - pygame.display.get_surface().get_width() - self.tile_width:
            suma_x = 0
        else:
            suma_x = 1
        
        #Una vez echo todos los cambios obtenemos dibujamos cada uno de los tiles
        for row in range(num_blocks_y + suma):
            for column in range(num_blocks_x + suma_x):
                
                #Obtenemos el frame del tile
                frame = self.map[layer][row + ly][column + lx].frame - 1
                type = self.map[layer][row + ly][column + lx].type
                #Si el tile existe y no es uno vacio
                if frame > -1:
                    #Lo dibujamos en su posición
                    pos_x = column * self.tile_width - margin_x
                    pos_y = row * self.tile_width - margin_y
                    screen.blit(self.tileset[frame], (pos_x, pos_y))
                    if type == NOPASSABLE:
                        pass
                        #pygame.draw.rect(screen, (0, 0, 0), (pos_x, pos_y, 45, 45), 1)

            #print row
            #print num_blocks_y
        
    def move(self, x, y):
        '''
        @brief Método encargado de asignar una nueva posición x e y el circuito
        
        @param x Nueva coordenada en el eje x en píxeles.
        @param y Nueva coordenada en el eje y en píxeles.
        '''
        self.x = x
        
        if y == 0:
            self.y = 1
        else:
            self.y = y
        
    def get_tile(self, layer, x, y):
        '''
        @brief Método que devuelve un tile dada una posición
        
        @param x Coordenada del eje x del tile a consultar.
        @param y Coordenada del eje y del tile a consultar.
        '''
        #Si el tile que se pide no esta en la pantalla, ni en el tileset, 
        #Pasamos un tile vacio
        if x < 0 or x > self.width or y < 0 or y > self.height:
            print "WARNING: tile fuera de rango"
            tile = Tile()
            return tile
            
        #Dado que despues de añadir las capas a self.map, añadimos el 
        #tamaño del ancho se entiende [y][x]
        return self.map[layer][y][x]
        
    def get_tile_height(self):
        '''
        @brief Método consultor
        
        @return El alto de un tile en píxeles
        '''
        return self.tile_height 
        
    def get_tile_width(self):
        '''
        @brief Método consultor
        
        @return El ancho de un tile en píxeles
        '''
        return self.tile_width 
        
    def get_width(self):
        '''
        @brief Método consultor.
        
        @brief El ancho del circuito en tiles
        '''
        return self.width 
        
    def get_height(self):
        '''
        @brief Método consultor.
        
        @brief El alto de circuito en tiles
        '''
        return self.height
        
    def get_x(self):
        '''
        @brief Método consultor
        
        @return Coordenada actual en x del circuito en píxeles
        '''
        return self.x
        
    def get_y(self):
        '''
        @brief Método consultor.
        
        @return Coordenada actual en y del circuito en píxeles 
        '''
        return self.y
    
    def get_real_width(self):
        '''
        @brief Método consultor.
        
        @return El ancho de un circuito en pixeles
        '''
        return self.width * self.tile_width
    
    def get_real_height(self):
        '''
        @brief Método consultor
        
        @return Alto del circuito en pixeles
        '''
        return self.height * self.tile_height
    
    def get_circuit_width(self):
        '''
        @brief Método consultor
        
        @return Ancho máximo de la "carretera" del circuito
        '''
        return self.circuit_width
    
    def get_goal_width(self):
        return self.goal_width
