#-*- encoding: utf-8 -*-

import state
import gamecontrol

class Mode(state.State):
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass 
    def completed_race(self):
        pass
    def reboot_race(self):
        pass

class Timed(Mode):
    def __init__(self, game, circuit_path):
        pass
    def update(self):
        self.game_control.update()
    def draw(self, screen):
        self.game_control.draw(screen) 
    def completed_race(self):
        pass
    def reboot_race(self):
        pass
        
class FastRace(Mode):
    def __init__(self, game, path_circuit):
        self.game = game
        print "Tipo de game en FastRace: ", type(game)
        self.game_control = gamecontrol.GameControl(game, path_circuit)        
    def update(self):
        self.game_control.update()
    def draw(self, screen):
        self.game_control.draw(screen) 
    def completed_race(self):
        pass
    def reboot_race(self):
        pass

class ChampionShip(Mode):
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass 
    def completed_race(self):
        pass
    def reboot_race(self):
        pass
