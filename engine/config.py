#-*- encoding: utf-8 -*-

'''
@file config.py
Implementa la clase Config
@author José Jesús Marente Florín
@date Abril 2011.
'''

#import modes
import pygame

from log import Log
from log import Singleton

FASTRACE, CHAMPIONSHIP, TIMED = range(3)

class Config:
    '''
    @brief Singleton con la configuración del juego
    '''
    __metaclass__ = Singleton
    def __init__(self):
        '''
        @brief Constructor. Inicializa todos los atributos necesarios
        '''
        Log().info('Constructor: Config')
        self.player_selected = None
        self.mode = None
        self.competitors = []
        self.debug = False
        self.level_debug = 0
        self.championship = None
        self.circuit = None
        self.laps = 3
        self.circuit_name = None
        self.championship_circuits = []
        self.championship_circuits_name = {}
        self.current_music = ''
        self.music_volume = 1
        pygame.mixer.music.set_volume(self.music_volume)
        self.sound_volume = 1
        self.fullscreen = False
        self.direction = 'rows'
        self.item = pygame.K_SPACE
        self.pause = pygame.K_ESCAPE
    
    def set_laps(self, laps):
        '''
        @brief Establece las vueltas
        
        @param laps número de vueltas
        '''
        self.laps = laps
    
    def get_laps(self):
        '''
        @brief Consulto de vueltas
        
        @return Número de vueltas
        '''
        return self.laps
        
    def get_mode(self):
        '''
        @brief Consultor del modo de juego
        
        @return Modo de juego
        '''
        return self.mode
        
    def set_mode(self, mode):
        '''
        @brief Establece el modo de juego
        
        @param mode Modo de juego
        '''
        self.mode = mode
        
    def get_player(self):
        '''
        @brief Consultor del jugador seleccionado
        
        @return Jugador Seleccionado
        '''
        return self.player_selected
        
    def set_player(self, player):
        '''
        @brief Establece el jugador seleccionado
        
        @return player Jugador Seleccionado
        '''
        self.player_selected = player
        
    def get_competitors(self):
        '''
        @brief Consultor de rivales del jugador
        
        @return Rivales
        '''
        return self.competitors
    
    def set_competitors(self, competitors):
        '''
        @brief Establece los rivales del jugador
        
        @param competitors Rivales
        '''
        self.competitors = competitors
    
    def add_competitor(self, competitor):
        '''
        @brief Añade un nuevo rival del jugador
        
        @param competitor Rival
        '''
        self.competitors.append(competitor)
        
    def clear_competitors(self):
        '''
        @brief Elimina todos los competidores
        '''
        self.competitors = []
    
    def get_debug(self):
        '''
        @brief Indica si esta en modo debug o no
        
        @return True o False
        '''
        return self.debug
        
    def get_level_debug(self):
        '''
        @brief Indica nivel de debug
        
        @return nivel de debug
        '''
        return self.debug
    
    def set_circuit(self, circuit):
        '''
        @brief Establece el circuito a competir
        
        @param circuit Circuito
        '''
        self.circuit = circuit

    def set_circuit_name(self, name):
        '''
        @brief Establece el nombre del circuito a competir
        
        @param name Nombr del circuito
        '''
        self.circuit_name = name
    
    def set_championship_circuits(self, circuits):
        '''
        @brief Establece los circuitos del campeonato
        
        @param circuits Circuitos
        '''
        self.championship_circuits = circuits
    
    def set_championship_circuit_name(self, circuit_path, name):
        '''
        @brief Establece el nombre de un circuito del campeonato
        
        @param circuit_path Ruta del circuito
        @param name Nombre del circuito
        '''
        self.championship_circuits_name[circuit_path] = name
    
    def get_championship_circuit_name(self, circuit_path):
        '''
        @brief DEvuelve el nombre de un circuito del campeonato
        
        @param circuit_path Ruta del circuito
        @return Nombre del circuito
        '''
        return self.championship_circuits_name[circuit_path]
        
    def add_championship_circuit(self, circuit):
        '''
        @brief Añade nuevo circuito al campeonato
        
        @param circuit Ruta del circuito
        '''
        self.championship_circuits.append(circuit)
    
    def get_championship_circuits(self):
        '''
        @brief DEvuelve los circuitos del campeonato
        
        @return Circuitos del campoenato
        '''
        return self.championship_circuits
    
    def clear_championship_circuits(self):
        '''
        @brief Elimina todos los circuitos del campeonato
        '''
        self.championship_circuits = []
        
    def get_circuit(self):
        '''
        @brief Devuelve el circuito actual
        
        @return Circuito
        '''
        return self.circuit

    def get_circuit_name(self):
        '''
        @brief Devuelve el nombre del circuito actual
        
        @return Nombre del circuito
        '''
        return self.circuit_name
        
    def set_championship(self, cp):
        '''
        @brief Establece el campeonato
        
        @param cp Campeonato
        '''
        self.championship = cp
    
    def get_championship(self):
        '''
        @brief Devuelve el campeonato
        
        @return Campeonato
        '''
        return self.championship
    
    def get_current_music(self):
        '''
        @brief Devuelve musica actual
        
        @return Musica actual
        '''
        return self.current_music
    
    def set_current_music(self, new_music):
        '''
        @brief Establece música actual
        
        @param new_music Musica
        '''
        self.current_music = new_music
    
    def set_music_volume(self, volume):
        '''
        @brief Establece el volumen de la música
        
        @param volume Volumen de la musica
        '''
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)
   
    def get_music_volume(self):
        '''
        @brief Devuelve el volumen de la música
        
        @return Volumen de la musica
        '''
        return self.music_volume
        
    def set_sound_volume(self, volume):
        '''
        @brief Establece el volumen de los sonidos
        
        @param volume Volumen de los sonidos
        '''
        self.sound_volume = volume
   
    def get_sound_volume(self):
        '''
        @brief Devuelve el volumen de los sonidos
        
        @return Volumen de los sonidos
        '''
        return self.sound_volume
    
    def get_fullscreen(self):
        '''
        @brief Devuelve si la aplicación esta en pantalla completa
        
        @return True o False
        '''
        return self.fullscreen
        
    def set_fullscreen(self, fullscreen):
        '''
        @brief Establece o quita el modo de pantalla completa
        
        @param fullscreen Booleano
        '''
        self.fullscreen = fullscreen
    
    def get_pause_key(self):
        '''
        @brief Devuelve la tecla de pausa
        
        @return Tecla de pausa
        '''
        return self.pause 
    
    def get_item_key(self):
        '''
        @brief Devuelve la tecla de lanzar item
        
        @return Tecla de lanzar item
        '''
        return self.item
    
    def get_direction(self):        
        '''
        @brief Devuelve la tecla de direccion
        
        @return Tecla de direccion
        '''
        return self.direction
        
    def set_pause_key(self, pause):
        '''
        @brief Establece la tecla de pausa
        
        @para pause Tecla de pausa
        '''
        self.pause = pause
    
    def set_item_key(self, item):
        '''
        @brief Establece la tecla de lanzar item
        
        @param item Tecla de lanzar item
        '''
        self.item = item
    
    def set_direction(self, direction):
        '''
        @brief Establece la tecla de direccion
        
        @param direction Tecla de direccion
        '''
        self.direction = direction
    
