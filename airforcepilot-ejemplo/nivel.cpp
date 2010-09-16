#include <iostream>
#include <cstdlib>
#include <map>
#include <string>
#include <algorithm>
#include "nivel.h"
#include "juego.h"
#include "universo.h"
#include "enemigo.h"
#include "harrier.h"
#include "aguila.h"

using namespace std;

Nivel::Nivel(Juego *juego, std::string ruta): juego_(juego)
{
	numero_nivel = 0;
	numero_niveles = 0;
	
	// Abrimos niveles.xml y sacamos la lista de todos los niveles del juego
	Parser p_niveles("XML/niveles.xml");
	
	vector<ticpp::Element*> lista_niveles;
	vector<ticpp::Element*>::iterator i;

	p_niveles.encontrar("nivel", lista_niveles);
	for(i = lista_niveles.begin(); i != lista_niveles.end(); i++){
		niveles.push_back(p_niveles.atributo("ruta", *i));
		numero_niveles++;
	}
		
	x = y = tile_alto_ = tile_ancho_ = alto_ = ancho_ = 0;
	mapa = NULL;
	tileset = NULL;
}

void Nivel::cargar_nivel(int i)
{
	int tileset_ancho = 1, tileset_alto = 1;
	
	if(i < 0 || i > numero_niveles - 1){
		cerr << "Nivel::cargar_nivel(): Nivel inexistente" << endl;
		exit(1);
	}
	
	// Si estaba cargado un nivel, liberamos su memoria
	if(mapa){
		free(**mapa);
		free(*mapa);
		free(mapa);
		mapa = NULL;
	}
	if(tileset){
		delete tileset;
		tileset = NULL;
	}
	
	numero_nivel = i;
	
	// Abrimos el fichero donde está la información del nivel actual
	Parser p_nivel(niveles[i]);
	
	ticpp::Element* e;
	
	// Información del mapa
	e = p_nivel.encontrar("map");
	p_nivel.atributo("width", e, &ancho_);
	p_nivel.atributo("height", e, &alto_);
	p_nivel.atributo("tileheight", e, &tile_alto_);
	p_nivel.atributo("tilewidth", e, &tile_ancho_);
	
	// Información del tileset
	e = p_nivel.encontrar("image");
	string ruta = p_nivel.atributo("source", e);
	
	e = p_nivel.encontrar("properties", p_nivel.encontrar("map"));
	
	// Número de tiles ancho/largo del tileset
	vector<ticpp::Element*>propiedades;
	
	p_nivel.encontrar("property", propiedades, e);
	
	for(vector<ticpp::Element*>::iterator i = propiedades.begin(); i != propiedades.end(); i++){
		if(p_nivel.atributo("name", *i) == "tileset_ancho")
			p_nivel.atributo("value", *i, &tileset_ancho);
		else if(p_nivel.atributo("name", *i) == "tileset_alto")
			p_nivel.atributo("value", *i, &tileset_alto);
	}
	
	tileset = new Imagen(ruta.c_str(), tileset_ancho, tileset_alto);
	
	// Falta color de transparencia
	
	// Mapa FORMATO mapa[CAPA][FILA][COLUMNA]
	
	// Reservamos memoria para el cubo de tiles
	
	
	
	if((mapa = (Tile***)malloc(4 * sizeof(Tile**))) == NULL){
		cerr << "Nivel::cargar(): Memoria insuficiente" << endl;
		exit(1);
	}
	
	for(int i = 0; i < 4; i++){		
		if((mapa[i] = (Tile**)malloc(alto_ * sizeof(Tile*))) == NULL){
			cerr << "Nivel::cargar(): Memoria insuficiente" << endl;
			exit(1);
		}
		
		for(int j = 0; j < alto_; j++){
			if((mapa[i][j] = (Tile*)malloc(ancho_ * sizeof(Tile))) == NULL){
				cerr << "Nivel::cargar(): Memoria insuficiente" << endl;
			}
		}
	}
	
	
	
	// Guardamos las 4 capas en el mapa
	
	vector<ticpp::Element*> capas;
	vector<ticpp::Element*> tiles_capa;
	
	// Buscamos las capas
	
	p_nivel.encontrar("layer", capas);
	
	int capa = 0;
	int fila = 0;
	int columna = 0;
	int n = 0;
	Tile tile;
	
	// Para cada capa rellenamos la matriz del mapa
	
	for(vector<ticpp::Element*>::iterator i = capas.begin(); i != capas.end(); i++){
		// Vector con todos los tiles de cada mapa
		p_nivel.encontrar("tile", tiles_capa, *i);
		
		for(vector<ticpp::Element*>::iterator j = tiles_capa.begin(); j != tiles_capa.end(); j++){
			p_nivel.atributo("gid", *j, &tile);
			fila = n / ancho_;
			columna = (n % ancho_) % ancho_;
			mapa[capa][fila][columna] = tile;
			n++;
		}
		
		n = 0;
		tiles_capa.clear();
		capa++;
	}
	

	// Comenzamos al principio del nivel
	x = 0;
	y = alto_ * tile_alto_ - juego_->univ()->pantalla_alto();

	// Cargamos los actores
	// Leemos el XML del Nivel y sacamos qué tiles corresponden a qué enemigos
	// Creamos un map<Tile, string*>
	// Recorremos la capa 4 y según sea la string cargamos un Enemigo u otro en las coordenadas indicadas
	
	//Tener un registro de enemigos nos evitar hacer lecturas de memoria secundaria
	
	map<Tile, Enemigo*> Enemigos;
	
	for(vector<ticpp::Element*>::iterator i = propiedades.begin(); i != propiedades.end(); i++){

		// Si está el harrier que va de izquierda a derecha
		if(p_nivel.atributo("name", *i) == "harrierizq"){
			p_nivel.atributo("value", *i, &tile);	
			Enemigos[tile] = new Harrier(juego_, "XML/harrier.xml");
		}
		
		// Si está el harrier que va de derecha a izquierda
		if(p_nivel.atributo("name", *i) == "harrierdrch"){
			p_nivel.atributo("value", *i, &tile);	
			Enemigos[tile] = new Harrier(juego_, "XML/harrier.xml");
			Enemigos[tile]->vel_x(Enemigos[tile]->vel_x() * -1);
		}
		
		// Si está el aguila
		if(p_nivel.atributo("name", *i) == "aguila"){
			p_nivel.atributo("value", *i, &tile);	
			Enemigos[tile] = new Aguila(juego_, "XML/aguila.xml");
		}
	}
		
	//cargar_actores();
	
	map<Tile, Enemigo*>:: iterator k;
	Enemigo* enemigo;
	
	// Recorremos la capa 3 del mapa y colocamos a los enemigos
	for(int i = 0; i < alto_; i++){
		for(int j = 0; j < ancho_; j++){
			k = Enemigos.find(mapa[3][i][j]);
			if(k != Enemigos.end()){
				// Tenemos que añadir un enemigo en la lista_enemigos
				// Copiamos un enemigo
				// Modificamos su posicion
				// Lo insertamos
				enemigo = k->second->copia();
				enemigo->pos_x(j * tile_alto_);
				enemigo->pos_y(i * tile_ancho_);
				juego_->add_enemigo(enemigo);
			}
		}
	}
	
	// Limpiamos el buffer de enemigos
	for(map<Tile, Enemigo*>:: iterator k = Enemigos.begin(); k != Enemigos.end(); k++){
		delete k->second;
	}
	Enemigos.clear();
}

Nivel::~Nivel()
{
	if(mapa){
		free(**mapa);
		free(*mapa);
		free(mapa);
		mapa = NULL;
	}
	
	delete tileset;	
}


void Nivel::dibujar(SDL_Surface* superficie, int capa)
{
	int lx, ly, margen_x, margen_y, num_bloques_x, num_bloques_y;
	int tile, pos_x, pos_y;
	
	// Posiciones
	lx = x / tile_ancho_;
	ly = y / tile_alto_;

	// Número de bloques a dibujar
	num_bloques_x = ancho_;
	num_bloques_y = alto_;
	
	// Cálculo del sobrante
	margen_y = y % tile_ancho_;
	margen_x = x % tile_alto_;
	
	if(margen_x)
		num_bloques_x++;
	if(margen_y)
		num_bloques_y++;
	
	//cout << "y " << y << " ly " << ly << " alto_ " << alto_ << endl;
	
	for(int col = 0; (col + lx) < ancho_; col++){
		for(int fil = 0; (fil + ly) < alto_; fil++){
			tile = mapa[capa][fil + ly][col + lx] - 1;
			if(tile != -1){
				pos_x = col * tile_ancho_ - margen_x;
				pos_y = fil * tile_ancho_ - margen_y;
				tileset->dibujar(superficie, tile, pos_x, pos_y);
			}
		}
		
	}
}

void Nivel::mover(int x, int y)
{
	this->x = x;
	this->y = y;
}

void Nivel::cargar_actores()
{
	Harrier* h;
	
	h = new Harrier(juego_, string("harrier.xml"),  400, 2200);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  20, 2200);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  0, 1600);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  600, 1600);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  0, 1400);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  600, 1400);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  400, 1200);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  0, 1200);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  200, 1200);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  600, 1200);
	juego_->add_enemigo(h);
	
	h = new Harrier(juego_, "harrier.xml",  400, 800);
	juego_->add_enemigo(h);
}

