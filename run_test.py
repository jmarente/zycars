#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pygame
import engine

from engine import keyboard
from pygame.locals import *

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((200,200))
    pygame.display.set_caption("Prueba de teclado")
    ARRIBA = K_UP
    ABAJO = K_DOWN
    DERECHA = K_RIGHT
    IZQUIERDA = K_LEFT
    clock = pygame.time.Clock()
    
    while not keyboard.quit():
        clock.tick(30)
        keyboard.update()
        
        if keyboard.newpressed(ARRIBA):
            print "ARRIBA newpressed"
        if keyboard.pressed(ARRIBA):
            print "ARRIBA pressed"
        if keyboard.release(ARRIBA):
            print "ARRIBA release"
        if keyboard.newpressed(ABAJO):
            print "ABAJO newpressed"
        if keyboard.pressed(ABAJO):
            print "ABAJO pressed"
        if keyboard.release(ABAJO):
            print "ABAJO release"
        if keyboard.newpressed(DERECHA):
            print "DERECHA newpressed"
        if keyboard.pressed(DERECHA):
            print "DERECHA pressed"
        if keyboard.release(DERECHA):
            print "DERECHA release"
        if keyboard.newpressed(IZQUIERDA):
            print "IZQUIERDA newpressed"
        if keyboard.pressed(IZQUIERDA):
            print "IZQUIERDA pressed"
        if keyboard.release(IZQUIERDA):
            print "IZQUIERDA release"
                    
if __name__ == "__main__":
    main()
