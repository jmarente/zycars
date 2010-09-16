#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pygame

from engine import data

PASSABLE, NOPASSABLE, LAG = range(3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    
    tile_types = data.load_image('tile_types.png')
    pixelarray = pygame.PixelArray(tile_types)
    
    if pixelarray[0] == tile_types.map_rgb((255, 0, 0)):
        print "El pixel (0) es rojo"
    if pixelarray[0] == pixelarray[0]:
        print "El pixel (0) es igual q (0)"
    if pixelarray[0] != pixelarray[1]:
        print "El pixel (0) es distinto que (1)"
    if pixelarray[1] == tile_types.map_rgb((0, 255, 0)):
        print "El pixe (1) es verde"
    if pixelarray[2] == tile_types.map_rgb((0, 0, 255)):
        print "El pixe (2) es azul"
    else:
        print "No hay colorrrrrrrrrrrrrrrrrrrrr"
    
    
if __name__ == '__main__':
    main()
