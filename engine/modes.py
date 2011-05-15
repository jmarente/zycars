#-*- encoding: utf-8 -*-

import state
import gamecontrol
import classificationmenu
import mainmenu

CLASSIFICATION, GAME = range(2)

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
        self.game = game
        print "Tipo de game en FastRace: ", type(game)
        self.game_control = gamecontrol.GameControl(self.game, self, path_circuit)
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
        self.path_circuit = path_circuit
        self.game_control = gamecontrol.GameControl(self.game, self, path_circuit, 1)  
        self.classification = classificationmenu.ClassificationMenu(self, 'menu/classificationmenu.xml')     
        self.state = GAME
        
    def update(self):
        if self.state == CLASSIFICATION:
            self.classification.update()
            
        elif self.state == GAME:
            self.game_control.update()
        
    def draw(self, screen):
        if self.state == CLASSIFICATION:
            self.classification.draw(screen)
            
        elif self.state == GAME:
            self.game_control.draw(screen) 
        
    def completed_race(self, position_players):
        self.classification.set_players_position(position_players)
        self.state = CLASSIFICATION
        
    def reboot_race(self):
        self.game_control = gamecontrol.GameControl(self.game, self, self.path_circuit, 1)  
        self.state = GAME
    
    def go_on(self):
        self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))

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
