#-*- encoding: utf-8 -*-

import basicmenu
import data
import resource
import xml.dom.minidom

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
        
        self.big_font = resource.get_font('cheesebu', 60)
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
        y = 100
        aux = 0
        for i in range(len(self.players_position)):
            
            #Si es el jugador, lo mostraremos resaltado
            if self.players_position[i][2]:
                color = (189, 9 , 38)
            else:
                color = (0, 0, 0)
                
            #Mostramos la posición del jugador
            surface_position = self.big_font.render(str(i + 1), True, color)
            screen.blit(surface_position, (30, 150 + aux))
            
            #Mostramos el orden
            surface_ordinal = self.tiny_font.render(self.position[i + 1], True, color)
            screen.blit(surface_ordinal, (60, 150 + aux))
            
            #Mostramos el avatar
            screen.blit(self.players_position[i][1].get_avatar(), (90, 150 + aux))
            
            #Mostramos el nombre
            player_name = self.big_font.render(self.players_position[i][1].get_name(), True, color)
            screen.blit(player_name, (160, 150 + aux))
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
        self.total_text = self.font.render('Tiempo total', True, (0, 0, 0))
        self.lap_text = self.font.render('Mejor Vuelta', True, (0, 0, 0))
    
    def set_results(self, player, total_time, total_improved, fast_lap, lap_improved):
        self.player = player
        aux = '%02d:%02d:%02d' % (total_time[0], total_time[1], total_time[2])
        self.total_time = self.font.render(aux, True, (0, 0, 0))
        self.total_improved = total_improved

        aux = '%02d:%02d:%02d' % (fast_lap[0], fast_lap[1], fast_lap[2])
        self.fast_lap = self.font.render(aux, True, (0, 0, 0))
        self.lap_improved = lap_improved
            
    def draw(self, screen):
        self.draw_basic_elements(screen)
        
        screen.blit(self.player.get_avatar(), (90, 180))
        name_surface = self.big_font.render(self.player.get_name(), True, (0, 0, 0))
        screen.blit(name_surface, (160, 180))
        
        screen.blit(self.lap_text, (100, 250))
        screen.blit(self.fast_lap, (130, 300))
        
        screen.blit(self.total_text, (100, 350))
        screen.blit(self.total_time, (130, 400))

        
        self.cursor.draw(screen)
