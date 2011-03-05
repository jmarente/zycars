# -*- encoding: utf-8 -*-

class Animation:
    '''
    @brief Clase encargada de gestionar las animaciones de una imagen.
    '''
    def __init__(self, frames, delay):
        '''
        @brief Constructor
        
        @param frames Cadena con los distintos frames de la animación, separados por comas
        @param delay Retardo entre un frame y otro
        '''
        self.__delay = delay
        
        #Dividimos la cadena por las comas
        frames = frames.split(',')
        self.__frames = []
        #Obtenemos el número de frames
        self.num_frames = len(frames)
        
        #Introducimos los frames en la lista de frames
        for element in frames:
            self.__frames.append(int(element))
        
        #Añadimos al final un -1, para indicar la finalización de la animación
        self.__frames.append(-1)
        
        #Indicamos el comienzo y el contador de retardo inicial
        self.__actual_frame = 0
        self.__counter_delay = 0
        
    def restart(self):
        '''
        @brief Método que reinicia la secuencia de animación.
        '''
        #Ponemos a 0 el contador del frame actual y el contador de retardo
        self.__actual_frame = 0
        self.__counter_delay = 0
         
    def update(self):
        '''
        @brief Actualiza la animación teniendo si ya se ha cumplido el retardo
        
        @return True si la animacion a acabado. Falso en caso contrario
        '''
        #Aumentamos el contador de retardo
        self.__counter_delay = self.__counter_delay  + 1
        
        #Si ya a pasado el retardo indicado
        if self.__counter_delay >= self.__delay:
            #Reiniciamos el contador
            self.__counter_delay = 0
            #Pasamor al siguiente frame de animación
            self.__actual_frame = self.__actual_frame + 1
            
            #Si ya hemos pasado el ultimo frame, reiniciamos el indice de frame
            if self.__frames[self.__actual_frame] == -1:
                self.__actual_frame = 0
                #Devolvemos True indicando que se ha completado la animación
                return True
        return False
            
    def get_delay(self):
        '''
        @brief Método consultor del retardo de la animación
        
        @return Retardo de la animación
        '''
        return self.__delay
         
    def set_delay(self, new_delay):
        '''
        @brief Método que establece un nuevo retardo
        
        @param Nuevo retardo de la animación
        '''
        self.__delay = new_delay
        
    def get_frame(self):
        '''
        @brief Método consultor del frame actual de la animación
        
        @return Frame actual de la animación
        '''
        return self.__frames[self.__actual_frame]
