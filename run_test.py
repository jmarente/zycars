#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
  @mainpage Zycars v1.0
  @author José J. Marente Florín
  
  <p style="text-align: center;"><img src="http://zycars.googlecode.com/svn/trunk/multimedia/image/menu/logo_menu.png" width=550px></p>

  <h2>¿Qué es Zycars?</h2>

  <p style="text-align: justify;">
    Es un juego de carreras en dos dimensiones con vista cenital, en el que se podrá competir contra 
    coches dirigidos por el ordenador. Está compuesto por varios modos de juego.
  </p>

  <p style="text-align: justify;">
    A lo largo de los circuitos en los que estemos compitiendo contra la inteligencia artificial, podremos
    encontrar distintas cajas que al colisionar con ellas nos proporcionen aleatoriamente una habilidad o
    ítem que nos ayuden en la competición contra nuestros rivales.
  </p>

  <h2>Autores</h2>

  <ul>
      <li>
          <strong><a href="http://code.google.com/p/zycars/" target="_blank">José Jesús Marente Florín</a></strong>:
          <ul>
              <li>Desarrollo</li>
          </ul>
      </li>
      <li>
          <strong><a href="http://www.deividart.com" target="_blank">David Nieto Rojas</a></strong>:
          <ul>
              <li>Diseño gráfico</li>
          </ul>
      </li>
      <li>
          <strong><a href="http://www.jamendo.com" target="_blank">Jamendo - Música</a></strong>:
          <ul>
              <li>Bob Wizman </li>
              <li>Pirato Ketchup</li>
              <li>Los Cadaver </li>
              <li>The Wavers</li>
              <li>Zamalska </li>
          </ul>
      </li>
  </ul>

  <h2>Licencia</h2>

  <ul>
      <li><b>Código fuente</b>: GPL v3
      <li><b>Ficheros multimedia</b>: Creative Commons 3.0 Atribución -
      No comercial - Compartir igual.</li>
  </ul>
'''

from engine import game

def main():
    '''
    @brief Función main del juego.
    '''
    zycars = game.Game()
    zycars.run()
    
if __name__ == "__main__":
    main()
