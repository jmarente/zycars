#-*- encoding: utf-8 -*-

import logging

class Singleton(type):
 
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance

class ColorFormatter(logging.Formatter):
 
    def color(self, level=None):
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
        retval = logging.Formatter.format(self, record)
        return self.color(record.levelname) + retval + self.color()

class Log:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        LOG_FILENAME = "log.out"
        
        self.logger = logging.getLogger('Zycars')
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(ColorFormatter('%(name)s - %(levelname)s - %(message)s'))
        
        self.logger.addHandler(handler)
        
        self.logger.debug('Constructor de Log')
        
    def debug(self, text):
        #self.logger.debug((chr(27) + '[1;31m') + text)
        self.logger.debug(text)
    
    def info(self, text):
        self.logger.info(text)
    
    def warning(self, text):
        self.logger.warning(text)
        
    def error(self, text):
        self.logger.error(text)
        
    def critical(self, text):
        self.logger.critical(text)
