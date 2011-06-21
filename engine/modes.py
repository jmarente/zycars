#-*- encoding: utf-8 -*-

import data
import state
import gamecontrol
import classificationmenu
import mainmenu
import config
import timer
import xml.dom.minidom

from collections import deque

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

class TimedRace(Mode):
    def __init__(self, game, path_circuit, laps):
        self.game = game
        self.path_circuit = path_circuit
        self.laps = laps
        self.state = GAME
        self.circuit_name = config.Config().get_circuit_name()
        self.best_total_time = None
        self.best_lap = None
        self.classification = classificationmenu.TimedMenu(self, 'menu/timedmenu.xml')     

        parse = xml.dom.minidom.parse(data.get_path_xml('times.xml'))
                
        for time in parse.getElementsByTagName('circuit'):
            print time.getAttribute('name')
            if time.getAttribute('name') == self.circuit_name:
                best_race = time.getElementsByTagName('bestrace')[0]
                self.best_total_time = (int(best_race.getAttribute('minutes')),
                                        int(best_race.getAttribute('seconds')),
                                        int(best_race.getAttribute('hseconds')))
                fastest_lap = time.getElementsByTagName('fasttestlap')[0]
                self.best_lap = (int(fastest_lap.getAttribute('minutes')),
                                int(fastest_lap.getAttribute('seconds')),
                                int(fastest_lap.getAttribute('hseconds')))   
                break

        self.game_control = gamecontrol.GameControl(self.game, self, path_circuit, self.best_total_time, self.best_lap, laps)

    def update(self):
        if self.state == GAME:
            self.game_control.update()
        elif self.state == CLASSIFICATION:
            self.classification.update()

            
    def draw(self, screen):
        if self.state == GAME:
            self.game_control.draw(screen) 
        elif self.state == CLASSIFICATION:
            self.classification.draw(screen)
            
    def completed_race(self, player, total_time, best_lap):
        self.state = CLASSIFICATION
        old_total_time = timer.Timer('cheesebu', 1, (0, 0, 0), 0, 0, "", 
                                    self.best_total_time[0], 
                                    self.best_total_time[1], 
                                    self.best_total_time[2])
                                    
        old_best_lap = timer.Timer('cheesebu', 1, (0, 0, 0), 0, 0, "", 
                                    self.best_lap[0], self.best_lap[1], 
                                    self.best_lap[2])
        
        total_improved = lap_improved = False
        if total_time.less_than(old_total_time):
            print "Ha mejorado el tiempo total"
            total_improved = True
        
        if best_lap.less_than(old_best_lap):
            print "Ha hecho la vuelta mas rapida"
            lap_improved = True
        
        if lap_improved or total_improved:
            parse = xml.dom.minidom.parse(data.get_path_xml('times.xml'))
            
            for circuit in parse.getElementsByTagName('circuit'):
                if circuit.getAttribute('name') == self.circuit_name:
                    if total_improved:
                        best_race = circuit.getElementsByTagName('bestrace')[0]
                        best_race.setAttribute('minutes', str(total_time.get_minutes()))
                        best_race.setAttribute('seconds', str(total_time.get_seconds()))
                        best_race.setAttribute('hseconds', str(total_time.get_hseconds()))
                    if lap_improved:
                        fastest_lap = circuit.getElementsByTagName('fasttestlap')[0]
                        fastest_lap.setAttribute('minutes', str(best_lap.get_minutes()))
                        fastest_lap.setAttribute('seconds', str(best_lap.get_seconds()))
                        fastest_lap.setAttribute('hseconds', str(best_lap.get_hseconds()))
            
            f = open(data.get_path_xml('times.xml'), 'wb')
            parse.writexml(f, encoding = 'utf-8', indent = ' ')
            f.close()
        
        tuple_total_time = (total_time.get_minutes(), total_time.get_seconds(), total_time.get_hseconds())
        tuple_best_lap = (best_lap.get_minutes(), best_lap.get_seconds(), best_lap.get_hseconds())
        
        self.classification.set_results(player, tuple_total_time, total_improved, tuple_best_lap, lap_improved)
            
    def reboot_race(self):
        self.game_control = gamecontrol.GameControl(self.game, self, self.path_circuit, self.best_total_time, self.best_lap, self.laps)
        self.state = GAME

    def go_on(self):
        self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))
                
class FastRace(Mode):
    def __init__(self, game, path_circuit, laps):
        self.game = game
        self.path_circuit = path_circuit
        self.laps = laps
        self.circuit_name = config.Config().get_circuit_name()
        self.classification = classificationmenu.ClassificationMenu(self, 'menu/classificationmenu.xml')     
        self.state = GAME

        self.circuit_name = config.Config().get_circuit_name()
        self.best_total_time = None
        self.best_lap = None
        parse = xml.dom.minidom.parse(data.get_path_xml('times.xml'))
                
        for time in parse.getElementsByTagName('circuit'):
            print time.getAttribute('name')
            if time.getAttribute('name') == self.circuit_name:
                best_race = time.getElementsByTagName('bestrace')[0]
                self.best_total_time = (int(best_race.getAttribute('minutes')),
                                        int(best_race.getAttribute('seconds')),
                                        int(best_race.getAttribute('hseconds')))
                fastest_lap = time.getElementsByTagName('fasttestlap')[0]
                self.best_lap = (int(fastest_lap.getAttribute('minutes')),
                                int(fastest_lap.getAttribute('seconds')),
                                int(fastest_lap.getAttribute('hseconds')))  
                break
                
        self.game_control = gamecontrol.GameControl(self.game, self, path_circuit, self.best_total_time, self.best_lap, self.laps)

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
        self.game_control = gamecontrol.GameControl(self.game, self, self.path_circuit, self.best_total_time, self.best_lap, self.laps)
        self.state = GAME
    
    def go_on(self):
        self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))

class ChampionShip(Mode):
    def __init__(self, game, championship_circuits, laps):
        self.game = game
        self.remaining_circuits = deque()
        self.current_circuit_path = None
        self.passed_circuits = deque()
        self.best_total_time = None
        self.best_lap = None
        self.laps = laps
        self.classification = classificationmenu.ClassificationMenu(self, 'menu/classificationmenu.xml')     
        
        self.scores = {1: 4, 2: 2, 3: 1, 4: 0}
        
        for circuit in championship_circuits:
            self.remaining_circuits.append(circuit)
        
        self.current_circuit_path = self.remaining_circuits.popleft()
        
        self.get_times(config.Config().get_championship_circuit_name(self.current_circuit_path))
        
        self.game_control = gamecontrol.GameControl(self.game, self, self.current_circuit_path, self.best_total_time, self.best_lap, self.laps)
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
        pass
        
    def go_on(self):
        self.passed_circuits.append(self.current_circuit_path)
        
        if len(self.remaining_circuits):
            self.current_circuit_path = self.remaining_circuits.popleft()
            self.get_times(config.Config().get_championship_circuit_name(self.current_circuit_path))
            self.state = GAME
            self.game_control = gamecontrol.GameControl(self.game, self, self.current_circuit_path, self.best_total_time, self.best_lap, self.laps)
        else:
            self.complete_championship()
                    
    def get_times(self, circuit_name):
        
        parse = xml.dom.minidom.parse(data.get_path_xml('times.xml'))

        for time in parse.getElementsByTagName('circuit'):
            print time.getAttribute('name')
            if time.getAttribute('name') == circuit_name:
                best_race = time.getElementsByTagName('bestrace')[0]
                self.best_total_time = (int(best_race.getAttribute('minutes')),
                                        int(best_race.getAttribute('seconds')),
                                        int(best_race.getAttribute('hseconds')))
                fastest_lap = time.getElementsByTagName('fasttestlap')[0]
                self.best_lap = (int(fastest_lap.getAttribute('minutes')),
                                int(fastest_lap.getAttribute('seconds')),
                                int(fastest_lap.getAttribute('hseconds')))  
                break
    
    def complete_championship(self):
        self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))

