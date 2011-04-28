# -*- encoding: utf-8 -*-

'''
@brief Módulo encargado de realizar los accesos a memoria necesarios, para obtener 
los recursos requeridos, tanto música, fuentes, imagenes, como ficheros xml.
'''
    
import pygame
import os

#Definimos los directorios en los que se encuentran los recursos multimedia
MULTIMEDIA_DIR = os.path.relpath(os.path.join(__file__, '..', '..', 'multimedia'))

#Directorio donde están los ficheros xml
XML_DIR = os.path.relpath(os.path.join(__file__, '..', '..', 'xml'))

def check_extension(file_name, extension):
    '''
    @brief Función encargada de comprobar si un archivo tiene la extensión dada.
    
    @param file_name Nombre de archivo a comprobar
    @param extension Extensión que el archivo deberia tener
    @return Verdadero en el caso que lo tenga, Falso en caso contrario.
    '''
    #Buscamos la posicion del punto que separa el nombre de la extensión
    position = file_name.find('.')
    
    #Si no tiene punto, es que no tiene extensión
    if position == -1:
        return False
    
    #Si tiene punto
    else:
        #Comparamos la extensión del archivo, con la que debería tener
        file_name_extension = file_name[position:]
        if extension == file_name_extension:
            return True
        else:
            return False
    
def cut_sprite(image, rows, columns):
    '''
    @brief Función encagarda de cortar una imagen segun las filas y columnas dadas.
    
    @param image Imagen a cortar
    @param rows Filas que tiene la imagen
    @param columns Columnas que tiene la imagen
    @return Lista con todas las imagenes por separado.
    '''
    #Lista que contendrá todas las imagenes
    sprite = []
    temp_image =  None
    rect = image.get_rect()
    
    #Obtenemos el tamaño de una imagen de la rejilla
    width = rect.w / columns
    height = rect.h / rows
    #sprite = range(rows * columns)
    
    for i in range(rows):
        for j in range(columns):
            
            #Vamos obteniendo las partes de la imagen que nos interesa
            temp_image = image.subsurface((rect.left, rect.top, width, height))
            
            #Insertamos en la lista de imagenes
            sprite.append(temp_image)
            
            #Pasamos a la siguiente imagen de la misma fila
            rect.left += width
            
        #Pasamos a la primera imagen de la siguiente fila
        rect.top += height
        rect.left = 0
    
    return sprite

def __load_basic_image(image_name):
    '''
    @brief Función encargada de cargar una imagen básica sin tener en cuenta canal alpha o
    o si es un sprite o no.
    
    @param image_name Nombre de la imagen a cargar
    @return Devuelve una imagen cargada
    '''
    #Si la imagen tiene la extensión que debería
    if check_extension(image_name, ".png") or check_extension(image_name, ".gif"):
        #Obtenemos su ruta
        image_path = os.path.join(MULTIMEDIA_DIR, "image", image_name)
    #Sino
    else:
        #Obtenemos su ruta añadiendole la extensión
        image_path = os.path.join(MULTIMEDIA_DIR, "image", image_name + ".png")
    
    #Cargamos la imagen
    try:
        image = pygame.image.load(image_path)
    except pygame.error, message:
        raise SystemExit, message
    
    return image
    
def image_alpha(image, alpha):
    '''
    @brief Función que define el canal alpha de una imagen, segun el valor de alpha
    
    @param image Imagen a convertir
    @param alpha Si es True, el fondo de la imagen es alpha.
    @return image Devuelve la imagen con el canal alpha
    '''
    #Si alpha es True, la imagen ya tiene fondo transparente
    if alpha:
        image = image.convert_alpha()
    
    #Si no, cogeremos como color alpha el pixel 0,0 de la imagen
    else:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
        
    return image
    
def load_image(image_name, alpha = True):
    '''
    @brief Funcion encargada de cargar y devolver una imagen normal.
    
    @param image_name Nombre de la imagen a cargar
    @param alpha, indica si la imagen tiene o no canal alpha
    @return La imagen cargada
    '''
    image = __load_basic_image(image_name)
    
    return image_alpha(image, alpha)
    
def load_sprite(image_name, rows, columns, alpha = True):
    '''
    @brief Funcion encargada de cargar y devolver un sprite.
    
    @param rows numero de filas.
    @param columns numero de columnas.
    @param alpha Indicará si la imagen tiene canal alpha o no
    @return Todas las imagenes que componen el sprite en una lista
    '''
    #Cargamos la imagen básica
    image = __load_basic_image(image_name)
    
    #Definimos el fondo transparente de la imagen
    image = image_alpha(image, alpha)
    
    #Devolvemos la imagen cortada
    return cut_sprite(image, rows, columns)

def load_sound(sound_name):
    '''
    @brief Función encargada de cargar y devolver un sonido.
    
    @param sound_name Nombre del sonido a cargar
    @return El archivo de sonido ya cargado
    '''
    #Comprobamos la extensión
    if check_extension(sound_name, ".wav"):
        #Obtenemos la ruta de archivo
        sound_path = os.path.join(MULTIMEDIA_DIR, "sound", sound_name)
        
    else:
        #Obtenemos la ruta del archivo añadiendole la extensión
        sound_path = os.path.join(MULTIMEDIA_DIR, "sound", sound_name + ".wav")
    
    #Cargamos el sonido
    try:
        sound = pygame.mixer.Sound(sound_path)
    except pygame.Error, message:
        raise SystemExit, message
    
    return sound

def load_font(font_name, size):
    '''
    @brief Función encargada de cargar y devolver una fuente.
    
    @param font_name Nombre de la fuente
    @param size Tamaño de la fuente.
    @return La fuente del tamaño indicado
    '''
    #Comprobamos la extensión
    if check_extension(font_name, ".ttf"):
        #Obtenemos la ruta del archivo
        font_path = os.path.join(MULTIMEDIA_DIR, "font", font_name)
        
    else:
        #Ruta del archivo añadiendole la extensión
        font_path = os.path.join(MULTIMEDIA_DIR, "font", font_name + ".ttf")
    
    #Cargamos la fuente
    try:
        font = pygame.font.Font(font_path, size)
    except pygame.Error, message:
        raise SystemExit, message
    
    return font
            
def get_path_music(music_name):
    '''
    @brief Función encargada de cargar y devolver la ruta de un archivo de musica.
    
    @param music_name Nombre del archivo de música.
    @return Ruta del archivo de musica
    '''
    #Comprobamos la extensión
    if check_extension(music_name, ".ogg"):
        #Obtenemos ruta del archivo
        music_path = os.path.join(MULTIMEDIA_DIR, "music", music_name)
        
    else:
        #Añadimos extensión
        music_path = os.path.join(MULTIMEDIA_DIR, "music", music_name + ".ogg")
        
    return music_path
    
def get_path_xml(xml_name, xml = True):
    '''
    @brief Función encargada de cargar y devolver la ruta de un archivo xml.
    
    @param nombre del archivo xml
    @param xml Indica si es un xml o tmx
    @return La ruta del acrhivo xml
    '''
    #Comprobamos extensión
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
