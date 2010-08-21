#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import engine
import pygame

from engine import data
from pygame.locals import *

def main():
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Prueba del modulo data.py')
    
    image1 = data.load_image('gameover')
    image2 = data.load_image('gameover.png')
    
    sprite1 = data.load_sprite('granny', 8, 12)
    sprite2 = data.load_sprite('granny.png', 8, 12)
    
    sound1 = data.load_sound('vanquish.wav')
    sound2 = data.load_sound('vanquish')
    
    font1 = data.load_font('DroidSans', 20)
    font2 = data.load_font('DroidSans.ttf', 35)
    
    font1_render = font1.render('Prueba de Font1', True, (0, 0, 0))
    font2_render = font2.render('Prueba de Font2', False, (0, 0, 0))
    
    path_music1 = data.get_path_music('waterski_me')
    path_music2 = data.get_path_music('waterski_me.ogg')
    
    path_xml1 = data.get_path_xml('prueba')
    path_xml2 = data.get_path_xml('prueba.xml')
    
    print path_xml1
    print path_xml2
    
    num1 = 0
    for elementos in sprite1:
        num1 += 1
    print num1

    num2 = 0
    for elementos in sprite2:
        num2 += 1
    print num2
    
    salir = False
    
    #sound1.play(-1)
    
    while not salir:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                salir = True
            if event.type == KEYDOWN:
                if event.key == K_1:
                   sound2.stop()
                   sound1.play(-1)
                elif event.key == K_2:
                    sound1.stop()
                    sound2.play(-1)
                elif event.key == K_3:
                    sound1.stop()
                    sound2.stop()
                elif event.key == K_a:
                    pygame.mixer.music.load(path_music1)
                    pygame.mixer.music.play(-1)
                elif event.key == K_s:     
                    pygame.mixer.music.load(path_music2)
                    pygame.mixer.music.play(-1)
                elif event.key == K_d:     
                    pygame.mixer.music.stop()
                    
        screen.blit(image1, (0, 0))
        screen.blit(image2, (400, 0))  
        screen.blit(sprite1[34], (5,5))      
        screen.blit(sprite2[95], (5,200))  
        screen.blit(font1_render, (400,5))    
        screen.blit(font2_render, (400,100))    
        pygame.display.flip()
    
if __name__ == "__main__":
    pygame.init()
    main()
