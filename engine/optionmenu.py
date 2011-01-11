#-*- encoding: utf-8 -*-

import basicmenu
import data
import button
import imagebutton
import xml.dom.minidom
import pygame

class OptionMenu(basicmenu.BasicMenu):
    def __init__(self, game, path_xml):
        basicmenu.BasicMenu.__init__(self, game)
        
        pygame.display.set_caption("Zycars: Opciones")

        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        
        self.parser_basic_info(parse)
        
        self.buttons = []
        for element in parse.getElementsByTagName('option'):
            xml_file = str(element.getAttribute('xml_file'))
            font_code = str(element.getAttribute('font'))
            text = str(element.getAttribute('text'))
            x = int(element.getAttribute('x'))
            y = int(element.getAttribute('y'))
            type_button = str(element.getAttribute('type'))
            
            image_button = None
            
            if type_button == 'normal':
                aux_button = button.Button(xml_file, text, x, y, font_code, True)
            elif type_button == 'image_button':
                image_code = str(element.getAttribute('image'))
                image_x = int(element.getAttribute('image_x'))
                image_y = int(element.getAttribute('image_y'))
                aux_button = imagebutton.ImageButton(xml_file, text, x, y, font_code, image_code, image_x, image_y, True)
                
            self.buttons.append(aux_button)
        
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
        
        self.cursor.update()

        if pygame.mouse.get_pressed()[0]:
            self.treat_option()
            
        self.cursor.update()
        
    def draw(self, screen):
            
        self.draw_basic_elements(screen)
        
        for button in self.buttons:
            button.draw(screen)
            
        self.cursor.draw(screen)
        
    def treat_option(self):
        if self.actual_option == "Aceptar":
            print "Aceptar"
        elif self.actual_option == "Cancelar":
            print "Cancelar"
