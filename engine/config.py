#-*- encoding: utf-8 -*-

import modes

from log import Log
from log import Singleton

FASTRACE, CHAMPIONSHIP, TIMED = range(3)

class Config:
    __metaclass__ = Singleton
    def __init__(self):
        Log().info('Constructor: Config')
        self.player_selected = None
        self.mode = None
        self.competitors = None
        self.debug = False
        self.level_debug = 0
        self.championship = None
        self.circuit = None
        
    def get_mode(self):
        return self.mode
        
    def set_mode(self, mode):
        self.mode = mode
        
    def get_player(self):
        return self.player_selected
        
    def set_player(self, player):
        self.player_selected = player
        
    def get_competitors(self):
        return self.competitors
    
    def set_competitors(self, competitors):
        self.competitors = competitors
    
    def debug(self):
        return self.debug
        
    def level_debug(self):
        return self.debug
    
    def set_circuit(self, circuit):
        self.circuit = circuit
    
    def get_circuit(self):
        return self.circuit
    
    def set_championship(self, cp):
        self.championship = cp
    
    def get_championship(self):
        return self.championship
    
    def start_game(self):
        if self.mode == CHAMPIONSHIP:
            pass
        elif self.mode == TIMED:
            pass
        elif self.mode == FASTRACE:
            pass
