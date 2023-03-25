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

# definir la población
def generar_jugador():
    jugador = {}
    for posicion, caracteristicas in Jugador.items():
        jugador[posicion] = {}
        for caracteristica in caracteristicas:
            jugador[posicion][caracteristica] = np.round(random.uniform(0.70, 0.99),2)
    return jugador.get("atributos")

def aptitud(poblacion, jugador_ideal):
    similitud_max = -math.inf
    jugador_mas_similar = None
    for equipo in poblacion:
        indice = 0
        for jugador in equipo:
            similitud = 0
            for caracteristica in GENES:
                    similitud += abs(min(jugador[caracteristica] - jugador_ideal[caracteristica], 0))
            if similitud > similitud_max:
                similitud_max = similitud
                print(similitud)
                jugador_mas_similar = jugador
                equipo.pop(indice)
            indice+=1
    return jugador_mas_similar

def jugador_mas_similar(jugadores, jugador_ideal):
    similitud_max = -math.inf
    jugador_mas_similar = None
    indice = 0
    for jugador in jugadores:
        similitud = np.float64(0)
        for caracteristica in GENES:
                simprev=(jugador_ideal[caracteristica]-jugador[caracteristica])
                similitud += max(simprev,0)
                # print(similitud)
                print(caracteristica, jugador[caracteristica], jugador_ideal[caracteristica], similitud)
        if similitud > similitud_max:
            similitud_max = similitud
            jugador_mas_similar = jugador
            jugadores.pop(indice)
        indice+=1
    return jugador_mas_similar

def generacionIndividual(cantidad, tam):
    equipos = []
    for individuo in range(cantidad):
        equipo = [generar_jugador() for _ in range(tam)]
        equipos.append(equipo)
    print("Cantidad equipos : ", len(equipos))
    print("Jugadores por rquipo : ", len(equipos[0]))
    return equipos


def seleccion():
    conjunto1 = Poblacion[(random.randint(0, len(Poblacion)-1))]
    conjunto2 = Poblacion[(random.randint(0, len(Poblacion)-1))]
    return conjunto1, conjunto2 

def cruza(padre1,padre2):
    n = len(padre1)
    punto1 = random.randint(0, n-1)
    punto2 = random.randint(0, n-1)
    punto3 = random.randint(0, n-1)
    punto4 = random.randint(0, n-1)
    puntos = sorted([punto1, punto2, punto3, punto4])
    hijo1 = padre1[:puntos[0]] + padre2[puntos[0]:puntos[1]] + padre1[puntos[1]:puntos[2]] + padre2[puntos[2]:puntos[3]] + padre1[puntos[3]:]
    hijo2 = padre2[:puntos[0]] + padre1[puntos[0]:puntos[1]] + padre2[puntos[1]:puntos[2]] + padre1[puntos[2]:puntos[3]] + padre2[puntos[3]:]
    return [hijo1, hijo2]

def mutacion(individuo, probabilidad_mutacion):
    if random.random() < probabilidad_mutacion:
        random.shuffle(individuo)
    return individuo

def diferencias(generaciones):
    poblacionPt = generaciones[0].copy()
    poblacionDf = generaciones[0].copy()
    poblacionMd = generaciones[0].copy()
    poblacionDl = generaciones[0].copy()

    mejores = []
    evaluacionesPorteros = [jugador_mas_similar(poblacionPt, JugadorIdeal.Portero) for jugador in range(4)]
    evaluacionesDenfensas = [jugador_mas_similar(poblacionDf, JugadorIdeal.Defensa) for jugador in range(4)]
    evaluacionesMedios = [jugador_mas_similar(poblacionMd, JugadorIdeal.Medio) for jugador in range(4)]
    evaluacionesDelanteros = [jugador_mas_similar(poblacionDl, JugadorIdeal.Delantero) for jugador in range(4)]
    
    mejores.append(evaluacionesPorteros)
    mejores.append(evaluacionesDenfensas)
    mejores.append(evaluacionesMedios)
    mejores.append(evaluacionesDelanteros)

    return mejores
        

def genetico(probabilidad_mutacion, num_generaciones, Poblacion):

    generaciones = []

    for generacion in range(num_generaciones):
        #Seleccion
        seleccionados = seleccion()
        #print(seleccionados,"*")
        
        #Cruza
        padre = seleccionados[1]
        madre = seleccionados[0]
        #hijo = cruzar(padre,madre,nueva_poblacion)
        hijo = cruza(padre, madre)

        #Mutación
        for i in range(len(hijo)):
            hijo[i] = mutacion(hijo[i], probabilidad_mutacion)
        #Poda
        Poblacion = [madre, padre , hijo[1] , hijo[0]]
        generaciones.append(Poblacion)

    print(len(Poblacion))
    # primera_generacion = diferencias(generaciones)
    
    PoblacionParaEvaluarPorteros = Poblacion.copy()
    # PoblacionParaEvaluarDefensas = Poblacion.copy()
    # PoblacionParaEvaluarMedios = Poblacion.copy()
    # PoblacionParaEvaluarDelanteros = Poblacion.copy()

    # mejores = []
    evaluacionesPorteros = [aptitud(PoblacionParaEvaluarPorteros, JugadorIdeal.Portero) for jugador in range(4)]
    # evaluacionesDenfensas = [jugador_mas_similar(PoblacionParaEvaluarDefensas, JugadorIdeal.Defensa) for jugador in range(4)]
    # evaluacionesMedios = [jugador_mas_similar(PoblacionParaEvaluarMedios, JugadorIdeal.Medio) for jugador in range(4)]
    # evaluacionesDelanteros = [jugador_mas_similar(PoblacionParaEvaluarDelanteros, JugadorIdeal.Delantero) for jugador in range(4)]
    
    # mejores.append(evaluacionesPorteros)
    # mejores.append(evaluacionesDenfensas)
    # mejores.append(evaluacionesMedios)
    # mejores.append(evaluacionesDelanteros)
    for portero in evaluacionesPorteros:
        print (portero)
    # return [mejores,primera_generacion]

Poblacion = generacionIndividual(4,20)
PROBABILIDAD_MUTACION = 0.5
NUM_GENERACIONES = 1
mejores_jugadores = genetico( PROBABILIDAD_MUTACION, NUM_GENERACIONES, Poblacion)

