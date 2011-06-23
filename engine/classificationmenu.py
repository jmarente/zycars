#-*- encoding: utf-8 -*-

import basicmenu
import data
import resource
import xml.dom.minidom
import config

class ClassificationMenu(basicmenu.BasicMenu):
    '''
    @brief Muestra las posiciones de los corredores tras una carrera
    '''
    def __init__(self, father, xml_path):
        '''
        @brief Constructor.
        
        @param father Modo de juego al que pertenece
        @param xml_path Ruta del archivo xml con la configuración básica
        '''
        basicmenu.BasicMenu.__init__(self, father)
        
        parse = xml.dom.minidom.parse(data.get_path_xml(xml_path))
        self.parser_basic_info(parse)
        
        self.classification_bar = resource.get_image('classification_bar')
        self.classification_winner = resource.get_image('classification_winner')
        self.classification_player = resource.get_image('classification_player')
        
        self.big_font = resource.get_font('cheesebu', 40)
        self.tiny_font = resource.get_font('cheesebu', 20)
        
        self.players_position = None
        
    def set_players_position(self, positions):
        '''
        @brief Establece la lista de los jugadores y sus posiciones
        
        @param positions Lista con la posicion de los jugadores
        '''
        self.players_position = positions
        
    def draw(self, screen):
        '''
        @brief Muestra la posición de los jugadores en pantalla
        
        @param screen Superficie destino
        '''
        #Dibujamos los elementos básicos del menu
        self.draw_basic_elements(screen)
        
        self.position = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th'}
        self.scores = {1: '4', 2: '2', 3: '1', 4: '0'}
        y = 100
        aux = 0
        image = None
        
        for i in range(len(self.players_position)):
            
            #Si es el jugador, lo mostraremos resaltado
            if self.players_position[i][2]:
                color = (248, 179 , 51)
                image = self.classification_player
            elif (i + 1) == 1:
                color = (189, 9, 38)
                image = self.classification_winner
            else:
                color = (189, 9, 38)
                image = self.classification_bar

            #Mostramos la barra
            screen.blit(image, (0, 150 + aux))
            
            #Mostramos la posición del jugador
            surface_position = self.big_font.render(str(i + 1), True, (189, 9, 38))
            screen.blit(surface_position, (30, 160 + aux))
            
            #Mostramos el orden
            surface_ordinal = self.tiny_font.render(self.position[i + 1], True, (189, 9, 38))
            screen.blit(surface_ordinal, (50, 160 + aux))
            
            #Mostramos el avatar
            screen.blit(self.players_position[i][1].get_avatar(), (150, 135 + aux))
            
            #Mostramos el nombre
            player_name = self.big_font.render(self.players_position[i][1].get_name(), True, color)
            screen.blit(player_name, (250, 160 + aux))
            
            if config.Config().get_mode() == config.CHAMPIONSHIP:
                score = self.big_font.render(str('+' + self.scores[i+1]), True, color)
                screen.blit(score, (500, 160 + aux))
            
            aux += y
        
        #Por ultimo mostramos el cursor
        self.cursor.draw(screen)
        
    def update(self):
        '''
        @brief Método que actualiza los elementos del menú
        '''
        #Comprobamos si el punto esta situado sobre algun botón
        self.actual_option = None
        for button in self.buttons:
            button.update()
            if button.get_selected():
                self.actual_option = button.get_option()
        
        #Si es asi cambiamos la imagen del cursor
        if self.actual_option:
            self.cursor.over()
        else:
            self.cursor.normal()
        
        #Actualizamos el cursor
        self.cursor.update()
    
    def treat_option(self, option):
        '''
        @brief Controla la opción elegida y que hacer según el caso.
        '''
        if option == u"Reiniciar":
            print "Elegido: Reiniciar carrera"
            self.game.reboot_race()
 
        elif option == "Continuar":
            print "Elegido: Continuar"
            self.game.go_on()

class TimedMenu(ClassificationMenu):
    def __init__(self, father, xml_path):
        ClassificationMenu.__init__(self, father, xml_path)
        self.player = None
        self.total_time = None
        self.total_improved = None
        self.fast_lap = None
        self.lap_improved = None
        self.all_laps = None
        self.total_text = self.font.render('Tiempo total', True, (0, 0, 0))
        self.lap_text = self.font.render('Mejor Vuelta', True, (0, 0, 0))
        self.all_laps_text = self.font.render('Tiempos por vuelta', True, (0, 0, 0))
        self.tiny_font = resource.get_font('cheesebu', 10)
        self.big_font = resource.get_font('cheesebu', 60)
        self.positions = {1: self.tiny_font.render('st', True, (189, 9, 38)), 
                        2: self.tiny_font.render('nd', True, (189, 9, 38)), 
                        3: self.tiny_font.render('rd', True, (189, 9, 38)),
                        4: self.tiny_font.render('th', True, (189, 9, 38))}

    
    def set_results(self, player, total_time, total_improved, fast_lap, lap_improved, all_laps):
        self.player = player
        aux = '%02d:%02d:%02d' % (total_time[0], total_time[1], total_time[2])
        self.total_time = self.big_font.render(aux, True, (189, 9, 38))
        self.total_improved = total_improved

        aux = '%02d:%02d:%02d' % (fast_lap[0], fast_lap[1], fast_lap[2])
        self.fast_lap = self.font.render(aux, True, (189, 9, 38))
        self.lap_improved = lap_improved
        
        self.all_laps = all_laps
            
    def draw(self, screen):
        self.draw_basic_elements(screen)
        
        screen.blit(self.player.get_racer_image(), (15, 240))
        name_surface = self.big_font.render(self.player.get_name(), True, (0, 0, 0))
        screen.blit(name_surface, (50, 180))
        
        screen.blit(self.total_text, (400, 170))
        screen.blit(self.total_time, (410, 210))
        
        screen.blit(self.all_laps_text, (400, 290))
        
        y = 0
        for i in range(len(self.all_laps)):
            time_surface = self.font.render(self.all_laps[i], True, (189, 9, 38))
            number = self.font.render(str(i+1), True, (189, 9, 38))
            screen.blit(number, (410, 325 + y))
            screen.blit(self.positions[i+1], (425, 325 + y))
            screen.blit(time_surface, (440, 325 + y))
            
            y += 30

        
        screen.blit(self.lap_text, (400, 420))
        screen.blit(self.fast_lap, (410, 460))
        
        self.cursor.draw(screen)

class ChampionShipMenu(ClassificationMenu):
    def __init__(self, father, xml_path):
        ClassificationMenu.__init__(self, father, xml_path)
        self.classification_championship = None

    def set_classification_championship(self, classification_championship):
        self.classification_championship = classification_championship
    
    def draw(self, screen):
        self.draw_basic_elements(screen)

        self.position = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th'}
        self.scores = {1: '4', 2: '2', 3: '1', 4: '0'}
        y = 100
        aux = 0
        image = None
        
        for i in range(len(self.classification_championship)):
            
            #Si es el jugador, lo mostraremos resaltado
            if self.classification_championship[i][2]:
                color = (248, 179 , 51)
                image = self.classification_player
            elif (i + 1) == 1:
                color = (189, 9, 38)
                image = self.classification_winner
            else:
                color = (189, 9, 38)
                image = self.classification_bar

            #Mostramos la barra
            screen.blit(image, (0, 150 + aux))
            
            #Mostramos la posición del jugador
            surface_position = self.big_font.render(str(i + 1), True, (189, 9, 38))
            screen.blit(surface_position, (30, 160 + aux))
            
            #Mostramos el orden
            surface_ordinal = self.tiny_font.render(self.position[i + 1], True, (189, 9, 38))
            screen.blit(surface_ordinal, (50, 160 + aux))
            
            #Mostramos el avatar
            screen.blit(self.classification_championship[i][1].get_avatar(), (150, 135 + aux))
            
            #Mostramos el nombre
            player_name = self.big_font.render(self.classification_championship[i][1].get_name(), True, color)
            screen.blit(player_name, (250, 160 + aux))
            
            score = self.big_font.render(str(self.classification_championship[i][0]), True, color)
            screen.blit(score, (500, 160 + aux))
            
            aux += y

        #Por ultimo mostramos el cursor
        self.cursor.draw(screen)

    def treat_option(self, option):
        '''
        @brief Controla la opción elegida y que hacer según el caso.
        ''' 
        if option == "Continuar":
            print "Elegido: Continuar"
            self.game.next_circuit()
