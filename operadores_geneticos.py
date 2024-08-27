import random
import numpy as np

ciudades = [0, 1, 2, 3, 4, 5]

def calcular_distancia(permutacion, matriz_distancias):
    distancia_total = 0
    for i in range(len(permutacion) - 1):
        ciudad_origen = ciudades.index(permutacion[i])
        ciudad_destino = ciudades.index(permutacion[i+1])
        distancia_total += matriz_distancias[ciudad_origen][ciudad_destino]
    ciudad_origen = ciudades.index(permutacion[-1])
    ciudad_destino = ciudades.index(permutacion[0])
    distancia_total += matriz_distancias[ciudad_origen][ciudad_destino]
    return distancia_total

def seleccion_por_torneo(poblacion, matriz_distancias, tamaño_poblacion_seleccionada, tamaño_torneo=2):
    ganadores = []
    for _ in range(tamaño_poblacion_seleccionada):
        torneo = random.sample(poblacion, tamaño_torneo)
        ganador = min(torneo, key=lambda x: calcular_distancia(x, matriz_distancias))
        ganadores.append(ganador)
    return ganadores

def seleccion_por_ruleta(poblacion, matriz_distancias, tamaño_poblacion_seleccionada, tamaño_torneo=None):
    probabilidades = [1 / len(poblacion)] * len(poblacion)

    seleccionados = []
    for _ in range(tamaño_poblacion_seleccionada):
        r = random.random()
        acumulado = 0
        for individuo, probabilidad in zip(poblacion, probabilidades):
            acumulado += probabilidad
            if acumulado >= r:
                seleccionados.append(individuo)
                break
    return seleccionados

def mutacion_intercambio_reciproco(individuo):
    a, b = random.sample(range(len(individuo)), 2)
    individuo[a], individuo[b] = individuo[b], individuo[a]
    return individuo

def mutacion_desplazamiento(individuo):
    start, end = sorted(random.sample(range(len(individuo)), 2))
    subsecuencia = individuo[start:end+1]
    restante = individuo[:start] + individuo[end+1:]
    insert_position = random.randint(0, len(restante))
    individuo_mutado = restante[:insert_position] + subsecuencia + restante[insert_position:]
    return individuo_mutado

def order_crossover(padre1, padre2):
    tamaño = len(padre1)
    inicio, fin = sorted(random.sample(range(tamaño), 2))
    hijo1 = [None] * tamaño
    hijo2 = [None] * tamaño
    hijo1[inicio:fin+1] = padre2[inicio:fin+1]
    hijo2[inicio:fin+1] = padre1[inicio:fin+1]

    def llenar_hijo(hijo, padre):
        posición = (fin + 1) % tamaño
        for gen in padre:
            if gen not in hijo:
                while hijo[posición] is not None:
                    posición = (posición + 1) % tamaño
                hijo[posición] = gen

    llenar_hijo(hijo1, padre1)
    llenar_hijo(hijo2, padre2)

    return hijo1, hijo2

def cruza_uniforme(padre1, padre2):
    tamaño = len(padre1)
    hijo1, hijo2 = [-1]*tamaño, [-1]*tamaño
    
    for i in range(tamaño):
        if random.random() < 0.5:
            hijo1[i] = padre1[i]
            hijo2[i] = padre2[i]
        else:
            hijo1[i] = padre2[i]
            hijo2[i] = padre1[i]
    
    hijo1 = reparar_hijo(hijo1, padre1, padre2)
    hijo2 = reparar_hijo(hijo2, padre1, padre2)
    
    return hijo1, hijo2

def reparar_hijo(hijo, padre1, padre2):
    tamaño = len(hijo)
    genes_faltantes = list(set(padre1) - set(hijo))
    genes_repetidos = [gen for gen in hijo if hijo.count(gen) > 1]
    
    for i in range(tamaño):
        if hijo[i] in genes_repetidos:
            if genes_faltantes:
                hijo[i] = genes_faltantes.pop()
                if hijo[i] in genes_repetidos:
                    genes_repetidos.remove(hijo[i])
    
    for i in range(tamaño):
        if hijo.count(hijo[i]) > 1 and genes_faltantes:
            hijo[i] = genes_faltantes.pop()
    
    return hijo

def reproduccion_poblacion(poblacion, funcion_cruza, funcion_mutacion, funcion_reparacion):
    tamaño_inicial = len(poblacion)
    if tamaño_inicial % 2 != 0:
        poblacion.append(poblacion[0])

    nueva_poblacion = []

    for i in range(0, len(poblacion), 2):
        padre1, padre2 = poblacion[i], poblacion[i + 1]
        hijo1, hijo2 = funcion_cruza(padre1, padre2)

        if funcion_cruza.__name__ == 'cruza_uniforme':
            hijo1 = funcion_reparacion(hijo1, padre1, padre2)
            hijo2 = funcion_reparacion(hijo2, padre1, padre2)

        if random.random() < 0.5:
            hijo1 = funcion_mutacion(hijo1)
        if random.random() < 0.5:
            hijo2 = funcion_mutacion(hijo2)

        nueva_poblacion.extend([hijo1, hijo2])

    if len(nueva_poblacion) > tamaño_inicial:
        nueva_poblacion = nueva_poblacion[:tamaño_inicial]

    return nueva_poblacion
