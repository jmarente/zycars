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
        self.close.append(self.home)
        
        while not self.in_target():
            
            self.current = self.best_open()
            self.close.append(self.current)
            
            if not self.in_target():
                neighbors = self.get_neighbors(self.current)
                
                neighbors = self.check_neighbors(neighbors)
                #neighbors = self.check_neighbors(neighbors, self.close)
                
                self.open += neighbors
        
        return self.complete_road(self.current)
    
    def get_neighbors(self, nodo):
        neighbors = []
        
        if map[nodo.row + 1][nodo.column] == cicuit.PASSABLE:
            neighbors.append(Nodo(nodo.row + 1, nodo.column, self.target, nodo))

        if map[nodo.row - 1][nodo.column] == cicuit.PASSABLE:
            neighbors.append(Nodo(nodo.row - 1, nodo.column, self.target, nodo))
            
        if map[nodo.row][nodo.column + 1] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row, nodo.column + 1, self.target, nodo))
        
        if map[nodo.row][nodo.column - 1] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row, nodo.column - 1, self.target, nodo))

        if map[nodo.row + 1][nodo.column + 1] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row + 1, nodo.column + 1, self.target, nodo))

        if map[nodo.row - 1][nodo.column - 1] == circuit.PASSABLE:
            neighbors.append(Nodo(nodo.row + 1, nodo.column + 1, self.target, nodo))
        
        return neighbors
    
    def best_open(self):
        actual = self.open[0]
        n = 0
        for i in range(1, len(self.open)):
            if self.open[i].f < actual.f:
                actual = self.open[i]
                n = i
        
        del self.open[i]
        return actual
    
    def check_neighbors(self, neighbors):
        
        result = []
        
        for nei in neighbors:
            for element in self.close:
                if nei.row == element.row and nei.column == element.column:
                    continue
                else:
                    resulto.append(nei)
        
        neighbors = result
        result = []
        
        for nei in neighbors:
            for element in self.open:
                if nei.row == element.row and nei.column == element.column:
                    if nei.g < element.g:
                        result.append(nei)
                else:
                    result.append(nei)
        
        return result

    
    def complete_road(self, node):
        aux = node
        path = deque()
        
        while actual:
            path.appendleft(aux)
            aux = aux.father
        
        return path
            
    def in_target(self):
        if self.current.row == self.target.row and self.current.column == self.target.column:
            return True
        return False
        
def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
