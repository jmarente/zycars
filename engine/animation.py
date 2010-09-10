# -*- encoding: utf-8 -*-

class Animation:
    '''
    Clase encargada de gestionar las animaciones de una imagen.
    '''
    def __init__(self, frames, delay):
        '''
        Recibe la secuancia de animación, junto con su retardo.
        '''
        self.__delay = delay
        frames = frames.split(',')
        self.__frames = []
        self.num_frames = len(frames)
        
        for element in frames:
            self.__frames.append(int(element))
            
        self.__frames.append(-1)
        self.__actual_frame = 0
        self.__counter_delay = 0
        print self.__frames
        
    def restart(self):
        '''
        Reinicia la secuencia de animación.
        '''
        self.__actual_frame = 0
        self.__counter_delay = 0
         
    def update(self):
        '''
        Actualiza la animación teniendo si ya se ha cumplido el retardo
        Devuelve verdadero si la animacion a acabado.
        Falso en caso contrario
        '''
        self.__counter_delay = self.__counter_delay  + 1
        if self.__counter_delay >= self.__delay:
            self.__counter_delay = 0
            self.__actual_frame = self.__actual_frame + 1
            if self.__frames[self.__actual_frame] == -1:
                self.__actual_frame = 0
                return True
        return False
            
    def get_delay(self):
        '''
        Método consultor del retardo de la animación
        '''
        return self.__delay
         
    def set_delay(self, new_delay):
        '''
        Establece el nuevo retardo
        '''
        self.__delay = new_delay
        
    def get_frame(self):
        '''
        Método consultor del frame actual de la animación
        '''
        return self.__frames[self.__actual_frame]
