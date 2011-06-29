# -*- encoding: utf-8 -*-

import resource

class ImageGrid:
    '''
    @brief Representa una rejilla de imagenes
    '''
    def __init__(self, image_code, rows, columns):
        '''
        @brief Constructor.
        
        @param image_code Código de la imagen
        @param rows Número de filas de la imagen
        @para columns Número de columnas de la imagen
        '''
        self.rows = rows
        self.columns = columns
        
        #Cargamos la imagen
        self.image = resource.get_image(image_code)
        #self.image = data.load_image(image_code)
        
        #Obtenemos el ancho y alto de una sola imagen de la rejilla
        self.height = self.image.get_height() / self.rows
        self.width = self.image.get_width() / self.columns
        
    def draw(self, screen, frame, x, y):
        '''
        @brief Dibuja un fragmento de la imagen sobre la superficie dada
        
        @param screen Superficie destino
        @param frame Fragmento de la imagen a mostrar
        @param x Coordenada x
        @param y Coordenada y
        '''
        subsurface = self.get_frame(frame)
        
        screen.blit(subsurface, (x, y))
        
    def get_frame(self, frame):
        '''
        @brief Devuelve un solo fragmento de la rejilla de imagenes, si el frame
        de la imagen no existe, devuelve el ultimo frame
        
        @param frame Número de frame de la imagen
        @return Subsuperficie con el fragmento de la imagen deseado
        '''
        subsurface = None
        
        #Obtenemos las coordenadas del fragmento
        x = ((frame % self.columns) * self.width)
        y = ((frame / self.columns) * self.height)
        
        #obtenemos el fragmento deseado
        subsurface = self.image.subsurface((x, y, self.width, self.height))
        
        return subsurface
        
    def get_frames(self):
        '''
        @brief Consulta número de frames de la imagen
        
        @return Devuelve el número de frames de la imagen
        '''
        return self.rows * self.columns
        
    def get_rows(self):
        '''
        @brief Consultra el número de filas
        
        @return Número de filas
        '''
        return self.rows
        
    def get_columns(self):
        '''
        @brief Consultra el número de columnas
        
        @return Número de columnas
        '''
        return self.columns

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
