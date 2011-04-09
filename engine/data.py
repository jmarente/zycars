# -*- encoding: utf-8 -*-

'''
Módulo encargado de realizar los accesos a memoria necesarios, para obtener los recursos
que sean requeridos, tanto música, fuentes, imagenes como xml.

'''
    
import pygame
import os

MULTIMEDIA_DIR = os.path.relpath(os.path.join(__file__, '..', '..', 'multimedia'))
XML_DIR = os.path.relpath(os.path.join(__file__, '..', '..', 'xml'))

def check_extension(file_name, extension):
    '''
    Función encargada de comprobar si un archivo tiene la extensión dada.
    Devolverá Verdadero en el caso que lo tenga, Falso en caso contrario.
    '''
    position = file_name.find('.')
    if position == -1:
        return False
    else:
        file_name_extension = file_name[position:]
        if extension == file_name_extension:
            return True
        else:
            return False
    
def cut_sprite(image, rows, columns):
    '''
    Dado una imagen y un numero de filas y columnas, la función se encarga de
    corta la imagen segun las filas y columnas dadas.
    Devolvera un lista con todas las imagenes por separado.
    '''
    sprite = []
    temp_image =  None
    rect = image.get_rect()
    width = rect.w / columns
    height = rect.h / rows
    #sprite = range(rows * columns)
    
    for i in range(rows):
        for j in range(columns):
            temp_image = image.subsurface((rect.left, rect.top, width, height))
            sprite.append(temp_image)
            rect.left += width
        rect.top += height
        rect.left = 0
    
    return sprite

def __load_basic_image(image_name):
    '''
    Función encargada de cargar una imagen básica sin tener en cuenta canal alpha o
    o si es un sprite o no.
    '''
    if check_extension(image_name, ".png"):
        image_path = os.path.join(MULTIMEDIA_DIR, "image", image_name)
    else:
        image_path = os.path.join(MULTIMEDIA_DIR, "image", image_name + ".png")
            
    try:
        image = pygame.image.load(image_path)
    except pygame.error, message:
        raise SystemExit, message
    
    return image
    
def image_alpha(image, alpha):
    '''
    Según el valor de alpha, tomaremos un color u otro como transparente en la imagen.
    Si es True tomaremos el transparente, si es False tomaremos el color del pixel 0,0
    como transparente
    '''
    if alpha:
        image = image.convert_alpha()
    else:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
        
    return image
    
def load_image(image_name, alpha = True):
    '''
    Funcion encargada de cargar y devolver una imagen normal.
    El valor alpha indicara si la imagen tiene canal alpha o no.
    '''
    image = __load_basic_image(image_name)
    
    return image_alpha(image, alpha)
    
def load_sprite(image_name, rows, columns, alpha = True):
    '''
    Funcion encargada de cargar y devolver un sprite.
    Rows numero de filas.
    columns numero de columnas.
    El valor alpha indicara si la imagen tiene canal alpha o no
    '''
    image = __load_basic_image(image_name)
    
    image = image_alpha(image, alpha)
    
    return cut_sprite(image, rows, columns)

def load_sound(sound_name):
    '''
    Funcion encargada de cargar y devolver un sonido.
    '''
    if check_extension(sound_name, ".wav"):
        sound_path = os.path.join(MULTIMEDIA_DIR, "sound", sound_name)
    else:
        sound_path = os.path.join(MULTIMEDIA_DIR, "sound", sound_name + ".wav")
        
    try:
        sound = pygame.mixer.Sound(sound_path)
    except pygame.Error, message:
        raise SystemExit, message
    
    return sound

def load_font(font_name, size):
    '''
    Funcion encargada de cargar y devolver una fuente.
    Size, será el tamaño de la fuente.
    '''
    if check_extension(font_name, ".ttf"):
        font_path = os.path.join(MULTIMEDIA_DIR, "font", font_name)
    else:
        font_path = os.path.join(MULTIMEDIA_DIR, "font", font_name + ".ttf")
    
    try:
        font = pygame.font.Font(font_path, size)
    except pygame.Error, message:
        raise SystemExit, message
    
    return font
            
def get_path_music(music_name):
    '''
    Funcion encargada de cargar y devolver la ruta de un archivo de musica.
    '''
    if check_extension(music_name, ".ogg"):
        music_path = os.path.join(MULTIMEDIA_DIR, "music", music_name)
    else:
        music_path = os.path.join(MULTIMEDIA_DIR, "music", music_name + ".ogg")
        
    return music_path
    
def get_path_xml(xml_name, xml = True):
    '''
    Funcion encargada de cargar y devolver la ruta de un archivo xml.
    '''
    if xml:
        if check_extension(xml_name, ".xml"):
            xml_path = os.path.join(XML_DIR, xml_name)
        else:
            xml_path = os.path.join(XML_DIR, xml_name + ".xml")
    else:
        if check_extension(xml_name, ".tmx"):
            xml_path = os.path.join(XML_DIR, xml_name)
        else:
            xml_path = os.path.join(XML_DIR, xml_name + ".tmx")
        
    return xml_path
