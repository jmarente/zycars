#-*- encoding: utf-8 -*-

import basicmenu
import data
import resource
import imagebutton
import xml.dom.minidom
import pygame
from collections import deque

class CarFeatures:
    def __init__(self):
        pass
    def update(self):
        pass 
    def draw(self, screen):
        pass 

class GroupOption:
    def __init__(self, parse_xml, image_normal_code, image_selected_code, x, y, image_y):
        self.x = x
        self.y = y
        self.image_y = image_y
        options = []
        self.normal_image = resource.get_image(image_normal_code)
        self.option1_x = x
        self.option2_x = self.normal_image.get_width() + self.option1_x + 50
        self.selected_image = resource.get_image(image_selected_code)
        self.option3_x = self.normal_image.get_width() + self.option2_x + 50
        self.left_options = deque()
        self.right_options = deque()
        self.actual_option = None
        self.actual_right = None
        self.actual_left = None
        
        for element in parse_xml.getElementsByTagName('character'):
            image_code = element.getAttribute('image')
            name = element.getAttribute('name')
            self.right_options.append((name, resource.get_image(image_code)))
        
        self.actual_option = self.right_options.popleft()
        self.actual_right = self.right_options.popleft()

    def update(self):
        pass
    def draw(self, screen):
        if self.actual_left:
            screen.blit(self.normal_image, (self.option1_x, self.y))
            screen.blit(self.actual_left[1], (self.option1_x, self.image_y))

        screen.blit(self.selected_image, (self.option2_x, self.y))
        screen.blit(self.actual_option[1], (self.option2_x, self.image_y))
        
        if self.actual_right:
            screen.blit(self.normal_image, (self.option3_x, self.y))
            screen.blit(self.actual_right[1], (self.option3_x, self.image_y))
        
    def actual_selected(self):
        return self.actual_option[0]
        
    def move_left(self):
        if self.actual_right:
            self.left_options.append(self.actual_left)
            self.actual_left = self.actual_option
            self.actual_option = self.actual_right
            if len(self.right_options) > 0:
                self.actual_right = self.right_options.popleft()
            else:
                self.actual_right = None
                
    def move_right(self):
        if self.actual_left:
            self.right_options.appendleft(self.actual_right)
            self.actual_right = self.actual_option
            self.actual_option = self.actual_left
            if len(self.left_options) > 0:
                self.actual_left = self.left_options.pop()
            else:
                self.actual_left = None
                
    def add_option(self, new_option):
        if not self.actual_option:
            self.actual_option = new_option
        else:
            self.right_options.append(new_option)

class CharacterMenu(basicmenu.BasicMenu):
    def __init__(self, game, path_xml):
        basicmenu.BasicMenu.__init__(self, game)
        
        pygame.display.set_caption("Zycars: Selección de personaje")
        
        parse = xml.dom.minidom.parse(data.get_path_xml(path_xml))
        self.parser_basic_info(parse)
        
        characters_parse = parse.getElementsByTagName('characters')[0]
        self.group_option = GroupOption(characters_parse, characters_parse.getAttribute('normal_image'), \
                                        characters_parse.getAttribute('selected_image'),150, 110, 80)
        
        self.cars = {}
        for element in parse.getElementsByTagName('character'):
            character_name = element.getAttribute('name')
            image_car_code = element.getAttribute('image_car')
            path_xml = element.getAttribute('path_xml')
            
            self.cars[character_name] = {}
            self.cars[character_name]['image_car'] = resource.get_image(image_car_code)
            self.cars[character_name]['name_character'] = resource.get_font('cheesebu', 40).render(character_name, True, (255, 255, 255))
            self.cars[character_name]['path_xml'] = path_xml
        self.new_pressed = True
        
    def update(self):
        
        self.actual_option = None
        for button in self.buttons:
            button.update()
            if button.get_selected():
                self.actual_option = button.get_option()
        
        if self.actual_option:
            self.cursor.over()
            if pygame.mouse.get_pressed()[0]:
                self.treat_option()
                self.new_pressed = False
            else:
                self.new_pressed = True
        else:
            self.cursor.normal()
                
        self.cursor.update()
    
    def draw(self, screen):
        
        self.draw_basic_elements(screen)

        for button in self.buttons:
            button.draw(screen)
        
        self.group_option.draw(screen)
        
        screen.blit(self.cars[self.group_option.actual_selected()]['image_car'], (50, 325))
        screen.blit(self.cars[self.group_option.actual_selected()]['name_character'], (300, 270))
        
        self.cursor.draw(screen)
    
    def treat_option(self):
        if self.actual_option == "Aceptar":
            print "Aceptar, Elegido:" + self.cars[self.group_option.actual_selected()]['path_xml']
            
        elif self.actual_option == "Cancelar":
            print "Cancelar"
        
        elif self.actual_option == "Izquierda":
            if self.new_pressed:
                print "Izquierda"
                self.group_option.move_right()
            
        elif self.actual_option == "Derecha":
            if self.new_pressed:
                print "Derecha"            
                self.group_option.move_left()
