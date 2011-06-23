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

CLASSIFICATION, CHAMPIONSHIPMENU, GAME = range(3)

class Mode(state.State):
    FASTRACE, TIMED, CHAMPIONSHIP = range(3)
    def __init__(self, game, laps, xml_classification):
        self.game = game
        self.laps = laps
        self.state = GAME
        self.path_circuit = None
        self.best_total_time = None
        self.best_lap = None
        self.game_control = None
        if self.type == Mode.TIMED:
            self.classification = classificationmenu.TimedMenu(self, xml_classification) 
        else:
            self.classification = classificationmenu.ClassificationMenu(self, xml_classification)

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
        
    def completed_race(self):
        pass
        
    def reboot_race(self):
        self.game_control = gamecontrol.GameControl(self.game, self, self.path_circuit, self.best_total_time, self.best_lap, self.laps)
        self.state = GAME

    def go_on(self):
        self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))
        
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

class TimedRace(Mode):
    def __init__(self, game, path_circuit, laps):
        self.type = Mode.TIMED
        Mode.__init__(self, game, laps, 'menu/timedmenu.xml')
        self.path_circuit = path_circuit
        self.circuit_name = config.Config().get_circuit_name()

        self.get_times(self.circuit_name)

        self.game_control = gamecontrol.GameControl(self.game, self, path_circuit, self.best_total_time, self.best_lap, laps)
            
    def completed_race(self, player, total_time, best_lap, all_laps):
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
        
        self.classification.set_results(player, tuple_total_time, total_improved, tuple_best_lap, lap_improved, all_laps)
        self.state = CLASSIFICATION

class FastRace(Mode):
    def __init__(self, game, path_circuit, laps):
        self.type = Mode.FASTRACE
        Mode.__init__(self, game, laps, 'menu/classificationmenu.xml')
        self.path_circuit = path_circuit
        self.circuit_name = config.Config().get_circuit_name()

        self.circuit_name = config.Config().get_circuit_name()
        
        self.get_times(self.circuit_name)
                
        self.game_control = gamecontrol.GameControl(self.game, self, path_circuit, self.best_total_time, self.best_lap, self.laps)
        
    def completed_race(self, position_players):
        self.classification.set_players_position(position_players)
        self.state = CLASSIFICATION

class ChampionShip(Mode):
    def __init__(self, game, championship_circuits, laps):
        self.type = Mode.CHAMPIONSHIP
        Mode.__init__(self, game, laps, 'menu/classificationmenu.xml')
        self.remaining_circuits = deque()
        self.path_circuit = None
        self.passed_circuits = deque()
        self.championship_menu = classificationmenu.ChampionShipMenu(self, 'menu/championshipmenu.xml')     
        
        self.scores = {1: 4, 2: 2, 3: 1, 4: 0}
        self.classification_championship = []
        self.players_position = None
        
        for circuit in championship_circuits:
            self.remaining_circuits.append(circuit)
        
        self.path_circuit = self.remaining_circuits.popleft()
        
        self.get_times(config.Config().get_championship_circuit_name(self.path_circuit))
        
        self.game_control = gamecontrol.GameControl(self.game, self, self.path_circuit, self.best_total_time, self.best_lap, self.laps)

    def update(self):
        if self.state == CLASSIFICATION:
            self.classification.update()
            
        elif self.state == GAME:
            self.game_control.update()   
        
        elif self.state == CHAMPIONSHIPMENU:
            self.championship_menu.update()
    
    def draw(self, screen):
        if self.state == CLASSIFICATION:
            self.classification.draw(screen)
            
        elif self.state == GAME:
            self.game_control.draw(screen) 
        
        elif self.state == CHAMPIONSHIPMENU:
            self.championship_menu.draw(screen)
                    
    def completed_race(self, position_players):
        self.players_position = []
        for i in range(len(position_players)):
            self.players_position.append((position_players[i][0], position_players[i][1], position_players[i][2], self.scores[i+1]))
            
        print "Carrera completada"
        print self.players_position
        
        self.classification.set_players_position(self.players_position)
        self.state = CLASSIFICATION
                
    def go_on(self):
        
        if not self.classification_championship:
            for i in range(len(self.players_position)):
                self.classification_championship.append([self.players_position[i][3], self.players_position[i][1], self.players_position[i][2]])
        else:
            for element in self.classification_championship:
                for position in self.players_position:
                    if element[1].get_name() == position[1].get_name():
                        element[0] += position[3]
        
        self.classification_championship = sorted(self.classification_championship, reverse = True)
        
        print "ESTADO CAMPEONATO"
        print self.classification_championship
        
        self.championship_menu.set_classification_championship(self.classification_championship)
        self.state = CHAMPIONSHIPMENU
    
    def next_circuit(self):
        self.passed_circuits.append(self.path_circuit)
        
        if len(self.remaining_circuits):
            self.path_circuit = self.remaining_circuits.popleft()
            self.get_times(config.Config().get_championship_circuit_name(self.path_circuit))
            self.state = GAME
            self.game_control = gamecontrol.GameControl(self.game, self, self.path_circuit, self.best_total_time, self.best_lap, self.laps)
        else:
            self.complete_championship()
    
    def complete_championship(self):
        self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))

