#ifndef _NIVEL_
#define _NIVEL_

#include <vector>
#include <string>
#include <SDL/SDL.h>
#include "imagen.h"
#include "parser.h"

class Juego;

/**
	\enum tipo_tile
	
	Utilizado para saber de qué tipo es cada tile
*/
typedef enum{
	ATRAVESABLE,
	NOATRAVESABLE,
	SUELOFLOTANTE
} tipo_tile;

/**
	\struct Tile
	@brief Registro que guarda la información sobre los tiles, el cuadro de la rejilla del tileset y su tipo
*/
/*typedef struct{
	
		Cuadro del Tileset (rejilla de imágenes)
	
	int cuadro;
	
		Tipo de tile (atravesable, no atravesable etc)
	
	int tipo;
}Tile;*/

typedef int Tile;

/**
	@brief Utilizada para cargar, manejar y dibujar los niveles del juego
	
	Abre un fichero tipo "niveles.xml" con una estructura análofa a la siguiente:
	
	\code
	<niveles>
		<nivel ruta="nivel1.xml" />
		<nivel ruta="nivel2.xml" />
	</niveles>
	\endcode
	
	Los niveles se han creado con la aplicación Tiled un creador de mapas basados en tiles libre y multiplataforma, ya que utiliza Java.
	Para obtener el programa: http://mapeditor.org/ En su web se puede aprender la utilización del programa.
	Al crear un mapa con este programa se puede exportar en formato XML. Esta clase es capaz de Parsear este tipo de ficheros XML y cargarlos.
	
	Forma de crear mapas con Tiled compatibles con Air Force Pilot
	
	<ul>
		<li>Los mapas deben tener 4 capas:
		<ul>
			<li>Capa 0: Tiles para el terreno (suelo, mar...)</li>
			<li>Capa 1: Tiles con transparencias (rocas, vallas, flores...)</li>
			<li>Capa 2: Tiles que deben ser renderizados encima del personaje (parte alta de árboles y casas...)</li>
			<li>Capa 3: Tiles con los participantes (enemigos, objetos...)</li>
		</ul></li>
		<li>Las colisiones de terreno serán comprobadas en las capas 0, 1 y 3</li>
	</ul>
	
*/
class Nivel{
	public:
		
		/**
			Constructor
			Abre el fichero explicado anteriormente con las rutas de todos los niveles
			@param ruta Ruta del fichero XML que contiene las rutas de todos los niveles de juego
		*/
		Nivel(Juego *juego, std::string ruta);
		
		/**
			Destructor
			Libera la memoria ocupada por los niveles
		*/
		~Nivel();
		
		/**
			Dibuja la capa seleccionada del nivel actual en pantalla dentro del recuadro asignado
			@param superficie Superficie donde hacer el bliting
			@param capa Capa del mapa a ser bliteada
		*/
		void dibujar(SDL_Surface* superficie, int capa);
		
		/**
			Carga el nivel i en memoria
			@param i Número del nivel a cargar
		*/
		void cargar_nivel(int i);
		
		/**
			Carga el siguiente nivel en memoria
		*/
		void siguiente();
		
		/**
			Carga el nivel anterior en memoria
		*/
		void anterior();
		
		/**
			Reinicia el nivel actual (cuando el personaje muere, por ejemplo)
		*/
		void reinciar();
		
		/**
			Utilizado para hacer scrolling, mueve la esquina superior izquierda de la parte visible del mapa a las coordenadas x,y
			@param x_ Coordenada en el eje x donde se moverá el mapa
			@param y_ Coordenada en el eje y donde se moverá el mapa
		*/
		void mover(int x_, int y_);
		
		/**
			@return Número del Nivel actual
		*/
		int nivel_actual() const;
		
		/**
			@return Número de niveles disponibles
		*/
		int n_niveles() const;
		
		/**
			@return Scroll en el eje x del nivel en píxeles
		*/
		int nivel_x() const;
		
		/**
			@return Scroll en el eje y del nivel en píxeles
		*/
		int nivel_y() const;
		
		/**
			@return Altura del nivel en píxeles
		*/
		int nivel_alto() const;
		
		/**
			@return Anchura del nivel en píxeles
		*/
		int nivel_ancho() const;
		
		/**
			@return Altura de un tile en píxeles
		*/
		int tile_alto() const;
		
		/**
			@return Anchura de un tile en píxeles
		*/
		int tile_ancho() const;
		
		/**
			Consulta un tile dadas unas cordenadas y una capa del nivel
		
			@param x Coordenada del eje x del nivel en píxeles
			@param y Coordenada del eje y del nivel en píxeles
			@param capa Capa a consultar
			@return Devuelve el Tile que se encuentra en (x,y) en la capa indicada
		*/
		Tile get_tile(int x, int y, int capa) const;
		
	private:
		Juego *juego_;
		
		int numero_nivel; // Número de nivel actual
		int numero_niveles; // Número de niveles
		Tile*** mapa; // Mapa de tiles (es tridimensional porque son 3 capas)
		std::vector<std::string> niveles; // Vector con las rutas de los niveles del juego
		Imagen* tileset;
		
		int x, y; // Coordenadas a partir de las cuales se renderiza el mapa
		int alto_, ancho_; // Alto y ancho del mapa
		int tile_ancho_, tile_alto_; // Alto y ancho de cada tile
		
		void cargar_actores(); // Utiliza la clase Juego para incluir en los actores del juego
};

inline int Nivel::n_niveles() const {return numero_niveles;}
inline int Nivel::nivel_actual() const {return numero_nivel;}
inline Tile Nivel::get_tile(int x, int y, int capa) const {return mapa[x][y][capa];}
inline int Nivel::nivel_x() const {return x;}
inline int Nivel::nivel_y() const {return y;}
inline int Nivel::nivel_alto() const {return alto_ * tile_alto_;}
inline int Nivel::nivel_ancho() const {return ancho_ * tile_ancho_;}
inline int Nivel::tile_alto() const {return tile_alto_;}
inline int Nivel::tile_ancho() const {return tile_ancho_;}

#endif
