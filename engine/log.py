#-*- encoding: utf-8 -*-

'''
@file log.py
Implementa la clase Log, Singleton, ColorFormatter
@author José Jesús Marente Florín
@date Febrero 2011.
'''

import logging

class Singleton(type):
    '''
    @brief Clase singleton sacada de la wikipedia
    '''
    def __init__(cls, name, bases, dct):
        '''
        @brief Constructor
        '''
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        '''
        @brief funcion call
        '''
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args, **kw)
        return cls.__instance

class ColorFormatter(logging.Formatter):
    '''
    @brief Clase que establece el color de los mensajes
    '''
    def color(self, level=None):
        '''
        @brief Establece el color
        '''
        codes = {\
            None:       (1,   0),
            'DEBUG':    (1,   32), # verde
            'INFO':     (1,   36), # cian
            'WARNING':  (1,  33), # amarillo
            'ERROR':    (1,  31), # rojo
            'CRITICAL': (1, 101), # blanco, fondo rojo
            }
        return (chr(27)+'[%d;%dm') % codes[level]
        
    def format(self, record):
        '''
        @brief Establece el formato
        '''
        retval = logging.Formatter.format(self, record)
        return self.color(record.levelname) + retval + self.color()

class Log:
    '''
    @brief Clase Log, singleton
    '''
    __metaclass__ = Singleton
    
    def __init__(self):
        '''
        @brief Constructor
        '''
        #LOG_FILENAME = "log.out"
        
        self.logger = logging.getLogger('Zycars')
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(ColorFormatter('%(name)s - %(levelname)s - %(message)s'))
        
        self.logger.addHandler(handler)
        
        #self.logger.debug('Constructor de Log')
        
    def debug(self, text):
        '''
        @brief Indica mesaje de debug
        
        @param text Texto con el mensaje
        '''
        self.logger.debug(text)
    
    def info(self, text):
        '''
        @brief Indica mesaje de informacion
        
        @param text Texto con el mensaje
        '''
        self.logger.info(text)
    
    def warning(self, text):
        '''
        @brief Indica mesaje de warning
        
        @param text Texto con el mensaje
        '''
        self.logger.warning(text)
        
    def error(self, text):
        '''
        @brief Indica mesaje de error
        
        @param text Texto con el mensaje
        '''
        self.logger.error(text)
        
    def critical(self, text):
        '''
        @brief Indica mesaje de error critico
        
        @param text Texto con el mensaje
        '''
        self.logger.critical(text)
