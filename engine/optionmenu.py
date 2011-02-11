#-*- encoding: utf-8 -*-

import basicmenu
import data
import resource
import button
import imagebutton
import slider
import mainmenu
import xml.dom.minidom
import pygame

class OptionMenu(basicmenu.BasicMenu):
    def __init__(self, game, path_xml):
        basicmenu.BasicMenu.__init__(self, game)
        
        pygame.display.set_caption("Zycars: Opciones")

        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        self.parser_basic_info(parse)
        
        self.text_layers = {}
        self.elements_layers = {}
        self.actual_layer = None
        
        for element in parse.getElementsByTagName('layer'):
            
            name_layer = str(element.getAttribute('name'))
            self.text_layers[name_layer] = []
            self.elements_layers[name_layer] = []
            
            font_code = str(element.getAttribute('font_code'))
            size = int(element.getAttribute('size'))
            
            font_temp = resource.get_font(font_code, size)
            
            for text in element.getElementsByTagName('text'):
                
                value = text.getAttribute('value')
                posx = int(text.getAttribute('x'))
                posy = int(text.getAttribute('y'))
                text_render = font_temp.render(value, True, (0,0,0))
                text_render_rect = text_render.get_rect()
                text_render_rect.x = posx
                text_render_rect.y = posy
                
                self.text_layers[name_layer].append((text_render, text_render_rect))
            
            for slider_option in element.getElementsByTagName('slider'):
                xml_path = str(slider_option.getAttribute('xml_file'))
                x = int(slider_option.getAttribute('x'))
                y = int(slider_option.getAttribute('y'))
                new_slider = slider.Slider(xml_path, 50, 100, x, y)
                self.elements_layers[name_layer].append(new_slider)
                
        self.actual_layer = "Sonido"
                            
    def update(self):
        
        self.actual_option = None
        number = 0
        for button in self.buttons:
            button.update()
            number += 1
            if button.get_selected():
                self.actual_option = button.get_option()
        
        if self.actual_option:
            self.cursor.over()
        else:
            self.cursor.normal()
        
        for element in self.elements_layers[self.actual_layer]:
            element.update()
        
        self.cursor.update()

        if pygame.mouse.get_pressed()[0]:
            self.treat_option()
                    
    def draw(self, screen):
            
        self.draw_basic_elements(screen)
        
        for button in self.buttons:
            button.draw(screen)
        
        for element in self.text_layers[self.actual_layer]:
            screen.blit(element[0], element[1])

        for element in self.elements_layers[self.actual_layer]:
            element.draw(screen)
            
        self.cursor.draw(screen)
        
    def treat_option(self):
        if self.actual_option == "Aceptar":
            print "Aceptar"
            self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))
            
        elif self.actual_option == "Cancelar":
            print "Cancelar"
            self.game.change_state(mainmenu.MainMenu(self.game, 'menu/mainmenu.xml'))

        elif self.actual_option == "Sonido":
            self.actual_layer = "Sonido"
            
        elif self.actual_option == "Pantalla":
            self.actual_layer = "Pantalla"
            
        elif self.actual_option == "Controles":
            self.actual_layer = "Controles"
