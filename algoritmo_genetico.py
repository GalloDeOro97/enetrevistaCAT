import random
import numpy as np
from operadores_geneticos import (
    seleccion_por_torneo,
    seleccion_por_ruleta,
    cruza_uniforme,
    order_crossover,
    mutacion_intercambio_reciproco,
    mutacion_desplazamiento,
    reproduccion_poblacion,
    reparar_hijo
)
import pandas as pd
def algoritmo_genetico(poblacion, funcion_seleccion, funcion_cruza, funcion_mutacion, funcion_reproduccion, generaciones=100):
    for _ in range(generaciones):
        poblacion_seleccionada = funcion_seleccion(poblacion)
        nueva_poblacion = funcion_reproduccion(poblacion_seleccionada, funcion_cruza, funcion_mutacion, reparar_hijo)
        poblacion = funcion_seleccion(nueva_poblacion)
    return poblacion

def generar_poblacion(tamaño_poblacion, ciudades):
    poblacion = []
    for _ in range(tamaño_poblacion):
        permutacion = random.sample(ciudades, len(ciudades))
        poblacion.append(permutacion)
    return poblacion

def calcular_distancia(permutacion, matriz_distancias):
    distancia_total = 0
    for i in range(len(permutacion) - 1):
        ciudad_origen = permutacion[i]
        ciudad_destino = permutacion[i+1]
        distancia_total += matriz_distancias[ciudad_origen][ciudad_destino]
    ciudad_origen = permutacion[-1]
    ciudad_destino = permutacion[0]
    distancia_total += matriz_distancias[ciudad_origen][ciudad_destino]
    return distancia_total

def mejor_ruta(poblacion, matriz_distancias):
    mejor_individuo = min(poblacion, key=lambda x: calcular_distancia(x, matriz_distancias))
    mejor_costo = calcular_distancia(mejor_individuo, matriz_distancias)
    return mejor_individuo, mejor_costo

def obtener_resultados(ciudades, matriz_distancias, tamaño_poblacion=10, generaciones=10):
    funciones_seleccion = [seleccion_por_torneo, seleccion_por_ruleta]
    funciones_cruza = [cruza_uniforme, order_crossover]
    funciones_mutacion = [mutacion_intercambio_reciproco, mutacion_desplazamiento]
    
    resultados = []

    for s in funciones_seleccion:
        for c in funciones_cruza:
            for m in funciones_mutacion:
                encabezado = f"{s.__name__.split('_')[2][0].upper()}{c.__name__.split('_')[1][0].upper()}{m.__name__.split('_')[1][0].upper()}"
                for ejecucion in range(1, 11):  # Realizar 10 ejecuciones
                    poblacion = generar_poblacion(tamaño_poblacion, ciudades)
                    poblacion_final = algoritmo_genetico(
                        poblacion,
                        lambda p: s(p, matriz_distancias, len(p)),
                        c,
                        m,
                        reproduccion_poblacion,
                        generaciones=generaciones
                    )
                    
                    ruta_optima, costo_optimo = mejor_ruta(poblacion_final, matriz_distancias)
                    resultados.append({
                        "Ejecución": ejecucion,
                        "Combinación": encabezado,
                        "Resultado": f"{ruta_optima}, {costo_optimo}"
                    })

    df_resultados = pd.DataFrame(resultados)
    return df_resultados

if __name__ == "__main__":
   # ciudades = [0, 1, 2, 3, 4, 5]
    
    #matriz_distancias = np.array([
     #   [0, 300, 180, 300, 460, 250],
      #  [300, 0, 160, 140, 360, 150],
       # [180, 160, 0, 200, 290, 100],
       # [300, 140, 200, 0, 200, 150],
       # [460, 360, 290, 200, 0, 360], 
       # [250, 150, 100, 150, 360, 0]
   # ])

    ciudades = [0 ,1, 2, 3, 4]

    matriz_distancias = np.array([
         [0, 2, 1, 10, 25],
         [2, 0, 18, 5, 18],
         [1, 18, 0, 10, 20],
         [10, 5, 10, 0, 7],
         [25, 18, 20, 7, 0]
     ])
    
    df_resultados = obtener_resultados(ciudades, matriz_distancias)
    print(df_resultados)
    df_resultados.to_csv("resultados_algoritmo_genetico.csv", index=False)
