import random
import math
import numpy as np
from ideal import JugadorIdeal

# Atributos de los jugadores
GENES = ["altura", "agilidad", "reflejos", "velocidad", "técnica", 
         "visión", "fisico", "ppp", "distancia_de_lanzamiento", "distancia_de_tiro"]

#Clase con el Jugador Ideal de cada posicion
Modelo = JugadorIdeal
Jugador = {
    "atributos":GENES
}
Jugadores = []

# definir la población
def generar_jugador():
    jugador = {}
    for posicion, caracteristicas in Jugador.items():
        jugador[posicion] = {}
        for caracteristica in caracteristicas:
            jugador[posicion][caracteristica] = np.round(random.uniform(0.70, 0.99),2)
    Jugadores.append(jugador.get("atributos"))
    return jugador

def jugador_mas_similar(jugadores, jugador_ideal):
    similitud_max = -math.inf
    jugador_mas_similar = None
    for jugador in jugadores:
        similitud = 0
        for caracteristica in GENES:
                similitud += abs(jugador[caracteristica] - jugador_ideal[caracteristica])
        if similitud > similitud_max:
            similitud_max = similitud
            jugador_mas_similar = jugador
    return jugador_mas_similar

GenerarJugadores = [generar_jugador() for _ in range(40)]
Poblacion = []


def generar_individuos():
    cantidad_jugadores = 4
    inicio = 0
    extremo = 4
    cantidad_defensas = int(len(Jugadores) / cantidad_jugadores)
    for a in range(cantidad_defensas):
        Poblacion.append(Jugadores[inicio:extremo])
        inicio += 4
        extremo += 4

generar_individuos()

def seleccion():
    conjunto1 = Poblacion[(random.randint(0, len(Poblacion)-1))]
    conjunto2 = Poblacion[(random.randint(0, len(Poblacion)-1))]
    return conjunto1, conjunto2
            

def cruza(padre,madre, np):
    padre1 = padre[:2]
    padre2 = padre[2:4]
    madre1 = madre[:2]
    madre2 = madre[2:4]
    hijo1 = padre2 + madre1
    hijo2 = madre2 + padre1
    np.append(hijo1)
    np.append(hijo2)

def mutacion(equipo, probabilidad_mutacion):

    if random.random() < probabilidad_mutacion:
        equipo.pop(0)
        equipo.insert(0, generar_jugador().get("atributos"))
    return equipo

        

        

def genetico(probabilidad_mutacion, num_generaciones):

    for generacion in range(num_generaciones):
        
        #Seleccion
        seleccionados = seleccion()
        
        #Cruza
        nueva_poblacion = []
        padre = seleccionados[1]
        madre = seleccionados[0]
        hijo = cruza(padre, madre, nueva_poblacion)

        #Mutación
        for i in range(len(nueva_poblacion)):
            nueva_poblacion[i] = mutacion(nueva_poblacion[i], probabilidad_mutacion)
        #Poda
        Poblacion = seleccionados[0] + seleccionados[1] + nueva_poblacion[1] + nueva_poblacion[0]

    mejorPortero = jugador_mas_similar(Poblacion, JugadorIdeal.Portero)
    mejorDefensa = jugador_mas_similar(Poblacion, JugadorIdeal.Defensa)
    mejorMedio = jugador_mas_similar(Poblacion, JugadorIdeal.Medio)
    mejorDelantero = jugador_mas_similar(Poblacion, JugadorIdeal.Delantero)

    mejores = []
    mejores.append(mejorPortero)
    mejores.append(mejorDefensa)
    mejores.append(mejorMedio)
    mejores.append(mejorDelantero)

    return mejores


# PROBABILIDAD_MUTACION = 0.4
# NUM_GENERACIONES = 10
# mejores_jugadores = genetico( PROBABILIDAD_MUTACION, NUM_GENERACIONES)
# posiciones = ["Portero", "Defensa", "Medio", "Delantero"]
# print("Equipo:")

# for posicion in posiciones:
#     caracteristicas = mejores_jugadores[(posiciones.index(posicion))]
#     print(f"{posicion}:")
#     for caracteristica, valor in caracteristicas.items():
#         print(f" - {caracteristica}: {valor:.2f}")