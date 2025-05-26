import sys
from typing import List, Dict, Tuple, Optional

class Ruta:
    def __init__(self, nombre: str, ciudad1: str, ciudad2: str, 
                 tiempo_normal: int, tiempo_lluvia: int, 
                 tiempo_nieve: int, tiempo_tormenta: int):
        self.nombre = nombre
        self.ciudad1 = ciudad1
        self.ciudad2 = ciudad2
        self.tiempo_normal = tiempo_normal
        self.tiempo_lluvia = tiempo_lluvia
        self.tiempo_nieve = tiempo_nieve
        self.tiempo_tormenta = tiempo_tormenta

class Grafo:
    def __init__(self, rutas: List[Ruta]):
        self.rutas_originales = rutas.copy()
        self.ciudades = []
        self.indice_ciudad = {}
        self.matriz = []
        
        # Construir lista de ciudades únicas
        for ruta in rutas:
            if ruta.ciudad1 not in self.indice_ciudad:
                self.indice_ciudad[ruta.ciudad1] = len(self.ciudades)
                self.ciudades.append(ruta.ciudad1)
            if ruta.ciudad2 not in self.indice_ciudad:
                self.indice_ciudad[ruta.ciudad2] = len(self.ciudades)
                self.ciudades.append(ruta.ciudad2)
        
        self._construir_matriz()
    
    def _construir_matriz(self):
        n = len(self.ciudades)
        infinito = sys.maxsize // 2
        self.matriz = [[infinito] * n for _ in range(n)]
        
        # Inicializar diagonal con 0
        for i in range(n):
            self.matriz[i][i] = 0
        
        # Llenar matriz con tiempos normales
        for ruta in self.rutas_originales:
            i = self.indice_ciudad[ruta.ciudad1]
            j = self.indice_ciudad[ruta.ciudad2]
            self.matriz[i][j] = ruta.tiempo_normal
            self.matriz[j][i] = ruta.tiempo_normal
    
    def obtener_matriz(self) -> List[List[int]]:
        return self.matriz
    
    def obtener_ciudades(self) -> List[str]:
        return self.ciudades.copy()
    
    def obtener_rutas_originales(self) -> List[Ruta]:
        return self.rutas_originales.copy()
    
    def actualizar_ruta(self, ciudad1: str, ciudad2: str, tiempo: int):
        i = self.indice_ciudad[ciudad1]
        j = self.indice_ciudad[ciudad2]
        self.matriz[i][j] = tiempo
        self.matriz[j][i] = tiempo
    
    def obtener_peso(self, ciudad1: str, ciudad2: str) -> int:
        i = self.indice_ciudad[ciudad1]
        j = self.indice_ciudad[ciudad2]
        return self.matriz[i][j]
class AlgortimoFloyd:
    def __init__(self):
        self.distancias = []
        self.siguiente = []
        self.infinito = sys.maxsize 
    
    def calcular(self, matriz: List[List[int]]):
        n = len(matriz)
        self.distancias = [fila.copy() for fila in matriz]
        self.siguiente = [[0] * n for _ in range(n)]
        
        # Inicializar matriz siguiente
        for i in range(n):
            for j in range(n):
                if i != j and matriz[i][j] < self.infinito:
                    self.siguiente[i][j] = j
                else:
                    self.siguiente[i][j] = -1
        
        # Algoritmo de Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if self.distancias[i][k] + self.distancias[k][j] < self.distancias[i][j]:
                        self.distancias[i][j] = self.distancias[i][k] + self.distancias[k][j]
                        self.siguiente[i][j] = self.siguiente[i][k]
    
    def obtener_distancia(self, i: int, j: int) -> int:
        return self.distancias[i][j]
    
    def obtener_ruta_indices(self, origen: int, destino: int) -> List[int]:
        if self.siguiente[origen][destino] == -1:
            return []
        
        ruta = []
        actual = origen
        while actual != destino:
            ruta.append(actual)
            actual = self.siguiente[actual][destino]
        ruta.append(destino)
        return ruta


