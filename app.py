import random
from ideal import JugadorIdeal
import numpy as np

# Atributos de los jugadores
GENES = ["altura", "agilidad", "reflejos", "velocidad", "técnica", 
         "visión", "fisico", "ppp", "distancia_de_lanzamiento", "distancia_de_tiro"]

POSICIONES = {
    "Portero": GENES,
    "Defensa": GENES,
    "Medio": GENES,
    "Delantero": GENES
}

#Arrays de jugadores generados pos posicion (20 jugadores por arreglo)
Porteros=[]
Defensas=[]
Medios=[]
Delanteros=[]

#Clase con el Jugador Ideal de cada posicion
Modelo = JugadorIdeal


# definir la población
def generar_jugador():
    jugador = {}
    for posicion, caracteristicas in POSICIONES.items():
        jugador[posicion] = {}
        for caracteristica in caracteristicas:
            jugador[posicion][caracteristica] = random.uniform(0.1, 0.99)
    Porteros.append(jugador.get("Portero"))
    Defensas.append(jugador.get("Defensa"))
    Medios.append(jugador.get("Medio"))
    Delanteros.append(jugador.get("Delantero"))
    return jugador

POBLACION_INICIAL = [generar_jugador() for _ in range(20)]

#Ejemplo para optener el portero en la posicion 1 y su atributo "altura"
#print("Porteros :", Porteros[1]["altura"])
#---------------------------------------------------



#Ejemplo para Obtener todos los jugadores en la lista de medios y comparalos por genes.
#Funcion para evaluar Todos los jugadores de una posicion con el jugador ideal de esa posicion en base a sus genes
def evaluarJugadorModelo(jugadores):
    for medio in Medios:
        #print("Jugador : " , jugador)
        for genes in GENES:
            jugador = np.round(medio[genes], 2)
            modelo = np.round(Modelo.Medio[genes],2)

#Suma todos los valores de las caracteristicas de un jugador y retorna la suma
def evaluarJugador(jugador):
    puntaje=0
    for genes in GENES:
        caracteristicas = np.round(jugador[genes], 2)
        puntaje += caracteristicas
    return puntaje

#Funcion inconclusa, seleccion de los mejores jugadores
def seleccionar():       
    #ejemplo de evaluacion
    #se evalua cada jugador del arreglo de "Medios"
    evaluaciones = [evaluarJugador(medio) for medio in Medios]
    #print(np.round(evaluaciones,2))
    #Se imprime el valor maximo hayado (valor maximo de la suma de la funcion evaluarJugador())
    print(max(evaluaciones))
    #Se imprime la posicion del jugador hayado con el valor maximo en la suma
    print("Max :", evaluaciones.index(max(evaluaciones)))
    #Se imprime todo el jugador (diccionario de jugador con sus caracteristicas)
    print(Medios[evaluaciones.index(max(evaluaciones))])



# definir la función de evaluación (puntaje)
def evaluar(jugador):
    puntaje = 0
    for posicion, caracteristicas in POSICIONES.items():
        posicion_puntaje = 0
        for caracteristica in caracteristicas:
            posicion_puntaje += jugador[posicion][caracteristica]
        puntaje += posicion_puntaje
    return puntaje


def seleccionar(poblacion):
    evaluaciones = [evaluar(jugador) for jugador in poblacion]
    max_puntaje = max(evaluaciones)
    seleccionados = []
    for i in range(len(poblacion)):
        if random.uniform(0, 1) < (evaluaciones[i] / max_puntaje):
            seleccionados.append(poblacion[i])
    return seleccionados

def cruzar(padre, madre):
    hijo = {}
    for posicion in POSICIONES.keys():
        hijo[posicion] = {}
        for caracteristica in POSICIONES[posicion]:
            if random.random() < 0.5:
                hijo[posicion][caracteristica] = padre[posicion][caracteristica]
            else:
                hijo[posicion][caracteristica] = madre[posicion][caracteristica]
    return hijo

def mutar(jugador, probabilidad_mutacion):
    mutado = jugador.copy()
    for posicion in POSICIONES.keys():
        for caracteristica in POSICIONES[posicion]:
            if random.random() < probabilidad_mutacion:
                mutado[posicion][caracteristica] = random.uniform(0, 1)
    return mutado

def algoritmo_genetico(poblacion, probabilidad_mutacion, num_generaciones):
    for generacion in range(num_generaciones):
        # selección
        seleccionados = seleccionar(poblacion)
        
        # cruce
        nueva_poblacion = []
        for i in range(len(seleccionados) // 2):
            padre = seleccionados[random.randint(0, len(seleccionados)-1)]
            madre = seleccionados[random.randint(0, len(seleccionados)-1)]
            hijo = cruzar(padre, madre)
            nueva_poblacion.append(hijo)
        
        # mutación
        for i in range(len(nueva_poblacion)):
            nueva_poblacion[i] = mutar(nueva_poblacion[i], probabilidad_mutacion)
        
        # reemplazo
        poblacion = seleccionados + nueva_poblacion
    
    # evaluación final
    evaluaciones = [evaluar(jugador) for jugador in poblacion]
    mejor_jugador = poblacion[evaluaciones.index(max(evaluaciones))]
    return mejor_jugador



POBLACION_INICIAL = [generar_jugador() for _ in range(20)]
PROBABILIDAD_MUTACION = 0.4
NUM_GENERACIONES = 10
mejor_jugador = algoritmo_genetico(POBLACION_INICIAL, PROBABILIDAD_MUTACION, NUM_GENERACIONES)

# imprimir el equipo resultante
print("Equipo:")
player=[]

def createplayer():
    for posicion in POSICIONES.keys():
        caracteristicas = mejor_jugador[posicion]
        print(f"{posicion}:")
        for caracteristica, valor in caracteristicas.items():
            print(f" - {caracteristica}: {valor:.2f}")
            player.append(valor)
    print(player.__len__())
    return player  


#Ejemplo de jugador generado
#""""'Portero': 
# {'altura': 0.30397156960088567, 
# 'agilidad': 0.5470272081147906, 
# 'reflejos': 0.47055859397806765, 
# 'velocidad': 0.7640728378419078, 
# 'técnica': 0.9688119228795901, 
# 'visión': 0.10856785725595852, 
# 'fisico': 0.900921325488214, 
# 'ppp': 0.049082822994364284, 
# 'distancia_de_lanzamiento': 0.9343541306300858,
#  'distancia_de_tiro': 0.7991211411944863},""""