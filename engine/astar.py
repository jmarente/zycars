#-*- encoding: utf-8 -*-

'''
@file Implementación de el algoritmo A* para la búsqueda de caminos
@author José Jesús Marente Florín
@date Abril 2011
'''
import circuit

from collections import deque

#Variable global del modulo donde se almacenara el mapa de guia 
map = None

class Nodo:
    '''
    @brief Representa un nodo(posible estado) en el A*
    '''
    def __init__(self, row, column, target_pos, father = None):
        '''
        @brief Constructor
        
        @param row Fila del nodo en el mapa
        @param column Columna del nodo en el mapa
        @param target_pos Posicion del objetivo al que se desea llegar.
        @param father Nodo padre, None por defecto
        '''
        self.father = father
        self.row = row
        self.column = column
        
        #Calculamos la distancia hasta el objetivo, nuestra heuristicos
        self.h = distance((row, column), (target_pos[0], target_pos[1]))
        
        #Si no tenemos padre nuestra g es 0
        if not father:
            self.g = 0
        
        #Si no, sera la g de nuestro padre mas 1
        else:
            self.g = self.father.g + 1

        #El valor de f será la suma de g y h
        self.f = self.h + self.g
    
    def __str__(self):
        '''
        @brief Conversor a cadena 
        '''
        #Añadimos los campos que nos interesa y devolvemos el resultado
        result = ""
        result += "Fila: " + str(self.row)
        result += " Columna: " + str(self.column)
        result += " h: " + str(self.h)
        result += " g: " + str(self.g)
        result += " f: " + str(self.f)
        return result

class Astar:
    '''
    @brief Implementación de la búsqueda de caminos mediante el algoritmo A*
    '''
    def __init__(self):
        '''
        @brief Constructo. Declaramos la variables necesarias
        '''
        
        #Nodo origen
        self.home = None
        
        #Nodo destino
        self.target = None
        
        #Lista de abiertos(nodos por los que aú no hemos pasado
        self.open = []
        
        #Lista de cerrados(nodos por los que ya hemos pasado)
        self.close = []
        
        #Nodo actual
        self.current = None
    
    def get_road(self, home, target):
        '''
        @brief Calcula el camino necesario para ir del inicio al destino
        
        @param home Posición inicial
        @param target Posición destino
        @return Lista con los puntos necesarios para llegar al destino
        '''
        
        #Creamos los nodos inicial y destino
        self.home = Nodo(home[0], home[1], target)
        self.target = Nodo(target[0], target[1], target)
        
        self.current = self.home
        
        #Obtenemos los vecinos y los añadimos a la lista de abiertos
        self.open += self.get_neighbors(self.home)
        
        #Insertamos el nodo inicial en la lista de cerrados
        self.close.append(self.current)
        
        #print "Inicio: ", self.home
        #print "Objetivo: ", self.target
        
        #Comenzamos la busqueda del camino
        #Mientras no estemos en el destino
        while not self.is_target():
            
            #Obtenemos el mejor elemento de la lista de abiertos
            self.current = self.best_open()
            
            #Lo introducimos en la lista de cerrados
            self.close.append(self.current)
            
            #Si no es el objetivo
            if not self.is_target():
                
                #Obtenemos todos los nodos vecinos del actual
                neighbors = self.get_neighbors(self.current)
                
                #Comprobamos los vecinos y actualizamos la lista de abiertos y cerrados
                self.check_neighbors(neighbors)
        
        #Una vez completado devolvemos la lista completa del camino
        return self.complete_road(self.current)
    
    def get_neighbors(self, nodo):
        '''
        @brief Obtiene la lista de vecinos del nodo
        
        @param nodo Nodo del que queremos obtener los vecinos
        @return lista con los vecinos
        '''
        neighbors = []
        
        #Obtenemos los nodos adyacentes si son atravesables
        if map[nodo.row + 1][nodo.column] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row + 1, nodo.column, (self.target.row, self.target.column), nodo))

        if map[nodo.row - 1][nodo.column] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row - 1, nodo.column, (self.target.row, self.target.column), nodo))
            
        if map[nodo.row][nodo.column + 1] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row, nodo.column + 1, (self.target.row, self.target.column), nodo))
        
        if map[nodo.row][nodo.column - 1] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row, nodo.column - 1, (self.target.row, self.target.column), nodo))

        if map[nodo.row + 1][nodo.column + 1] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row + 1, nodo.column + 1, (self.target.row, self.target.column), nodo))

        if map[nodo.row - 1][nodo.column - 1] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row + 1, nodo.column + 1, (self.target.row, self.target.column), nodo))
        
        return neighbors
    
    def best_open(self):
        '''
        @brief Devuelve el nodo con la f mas baja de la lista de abiertos, y lo elimina de esta
        '''
        actual = self.open[0]
        n = 0
        
        #Recorremos los nodos de la lista de abiertos
        for i in range(1, len(self.open)):
            
            #Si el actual tiene mejor f, nos lo quedamos
            if self.open[i].f < actual.f:
                actual = self.open[i]
                n = i
        
        #Lo eliminamos de la lista de abiertos
        del self.open[n]
        return actual
    
    def in_list(self, node, myList):
        '''
        @brief Comprueba si un nodo esta en un lista
        
        @param node Nodo a comprobar
        '''
        for element in myList:
            #Si tiene la misma posicion es que son el mismo nodo
            if node.row == element.row and node.column == element.column:
                return True
                
        return False
    
    def check_neighbors(self, neighbors):
        '''
        @brief Comprueba si los vecinos estan en abiertos o cerrados y actualiza la lista de abietos
        
        @param neighbors Lista con los nodos vecinos
        '''
        #recorremos cada uno de los vecinos
        for i in range(len(neighbors)):
            
            #Si esta en la lista de cerramos continuamos
			if self.in_list(neighbors[i], self.close):
				continue
            
            #Si no esta en la lista de abiertos lo insertamos en esta
			elif not self.in_list(neighbors[i], self.open):
				self.open.append(neighbors[i])
            
            #Si esta en la lista de abiertos    
			else:
                #Comprobamos el valor de g, si es mejor que el de nodo actual
				if self.current.g + 1 < neighbors[i].g:
                    
                    #Localizamos el nodo en la lista de abiertos
					for j in range(len(self.open)):
						if neighbors[i].row == self.open[j].row and neighbors[i].column == self.open[j].column :
                            
                            #Eliminamos el anterior
							del self.open[j]
                            
                            #Introducimos el nuevo
							self.open.append(neighbors[i])
							break

    
    def complete_road(self, node):
        '''
        @brief Obtiene la lista con el camino completo hasta un nodo
        
        @param node Nodo a obtener el camino
        @brief Cola con el camino hacia el nodo
        '''
        aux = node
        path = deque()
        
        #Mientras el padre no sea nulo(para no añadir también el inicio)
        while aux.father:
            #Vamos añadiendo en la cola
            path.appendleft(aux)
            aux = aux.father
        
        return path
            
    def is_target(self):
        '''
        @brief Comprueba si el nodo actual es el objetivo
        '''
        #Si tienen la misma posición es que es el objetivo
        if self.current.row == self.target.row and self.current.column == self.target.column:
            return True
            
        return False
        
def distance(a, b):
    '''
    @brief Calcula la distancia en linea recta de dos elemento
    '''
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
