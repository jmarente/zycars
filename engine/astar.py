#-*- encoding: utf-8 -*-

import circuit

from collections import deque

map = None

class Nodo:
    def __init__(self, row, column, target_pos, father = None):
        self.father = father
        self.row = row
        self.column = column
        self.h = distance((row, column), (target_pos[0], target_pos[1]))
        
        if not father:
            self.g = 0
        else:
            self.g = self.father.g + 1

        self.f = self.h + self.g
    
    def __str__(self):
        result = ""
        result += "Fila: " + str(self.row)
        result += " Columna: " + str(self.column)
        result += " h: " + str(self.h)
        result += " g: " + str(self.g)
        result += " f: " + str(self.f)
        #return str((self.row, self.column))
        return result

class Astar:
    def __init__(self):
        self.home = None
        self.target = None
        
        self.open = []
        self.close = []
        self.current = None
    
    def get_road(self, home, target):
        
        self.home = Nodo(home[0], home[1], target)
        self.target = Nodo(target[0], target[1], target)
        
        self.current = self.home
        self.open += self.get_neighbors(self.home)
        self.close.append(self.current)
        
        print "Inicio: ", self.home
        print "Objetivo: ", self.target
        while not self.is_target():
            
            self.current = self.best_open()
            self.close.append(self.current)
            
            if not self.is_target():
                neighbors = self.get_neighbors(self.current)
                
                self.check_neighbors(neighbors)
                #neighbors = self.check_neighbors(neighbors, self.close)
                
                #self.open += neighbors
        
        return self.complete_road(self.current)
    
    def get_neighbors(self, nodo):
        neighbors = []
        
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
        actual = self.open[0]
        n = 0
        for i in range(1, len(self.open)):
            if self.open[i].f < actual.f:
                actual = self.open[i]
                n = i
        
        del self.open[n]
        return actual
    
    def in_list(self, node, myList):
        for element in myList:
            if node.row == element.row and node.column == element.column:
                return True
        return False
    
    def check_neighbors(self, neighbors):
        for i in range(len(neighbors)):
			if self.in_list(neighbors[i], self.close):
				continue
			elif not self.in_list(neighbors[i], self.open):
				self.open.append(neighbors[i])
			else:
				if self.current.g + 1 < neighbors[i].g:
					for j in range(len(self.open)):
						if neighbors[i].row == self.open[j].row and neighbors[i].column == self.open[j].column :
							del self.open[j]
							self.open.append(neighbors[i])
							break

    
    def complete_road(self, node):
        aux = node
        path = deque()
        
        while aux.father:
            path.appendleft(aux)
            aux = aux.father
        
        return path
            
    def is_target(self):
        if self.current.row == self.target.row and self.current.column == self.target.column:
            return True
        return False
        
def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
