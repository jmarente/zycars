#-*- encoding: utf-8 -*-

'''
@file modes.py
Implementa la clase Mode, Championship, FastRace y TimedRace
@author José Jesús Marente Florín
@date Abril 2011.
'''

import data
import state
import gamecontrol
import classificationmenu
import mainmenu
import config
import timer
import xml.dom.minidom
import pygame

from collections import deque

#Distintos estados del juego
CLASSIFICATION, CHAMPIONSHIPMENU, GAME, CHAMPIONSHIPCOMPLETED = range(4)

class Mode(state.State):
    '''
    @brief Clase base para los modos de juego
    '''
    FASTRACE, TIMED, CHAMPIONSHIP = range(3)
    def __init__(self, game, laps, xml_classification, mode):
        '''
        @brief Constructor.
        
        @param game Referencia a game
        @param laps Vueltas que dar al circuito
        @param xml_classification XML del archivo con el menú de clasificación
        '''
        self.type = mode
        state.State.__init__(self, game)
        self.laps = laps
        self.state = GAME
        self.path_circuit = None
        self.best_total_time = None
        self.best_lap = None
        self.game_control = None
        
        #Según el tipo de juego creamos un menú u otro
        if self.type == Mode.TIMED:
            self.classification = classificationmenu.TimedMenu(self, 
                                                            xml_classification) 
        else:
            self.classification = classificationmenu.ClassificationMenu(self, 
                                                            xml_classification)

    def update(self):
        '''
        @brief Actualiza el modo de juego según el estado en el que se encuentre
        '''
        if self.state == CLASSIFICATION:
            self.classification.update()
            
        elif self.state == GAME:
            self.game_control.update()
        
    def draw(self, screen):
        '''
        @brief Dibuja en pantalla el estado actual
        
        @param screen Superficie destino
        '''
        if self.state == CLASSIFICATION:
            self.classification.draw(screen)
            
        elif self.state == GAME:
            self.game_control.draw(screen) 
        
    def completed_race(self):
        '''
        @brief Gestiona el modo de juego cuando se completa una carrera
        debe ser implementada por sus sucesores
        '''
        pass
        
    def reboot_race(self):
        '''
        @brief Reinicia la carrera actual
        '''
        pygame.mixer.music.stop()
        config.Config().set_current_music('')
        self.game_control = gamecontrol.GameControl(self.game, self, 
                                                self.path_circuit, 
                                                self.best_total_time, 
                                                self.best_lap, self.laps)
        self.state = GAME

    def go_on(self):
        '''
        @brief Vuelve al menú principal
        '''
        self.game.change_state(mainmenu.MainMenu(self.game, 
                                                'menu/mainmenu.xml'))
        
    def get_times(self, circuit_name):
        '''
        @brief obtiene los tiempos de un circuito determinado
        
        @param circuit_name Nombre del circuito que debemos obtener los tiempos
        '''
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
    '''
    @brief Gestiona el modo de juego contrarreloj
    '''
    def __init__(self, game, path_circuit, laps):
        '''
        @brief Constructor.
        
        @param game Referencia a game
        @param path_circuit Ruta con el circuito que se correrá
        @param laps Vueltas al circuito
        '''
        Mode.__init__(self, game, laps, 'menu/timedmenu.xml', Mode.TIMED)
        self.path_circuit = path_circuit
        self.circuit_name = config.Config().get_circuit_name()

        self.get_times(self.circuit_name)

        self.game_control = gamecontrol.GameControl(self.game, self, 
                                                path_circuit, 
                                                self.best_total_time, 
                                                self.best_lap, laps)
            
    def completed_race(self, player, total_time, best_lap, all_laps):
        '''
        @brief Función que gestiona la finaliación de una carrera
        
        @param player Jugador
        @param total_time Tiempo total el completar el circuito
        @param best_lap Mejor vuelta del jugador
        @param all_laps Tiempos de todas las vueltas
        '''
        old_total_time = timer.Timer('cheesebu', 1, (0, 0, 0), 0, 0, "", 
                                    self.best_total_time[0], 
                                    self.best_total_time[1], 
                                    self.best_total_time[2])
                                    
        old_best_lap = timer.Timer('cheesebu', 1, (0, 0, 0), 0, 0, "", 
                                    self.best_lap[0], self.best_lap[1], 
                                    self.best_lap[2])
        
        #Comprobamos si mejora alguno de los tiempos
        total_improved = lap_improved = False
        if total_time.less_than(old_total_time):
            print "Ha mejorado el tiempo total"
            total_improved = True
        
        if best_lap.less_than(old_best_lap):
            print "Ha hecho la vuelta mas rapida"
            lap_improved = True
        
        #Si a mejorado alguno se procede a almacenarlos en el fichero de tiempos
        if lap_improved or total_improved:
            parse = xml.dom.minidom.parse(data.get_path_xml('times.xml'))
            
            for circuit in parse.getElementsByTagName('circuit'):
                if circuit.getAttribute('name') == self.circuit_name:
                    if total_improved:
                        best_race = circuit.getElementsByTagName('bestrace')[0]
                        best_race.setAttribute('minutes', 
                                            str(total_time.get_minutes()))
                        best_race.setAttribute('seconds', 
                                            str(total_time.get_seconds()))
                        best_race.setAttribute('hseconds', 
                                            str(total_time.get_hseconds()))
                    if lap_improved:
                        fastest_lap = circuit.getElementsByTagName('fasttestlap')[0]
                        fastest_lap.setAttribute('minutes', 
                                                str(best_lap.get_minutes()))
                        fastest_lap.setAttribute('seconds', 
                                                str(best_lap.get_seconds()))
                        fastest_lap.setAttribute('hseconds', 
                                                str(best_lap.get_hseconds()))
            
            #Abrimos el fichero y almacenamos los cambios
            times_file = open(data.get_path_xml('times.xml'), 'wb')
            parse.writexml(times_file, encoding = 'utf-8', indent = ' ')
            times_file.close()
        
        tuple_total_time = (total_time.get_minutes(), total_time.get_seconds(), 
                            total_time.get_hseconds())
        tuple_best_lap = (best_lap.get_minutes(), best_lap.get_seconds(), 
                        best_lap.get_hseconds())
        
        #Establecemos los tiempos para le menú de tiempos
        self.classification.set_results(player, tuple_total_time, 
                                    total_improved, tuple_best_lap, 
                                    lap_improved, all_laps)
        self.state = CLASSIFICATION

class FastRace(Mode):
    '''
    @brief Gestiona el modo de juego carrera rápida
    '''
    def __init__(self, game, path_circuit, laps):
        '''
        @brief Constructor
        
        @param game Referencia a game
        @param path_circuit Archivo con el circuito a correr
        @param laps Vueltas al circuito
        '''
        Mode.__init__(self, game, laps, 'menu/classificationmenu.xml', 
                    Mode.FASTRACE)
        self.path_circuit = path_circuit
        self.circuit_name = config.Config().get_circuit_name()

        self.circuit_name = config.Config().get_circuit_name()
        
        self.get_times(self.circuit_name)
                
        self.game_control = gamecontrol.GameControl(self.game, self, 
                                                path_circuit, 
                                                self.best_total_time, 
                                                self.best_lap, self.laps)
        
    def completed_race(self, position_players):
        '''
        @brief Función que gestiona la finalización de una carrera
        
        @param position_players Lista con la posición de los jugadores.
        '''
        self.classification.set_players_position(position_players)
        self.state = CLASSIFICATION

class ChampionShip(Mode):
    '''
    @brief Gestiona el modo campeonato
    '''
    def __init__(self, game, championship_circuits, laps):
        '''
        @brief Constructor
        
        @param game Referencia a game
        @param championship_circuits Lista de circuitos a competir
        @param laps Vueltas a los circuitos
        '''
        Mode.__init__(self, game, laps, 'menu/classificationmenu.xml', 
                    Mode.CHAMPIONSHIP)
        self.remaining_circuits = deque()
        self.path_circuit = None
        self.passed_circuits = deque()
        self.championship_menu = classificationmenu.ChampionShipMenu(self, 
                                                'menu/championshipmenu.xml')
        self.championship_completed = classificationmenu.ChampionShipCompleted(self, 
                                                'menu/championshipmenu.xml')
        
        #Puntuaciones según los puestos
        self.scores = {1: 4, 2: 2, 3: 1, 4: 0}
        self.classification_championship = []
        self.players_position = None
        
        for circuit in championship_circuits:
            self.remaining_circuits.append(circuit)
        
        #Obtenemos el circuito actual
        self.path_circuit = self.remaining_circuits.popleft()
        
        #Obtenemos los tiempos del circuito actual
        self.get_times(config.Config().get_championship_circuit_name(self.path_circuit))
        
        self.game_control = gamecontrol.GameControl(self.game, self, 
                                                self.path_circuit, 
                                                self.best_total_time, 
                                                self.best_lap, self.laps)

    def update(self):
        '''
        @brief Actualiza el campeonato según el estado en el que se encuentre
        '''
        if self.state == CLASSIFICATION:
            self.classification.update()
            
        elif self.state == GAME:
            self.game_control.update()   
        
        elif self.state == CHAMPIONSHIPMENU:
            self.championship_menu.update()

        elif self.state == CHAMPIONSHIPCOMPLETED:
            self.championship_completed.update()
    
    def draw(self, screen):
        '''
        @brief Dibuja en pantalla el estado actual
        
        @param screen Superficie destino
        '''
        if self.state == CLASSIFICATION:
            self.classification.draw(screen)
            
        elif self.state == GAME:
            self.game_control.draw(screen) 
        
        elif self.state == CHAMPIONSHIPMENU:
            self.championship_menu.draw(screen)
        
        elif self.state == CHAMPIONSHIPCOMPLETED:
            self.championship_completed.draw(screen)
                    
    def completed_race(self, position_players):
        '''
        @brief Función que gestiona la finalización de una carrera
        
        @param position_players Lista con la posición de los jugadores.
        '''
        self.players_position = []
        for i in range(len(position_players)):
            self.players_position.append((position_players[i][0], 
                                        position_players[i][1], 
                                        position_players[i][2], 
                                        self.scores[i+1]))
            
        print "Carrera completada"
        print self.players_position
        
        self.classification.set_players_position(self.players_position)
        self.state = CLASSIFICATION
                
    def go_on(self):
        '''
        @brief PAsamos de un circuito a otro
        '''
        if not self.classification_championship:
            for i in range(len(self.players_position)):
                self.classification_championship.append(
                                                [self.players_position[i][3], 
                                                self.players_position[i][1], 
                                                self.players_position[i][2]])
        else:
            for element in self.classification_championship:
                for position in self.players_position:
                    if element[1].get_name() == position[1].get_name():
                        element[0] += position[3]
        
        self.classification_championship = sorted(self.classification_championship, 
                                                reverse = True)
        
        print "ESTADO CAMPEONATO"
        print self.classification_championship
        
        self.championship_menu.set_classification_championship(self.classification_championship)
        self.state = CHAMPIONSHIPMENU
    
    def next_circuit(self):
        '''
        @brief Pasamos al circuito siguiente, si hemos terminado todos, mostramos pantalla final
        '''
        self.passed_circuits.append(self.path_circuit)
        
        if len(self.remaining_circuits):
            pygame.mixer.music.stop()
            self.path_circuit = self.remaining_circuits.popleft()
            self.get_times(config.Config().get_championship_circuit_name(self.path_circuit))
            self.state = GAME
            self.game_control = gamecontrol.GameControl(self.game, self, 
                                                    self.path_circuit, 
                                                    self.best_total_time, 
                                                    self.best_lap, self.laps)
        else:
            self.state = CHAMPIONSHIPCOMPLETED
            self.championship_completed.set_classification_player(self.classification_championship)
            #self.complete_championship()
    
    def complete_championship(self):
        '''
        @brief Termina el campeonato y volvemos al menú principal
        '''
        self.game.change_state(mainmenu.MainMenu(self.game, 
                                                'menu/mainmenu.xml'))

