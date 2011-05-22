#-*- encoding: utf-8 -*-

import modes
import gamecontrol

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
        self.laps = None
        self.circuit_name = None
    
    def set_laps(self, laps):
        self.laps = laps
    
    def get_laps(self):
        return self.laps
        
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

    def set_circuit_name(self, name):
        self.circuit_name = name
        
    def get_circuit(self):
        return self.circuit

    def get_circuit_name(self):
        return self.circuit_name
        
    def set_championship(self, cp):
        self.championship = cp
    
    def get_championship(self):
        return self.championship
    
    def start_game(self, game):
        if self.mode == CHAMPIONSHIP:
            print "Modo campeonato no disponible"
        elif self.mode == TIMED:
            game.change_state(modes.TimedRace(game, self.get_circuit(), self.laps))
        elif self.mode == FASTRACE:
            game.change_state(modes.FastRace(game, self.get_circuit(), self.laps))
