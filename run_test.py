#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
from log import Log

def main():
    print "Prueba módulo log"
    Log().debug('debug')
    Log().info('info')    
    Log().error('error')
    Log().critical('critical')    
    Log().warning('warning')
    funcion_prueba()
    
def funcion_prueba():
    Log().debug('lalala')
    
if __name__ == "__main__":
    sys.exit(main())
