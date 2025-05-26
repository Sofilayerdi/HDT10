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
        
        for i in range(n):
            self.matriz[i][i] = 0
        
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
    
class AnalizadorArchivo:
    @staticmethod
    def analizar(nombre_archivo: str) -> List[Ruta]:
        rutas = []
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                
                partes = linea.split()
                if len(partes) != 6:
                    raise ValueError(f"Línea mal formada: {linea}")
                
                ciudad1 = partes[0]
                ciudad2 = partes[1]
                tiempo_normal = int(partes[2])
                tiempo_lluvia = int(partes[3])
                tiempo_nieve = int(partes[4])
                tiempo_tormenta = int(partes[5])
                
                nombre = f"{ciudad1}To{ciudad2}"
                rutas.append(Ruta(nombre, ciudad1, ciudad2, 
                                tiempo_normal, tiempo_lluvia, 
                                tiempo_nieve, tiempo_tormenta))
        return rutas

class main:
    def __init__(self):
        self.grafo = None
        self.floyd = AlgortimoFloyd()
        self.archivo_datos = "logistica.txt"
    
    def ejecutar(self):
        try:
            rutas = AnalizadorArchivo.analizar(self.archivo_datos)
            self.grafo = Grafo(rutas)
            self.floyd.calcular(self.grafo.obtener_matriz())
            
            salir = False
            while not salir:
                self.mostrar_menu()
                opcion = self.leer_opcion()
                
                if opcion == 1:
                    self.ruta_mas_corta()
                elif opcion == 2:
                    self.centro_grafo()
                elif opcion == 3:
                    self.modificar_grafo()
                elif opcion == 4:
                    print("\n¡Gracias por usar el programa de optimización de rutas!")
                    salir = True
                else:
                    print("\nOpción no válida. Intente nuevamente.")
        
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.archivo_datos}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
    
    def mostrar_menu(self):
        print("\n=====================================")
        print("\nSistema de Optimización de Rutas Logísticas\n")
        print("1. Ruta más corta entre dos ciudades")
        print("2. Centro del grafo")
        print("3. Modificar grafo")
        print("4. Salir")
        print("\nElija una opción: ", end="")
    
    def leer_opcion(self) -> int:
        try:
            return int(input().strip())
        except ValueError:
            return -1
    
    def ruta_mas_corta(self):
        ciudades = self.grafo.obtener_ciudades()
        print("\nCiudades disponibles:")
        for idx, ciudad in enumerate(ciudades):
            print(f"{idx}: {ciudad}")
        
        try:
            origen_idx = int(input("\nIngrese el índice de la ciudad origen: "))
            destino_idx = int(input("Ingrese el índice de la ciudad destino: "))
            
            if origen_idx < 0 or origen_idx >= len(ciudades) or destino_idx < 0 or destino_idx >= len(ciudades):
                print("\nÍndice de ciudad no válido.")
                return
            
            self.floyd.calcular(self.grafo.obtener_matriz())
            ruta_indices = self.floyd.obtener_ruta_indices(origen_idx, destino_idx)
            
            if not ruta_indices:
                print(f"\nNo hay ruta entre {ciudades[origen_idx]} y {ciudades[destino_idx]}")
                return
            
            distancia = self.floyd.obtener_distancia(origen_idx, destino_idx)
            ruta_ciudades = [ciudades[i] for i in ruta_indices]
            
            print("\nRuta más corta:", " -> ".join(ruta_ciudades))
            print(f"Distancia total: {distancia} horas")
        
        except ValueError:
            print("\nEntrada no válida. Debe ingresar un número.")

class main:
    def __init__(self):
        self.grafo = None
        self.floyd = AlgoritmoFloyd()
        self.archivo_datos = "logistica.txt"
    
    def ejecutar(self):
        try:
            rutas = AnalizadorArchivo.analizar(self.archivo_datos)
            self.grafo = Grafo(rutas)
            self.floyd.calcular(self.grafo.obtener_matriz())
            
            salir = False
            while not salir:
                self.mostrar_menu()
                opcion = self.leer_opcion()
                
                if opcion == 1:
                    self.ruta_mas_corta()
                elif opcion == 2:
                    self.centro_grafo()
                elif opcion == 3:
                    self.modificar_grafo()
                elif opcion == 4:
                    print("\n¡Gracias por usar el programa de optimización de rutas!")
                    salir = True
                else:
                    print("\nOpción no válida. Intente nuevamente.")
        
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.archivo_datos}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
    
    def mostrar_menu(self):
        print("\n=====================================")
        print("\nSistema de Optimización de Rutas Logísticas\n")
        print("1. Ruta más corta entre dos ciudades")
        print("2. Centro del grafo")
        print("3. Modificar grafo")
        print("4. Salir")
        print("\nElija una opción: ", end="")
    
    def leer_opcion(self) -> int:
        try:
            return int(input().strip())
        except ValueError:
            return -1
    
    def ruta_mas_corta(self):
        ciudades = self.grafo.obtener_ciudades()
        print("\nCiudades disponibles:")
        for idx, ciudad in enumerate(ciudades):
            print(f"{idx}: {ciudad}")
        
        try:
            origen_idx = int(input("\nIngrese el índice de la ciudad origen: "))
            destino_idx = int(input("Ingrese el índice de la ciudad destino: "))
            
            if origen_idx < 0 or origen_idx >= len(ciudades) or destino_idx < 0 or destino_idx >= len(ciudades):
                print("\nÍndice de ciudad no válido.")
                return
            
            self.floyd.calcular(self.grafo.obtener_matriz())
            ruta_indices = self.floyd.obtener_ruta_indices(origen_idx, destino_idx)
            
            if not ruta_indices:
                print(f"\nNo hay ruta entre {ciudades[origen_idx]} y {ciudades[destino_idx]}")
                return
            
            distancia = self.floyd.obtener_distancia(origen_idx, destino_idx)
            ruta_ciudades = [ciudades[i] for i in ruta_indices]
            
            print("\nRuta más corta:", " -> ".join(ruta_ciudades))
            print(f"Distancia total: {distancia} horas")
        
        except ValueError:
            print("\nEntrada no válida. Debe ingresar un número.")
        
        def centro_grafo(self):
            ciudades = self.grafo.obtener_ciudades()
            n = len(ciudades)
        
            if n == 0:
                print("\nNo hay ciudades en el grafo.")
            return
        
        self.floyd.calcular(self.grafo.obtener_matriz())
        
        centro_idx = -1
        minima_excentricidad = sys.maxsize
        
        print("\nCalculando centro del grafo...")
        print("\nExcentricidad para cada ciudad:")
        print("----------------------------------------")
        
        for i in range(n):
            maxima_distancia = 0
            
            for j in range(n):
                if i != j:
                    distancia = self.floyd.obtener_distancia(i, j)
                    if distancia < sys.maxsize // 2 and distancia > maxima_distancia:
                        maxima_distancia = distancia
            
            print(f"{ciudades[i]}: {maxima_distancia}")
            
            if maxima_distancia < minima_excentricidad:
                minima_excentricidad = maxima_distancia
                centro_idx = i
        
        if centro_idx != -1:
            print("----------------------------------------")
            print(f"\nCentro del grafo: {ciudades[centro_idx]}")
            print(f"Excentricidad (distancia máxima a cualquier otra ciudad): {minima_excentricidad}")
            
            print("\nDistancias desde el centro a otras ciudades:")
            print("------------------------------------------")
            for j in range(n):
                if centro_idx != j:
                    distancia = self.floyd.obtener_distancia(centro_idx, j)
                    if distancia < sys.maxsize // 2:
                        print(f"{ciudades[centro_idx]} -> {ciudades[j]}: {distancia} horas")
                    else:
                        print(f"{ciudades[centro_idx]} -> {ciudades[j]}: Sin ruta disponible")
        else:
            print("\nNo se pudo determinar el centro del grafo.")
    
    def modificar_grafo(self):
        rutas = self.grafo.obtener_rutas_originales()
        print("\nRutas disponibles:")
        for idx, ruta in enumerate(rutas):
            print(f"{idx}: {ruta.ciudad1} - {ruta.ciudad2} (Normal: {ruta.tiempo_normal}, Lluvia: {ruta.tiempo_lluvia}, Nieve: {ruta.tiempo_nieve}, Tormenta: {ruta.tiempo_tormenta})")
        
        try:
            opcion = int(input("\nElija una opción:\n1. Modificar ruta existente\n2. Agregar nueva ruta\n3. Bloquear ruta\n4. Volver\n\nOpción: "))
            
            if opcion == 1:
                self.modificar_ruta_existente()
            elif opcion == 2:
                self.agregar_nueva_ruta()
            elif opcion == 3:
                self.bloquear_ruta()
            elif opcion == 4:
                return
            else:
                print("\nOpción no válida.")
            
            # Recalcular Floyd después de modificar
            self.floyd.calcular(self.grafo.obtener_matriz())
        
        except ValueError:
            print("\nEntrada no válida. Debe ingresar un número.")
    
    def modificar_ruta_existente(self):
        rutas = self.grafo.obtener_rutas_originales()
        idx_ruta = int(input("\nIngrese el índice de la ruta a modificar: "))
        
        if idx_ruta < 0 or idx_ruta >= len(rutas):
            print("\nÍndice de ruta no válido.")
            return
        
        ruta = rutas[idx_ruta]
        print(f"\nModificando ruta: {ruta.ciudad1} - {ruta.ciudad2}")
        print("Seleccione condición climática:")
        print(f"1. Normal ({ruta.tiempo_normal})")
        print(f"2. Lluvia ({ruta.tiempo_lluvia})")
        print(f"3. Nieve ({ruta.tiempo_nieve})")
        print(f"4. Tormenta ({ruta.tiempo_tormenta})")
        
        opcion = int(input("Opción: "))
        
        if opcion == 1:
            nuevo_tiempo = ruta.tiempo_normal
        elif opcion == 2:
            nuevo_tiempo = ruta.tiempo_lluvia
        elif opcion == 3:
            nuevo_tiempo = ruta.tiempo_nieve
        elif opcion == 4:
            nuevo_tiempo = ruta.tiempo_tormenta
        else:
            print("\nOpción no válida.")
            return
        
        self.grafo.actualizar_ruta(ruta.ciudad1, ruta.ciudad2, nuevo_tiempo)
        print(f"\nRuta actualizada: {ruta.ciudad1} - {ruta.ciudad2} con nuevo tiempo: {nuevo_tiempo}")