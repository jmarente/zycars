# -*- encoding: utf-8 -*-
'''
@brief Carga y cachea todos los recursos multimedia necesarios.
Se pretende seguir una especie de patrón Singleton, pero usando un módulo en lugar de una clase, ya que
un módulo es accesible desde todo el sistema y tendra una única instancia.
Cuando queremos recursos de algún tipo simplente accedemos mediante su clave.
'''

import data
import pygame
import xml.dom.minidom

#Distintas variables globales
__initialize = False
__sprites = {}
__sprites_info = {}
__images = {}
__images_info = {}
__sounds = {}
__sounds_info = {}
__fonts = {}
__fonts_info = {}

def __initialize_module():
    '''
	@brief Función privada del módulo.Es la encargada de inicializar el módulo 
    parseando un fichero xml que contendrá todos los recursos necesarios en el sistema.
	'''
    parser = xml.dom.minidom.parse(data.get_path_xml('resources.xml'))
    
    for element in parser.getElementsByTagName("image"):
        code = element.getAttribute("code")
        name = element.getAttribute("name")
        alpha = bool(element.getAttribute("alpha"))
        __images_info[code] = (name, alpha)
    
    for element in parser.getElementsByTagName("sprite"):
        code = element.getAttribute("code")
        name = element.getAttribute("name")
        rows = int(element.getAttribute("rows"))
        columns = int(element.getAttribute("columns"))
        alpha = bool(element.getAttribute("alpha"))
        __sprites_info[code] = (name, rows, columns, alpha)
    
    for element in parser.getElementsByTagName("sound"):
        code = element.getAttribute("code")
        name = element.getAttribute("name") 
        __sounds_info[code] = name 
    
    for element in parser.getElementsByTagName("font"):
        code = element.getAttribute("code")
        name = element.getAttribute("name") 
        __fonts_info[code] = name 

def __check_initialize():
    '''
	@brief Función privada del módulo encargada de comprobar si el modulo ya se ha inicializado.
	Si no es asi se procede a inicializarlo.
	'''
    global __initialize
    
    if not __initialize:
        print "Módulo resource aún no inicializado, inizializando..."
        __initialize_module()
        __initialize = True

def get_image(image_code):
    '''
	@brief Función que devuelve la imagen asociada al código de imagen dado.
    
    @param image_code Código de la imagen a cargar.
    @return Referencia a la imagen cargada.
	'''
    __check_initialize()
    #si la imagen no estaba cargada la cargamos
    if __images.has_key(image_code):
        pass
        #print "Imagen " + image_code + " ya cargada."
    else:
        #print "Imagen " + str(image_code) + " no estaba cargada aún, cargando..."
        __images[image_code] = data.load_image(__images_info[image_code][0], __images_info[image_code][1])
        
    return __images[image_code]
        
def get_sprite(sprite_code):
    '''
	@brief función que devuelve el sprite asociada al código de sprite dado.
    
    @param sprite_code Código del sprite a cargar.
    @return Referencia al sprite cargado.
	'''
    __check_initialize()
    
    #Si no estaba cargado, lo cargamos
    if __sprites.has_key(sprite_code):
        pass
        #print "Sprite " + sprite_code + " ya cargado"
    else:
        #print "Sprite " + sprite_code + " no estaba cargado aún, cargando..."
        __sprites[sprite_code] = data.load_sprite(__sprites_info[sprite_code][0], __sprites_info[sprite_code][1], \
                                                __sprites_info[sprite_code][2], __sprites_info[sprite_code][3])
        
    return __sprites[sprite_code]
    
def get_sound(sound_code):
    '''
	@brief Función que devuelve el sonido asociado al código del sonido dado.
    
    @param sound_code Código del sonido a cargar.
    @return Referencia al sonido cargado.
	'''
    __check_initialize()
    if __sounds.has_key(sound_code):
        pass
        #print "Sonido " + sound_code + " ya cargado"
    else:
        #print "Sonido " +  sound_code + " no cargado, cargado..."
        __sounds[sound_code] = data.load_sound(__sounds_info[sound_code])
        
    return __sounds[sound_code]
    
def get_font(font_code, size):
    '''
	@brief Función que devuelve la fuente asociado con el codigo de fuente y tamaño dado.
    
    @param font_code Código de la fuente.
    @param size Tamaño de la fuente.
    @return Referencia a la fuente cargada
	'''
    __check_initialize()
    if __fonts.has_key((font_code, size)):
        pass
        #print "Fuente " + font_code + " con tamaño " + str(size) + " ya cargada"
    else:
        #print "Fuente " + font_code + " con tamaño " + str(size) +  " no estaba cargada aún, cargando..."
        __fonts[(font_code, size)] = data.load_font(__fonts_info[font_code], size)
        
    return __fonts[(font_code, size)]

