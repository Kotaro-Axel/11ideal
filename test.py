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
def generar_player(ideal):
    jugador = {}
    for posicion, caracteristicas in Jugador.items():
        jugador[posicion] = {}
        for caracteristica in caracteristicas:
            jugador[posicion][caracteristica] = np.round(
                random.uniform(ideal[caracteristica]-0.3, ideal[caracteristica]+0.3),2
                )
            #jugador[posicion]['id'] = 5
    return jugador.get("atributos")
    


def generar_jugador():
    jugador = {}
    for posicion, caracteristicas in Jugador.items():
        jugador[posicion] = {}
        for caracteristica in caracteristicas:
            jugador[posicion][caracteristica] = np.round(random.uniform(0.70, 0.99),2)
    return jugador.get("atributos")

def aptitud(equipo, defensaideal, medioideal, delanteroideal, porteroideal):

    similitud_global = []  

    for defensas in equipo[:4]:
        diferencia = 0
        for caracteristica in GENES:
            diferencia += abs(min(defensas[caracteristica] - defensaideal[caracteristica], 0))
        similitud_global.append(diferencia)

    for medios in equipo[4:8]:
        diferencia = 0
        for caracteristica in GENES:
            diferencia += abs(min(medios[caracteristica] - medioideal[caracteristica], 0))
        similitud_global.append(diferencia)

    for delanteros in equipo[8:10]:
        diferencia = 0
        for caracteristica in GENES:
            diferencia += abs(min(delanteros[caracteristica] - delanteroideal[caracteristica], 0))
        similitud_global.append(diferencia)


    for portero in equipo[10:11]:
        diferencia = 0
        for caracteristica in GENES:
            diferencia += abs(min(portero[caracteristica] - porteroideal[caracteristica], 0))
        similitud_global.append(diferencia)

    return sum(similitud_global)

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
                # print(caracteristica, jugador[caracteristica], jugador_ideal[caracteristica], similitud)
        if similitud > similitud_max:
            similitud_max = similitud
            jugador_mas_similar = jugador
            jugadores.pop(indice)
        indice+=1
    return jugador_mas_similar

def generacionIndividual(cantidad):
    equipos = []
    defensas = 4    
    medios = 4
    delanteros = 2
    portero = 1

    equipo = []
    index = 1
    for plantilla in range(4):
        for defensa in range(defensas):
            jugador = generar_player(Modelo.Defensa)
            jugador["id"] = index
            equipo.append(jugador)
            index+=1

        for medio in range(medios):
            jugador = generar_player(Modelo.Medio)
            jugador["id"] = index
            equipo.append(jugador)
            index+=1

        for medio in range(delanteros):
            jugador = generar_player(Modelo.Delantero)
            jugador["id"] = index
            equipo.append(jugador)
            index+=1

        for medio in range(portero):
            jugador = generar_player(Modelo.Portero)
            jugador["id"] = index
            equipo.append(jugador)
            index+=1
    # print(len(equipo))

    for team in range(cantidad):
        randomize = equipo.copy() 
        random.shuffle(randomize)
        equipos.append(randomize)


    return equipos


def seleccion(Poblacion):

    individuos = []
    individuo = 0

    for equipo in Poblacion:
        individuo = aptitud(equipo, Modelo.Defensa, Modelo.Medio, Modelo.Delantero, Modelo.Portero)
        individuos.append(individuo)

    mejor = min(individuos)
    indice_mejor = individuos.index(mejor)
    conjunto1=Poblacion[indice_mejor]

    individuos.pop(indice_mejor)

    mejor = min(individuos)
    indice_mejor = individuos.index(mejor)
    conjunto2 = Poblacion[indice_mejor]

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

def cruza2(parent1, parent2):
    # 2 puntos de cruza entre el rango [1, 42]
    point1 = random.randint(1, 42)
    point2 = random.randint(point1 + 1, 43)

    # copiar los 2 padres
    child1 = parent1.copy()
    child2 = parent2.copy()

    for i in range(point1, point2):
        idx = [d['id'] for d in parent2].index(parent1[i]['id'])
        child1[i], child2[idx] = child2[idx], child1[i]

    for child in [child1, child2]:
        ids_seen = set()
        for i, d in enumerate(child):
            if d['id'] in ids_seen:
                max_id = max(ids_seen)
                unused_id = max_id + 1
                while unused_id in ids_seen:
                    unused_id += 1
                child[i]['id'] = unused_id
            else:
                ids_seen.add(d['id'])

    return [child1, child2]

def mutacion(individuo, probabilidad_mutacion):
    # random.shuffle(individuo)
    a,b=0,0
    n_mutaciones = 44

    if random.uniform(0,1) <= probabilidad_mutacion:
        for _ in range(n_mutaciones):
            if random.uniform(0,1) <= probabilidad_mutacion:
                a, b = random.randint(0,len(individuo)), random.randint(0,len(individuo))
                a,b=int(a-1),int(b-1)
                individuo[a], individuo[b] = individuo[b], individuo[a]

    
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
        seleccionados = seleccion(Poblacion)
        #print(seleccionados,"*")
        
        #Cruza
        padre = seleccionados[1]
        madre = seleccionados[0]
        #hijo = cruzar(padre,madre,nueva_poblacion)
        hijo = cruza2(padre, madre)

        #Mutación
        for i in range(len(hijo)):
            if random.random() < probabilidad_mutacion:
                # print("Habrá mutación en el hijo ",i)
                hijo[i] = mutacion(hijo[i], probabilidad_mutacion)
        #Poda
        Poblacion = [madre, padre , hijo[1] , hijo[0]]
        generaciones.append(Poblacion)
    
    i=0
    aptitudesmejor=[]
    aptitudespeor=[]
    aptitudesmedio=[]
    for poblacion in generaciones:
        aprendizaje = []
        aptitudEquipo = 0
        j=0
        for equipo in poblacion:
            j+=1
            aptitudEquipo = aptitud(equipo, Modelo.Defensa, Modelo.Medio, Modelo.Delantero, Modelo.Portero)
            # print(equipo,"\n","Aptitud: ",aptitudEquipo,"\n")
            # print("Aptitud: ","equipo ", j,aptitudEquipo,"\n")
        
            aprendizaje.append(aptitudEquipo)
        
        # print(i)
        i+=1
    # print(aprendizaje)

        aptitudesmejor.append(min(aprendizaje))
        aptitudespeor.append(max(aprendizaje))
        aptitudesmedio.append(np.mean(aprendizaje))
    
    mejor=min(aptitudesmejor)
    aptitudes=[aptitudesmejor,aptitudespeor,aptitudesmedio]
    
    mejor_generacion = generaciones[(aprendizaje.index(mejor))]

    UltimaGeneracion = Poblacion.copy()

    for equipo in UltimaGeneracion:
        aptitud(equipo, Modelo.Defensa, Modelo.Medio, Modelo.Delantero, Modelo.Portero)

    return [mejor_generacion,aptitudes]

Poblacion = generacionIndividual(10)
PROBABILIDAD_MUTACION = 0.5
NUM_GENERACIONES = 100

def initiate_genetic(PROBABILIDAD_MUTACION, NUM_GENERACIONES):
    mejores_jugadores=genetico(PROBABILIDAD_MUTACION, NUM_GENERACIONES, Poblacion)
    # print(mejores_jugadores[1])
    return mejores_jugadores


# mejores_jugadores = genetico( PROBABILIDAD_MUTACION, NUM_GENERACIONES, Poblacion)
# print(len(mejores_jugadores[0][0]))

# print(mejores_jugadores[1])
# mejor_generacion = mejores_jugadores[0]
# curva_aprendizaje = mejores_jugadores[1]

