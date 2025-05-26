import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch
from HDT10 import Ruta, Grafo, AlgoritmoFloyd, AnalizadorArchivo, main

class TestRuta(unittest.TestCase):
    def test_creacion_ruta(self):
        ruta = Ruta("BuenosAiresToSaoPaulo", "BuenosAires", "SaoPaulo", 10, 15, 20, 50)
        self.assertEqual(ruta.nombre, "BuenosAiresToSaoPaulo")
        self.assertEqual(ruta.ciudad1, "BuenosAires")
        self.assertEqual(ruta.ciudad2, "SaoPaulo")
        self.assertEqual(ruta.tiempo_normal, 10)
        self.assertEqual(ruta.tiempo_lluvia, 15)
        self.assertEqual(ruta.tiempo_nieve, 20)
        self.assertEqual(ruta.tiempo_tormenta, 50)

class TestGrafo(unittest.TestCase):
    def setUp(self):
        rutas = [
            Ruta("BuenosAiresToSaoPaulo", "BuenosAires", "SaoPaulo", 10, 15, 20, 50),
            Ruta("BuenosAiresToLima", "BuenosAires", "Lima", 15, 20, 30, 70)
        ]
        self.grafo = Grafo(rutas)
    
    def test_ciudades(self):
        ciudades = self.grafo.obtener_ciudades()
        self.assertEqual(len(ciudades), 3)
        self.assertIn("BuenosAires", ciudades)
        self.assertIn("SaoPaulo", ciudades)
        self.assertIn("Lima", ciudades)
    
    def test_matriz_adyacencia(self):
        matriz = self.grafo.obtener_matriz()
        self.assertEqual(len(matriz), 3)
        self.assertEqual(matriz[0][0], 0)  
        self.assertEqual(matriz[0][1], 10)  
        self.assertEqual(matriz[1][0], 10)  
        self.assertEqual(matriz[0][2], 15)  
        self.assertEqual(matriz[2][0], 15)  
        self.assertEqual(matriz[1][2], sys.maxsize // 2)  
    
    def test_actualizar_ruta(self):
        self.grafo.actualizar_ruta("BuenosAires", "SaoPaulo", 20)
        matriz = self.grafo.obtener_matriz()
        self.assertEqual(matriz[0][1], 20)
        self.assertEqual(matriz[1][0], 20)
    
    def test_obtener_peso(self):
        peso = self.grafo.obtener_peso("BuenosAires", "SaoPaulo")
        self.assertEqual(peso, 10)
        peso = self.grafo.obtener_peso("SaoPaulo", "Lima")
        self.assertEqual(peso, sys.maxsize // 2)

class TestAlgoritmoFloyd(unittest.TestCase):
    def setUp(self):
        rutas = [
            Ruta("BuenosAiresToSaoPaulo", "BuenosAires", "SaoPaulo", 10, 15, 20, 50),
            Ruta("BuenosAiresToLima", "BuenosAires", "Lima", 15, 20, 30, 70),
            Ruta("LimaToQuito", "Lima", "Quito", 10, 12, 15, 20)
        ]
        grafo = Grafo(rutas)
        self.floyd = AlgoritmoFloyd()
        self.floyd.calcular(grafo.obtener_matriz())
        self.ciudades = grafo.obtener_ciudades()
    
    def test_distancias(self):
        idx_ba = self.ciudades.index("BuenosAires")
        idx_sp = self.ciudades.index("SaoPaulo")
        idx_li = self.ciudades.index("Lima")
        idx_qu = self.ciudades.index("Quito")
        
        self.assertEqual(self.floyd.obtener_distancia(idx_ba, idx_sp), 10)
        self.assertEqual(self.floyd.obtener_distancia(idx_ba, idx_li), 15)
        self.assertEqual(self.floyd.obtener_distancia(idx_li, idx_qu), 10)
        self.assertEqual(self.floyd.obtener_distancia(idx_ba, idx_qu), 25)  
    
    def test_rutas(self):
        idx_ba = self.ciudades.index("BuenosAires")
        idx_sp = self.ciudades.index("SaoPaulo")
        idx_li = self.ciudades.index("Lima")
        idx_qu = self.ciudades.index("Quito")
        
        ruta_ba_qu = self.floyd.obtener_ruta_indices(idx_ba, idx_qu)
        self.assertEqual(len(ruta_ba_qu), 3)
        self.assertEqual(ruta_ba_qu[0], idx_ba)
        self.assertEqual(ruta_ba_qu[1], idx_li)
        self.assertEqual(ruta_ba_qu[2], idx_qu)
        
        ruta_sp_qu = self.floyd.obtener_ruta_indices(idx_sp, idx_qu)
        self.assertEqual(len(ruta_sp_qu), 3)
        self.assertEqual(ruta_sp_qu[0], idx_sp)
        self.assertEqual(ruta_sp_qu[1], idx_ba)
        self.assertEqual(ruta_sp_qu[2], idx_li)


class TestAnalizadorArchivo(unittest.TestCase):
    def setUp(self):
        self.archivo_test = "test_logistica.txt"
        with open(self.archivo_test, 'w') as f:
            f.write("BuenosAires SaoPaulo 10 15 20 50\n")
            f.write("BuenosAires Lima 15 20 30 70\n")
    
    def tearDown(self):
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)
    
    def test_analizar_archivo(self):
        rutas = AnalizadorArchivo.analizar(self.archivo_test)
        self.assertEqual(len(rutas), 2)
        self.assertEqual(rutas[0].ciudad1, "BuenosAires")
        self.assertEqual(rutas[0].ciudad2, "SaoPaulo")
        self.assertEqual(rutas[0].tiempo_normal, 10)
        self.assertEqual(rutas[1].ciudad1, "BuenosAires")
        self.assertEqual(rutas[1].ciudad2, "Lima")
        self.assertEqual(rutas[1].tiempo_normal, 15)
    
    def test_archivo_no_existe(self):
        with self.assertRaises(FileNotFoundError):
            AnalizadorArchivo.analizar("archivo_inexistente.txt")
    

class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = main()
        self.app.archivo_datos = "test_logistica.txt"
        with open(self.app.archivo_datos, 'w') as f:
            f.write("BuenosAires SaoPaulo 10 15 20 50\n")
            f.write("BuenosAires Lima 15 20 30 70\n")
            f.write("Lima Quito 10 12 15 20\n")
    
    def tearDown(self):
        if os.path.exists(self.app.archivo_datos):
            os.remove(self.app.archivo_datos)
    
    @patch('builtins.input', side_effect=['1', '0', '1', '4'])
    def test_ruta_mas_corta(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.ejecutar()
            output = fake_out.getvalue()
            self.assertIn("Ruta más corta: BuenosAires -> SaoPaulo", output)
            self.assertIn("Distancia total: 10 horas", output)
    
    @patch('builtins.input', side_effect=['2', '4'])
    def test_centro_grafo(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.ejecutar()
            output = fake_out.getvalue()
            self.assertIn("Centro del grafo:", output)
            self.assertIn("Excentricidad", output)
    
    @patch('builtins.input', side_effect=['3', '1', '0', '1', '4'])
    def test_modificar_ruta_existente(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.ejecutar()
            output = fake_out.getvalue()
            self.assertIn("Ruta actualizada:", output)
    
    @patch('builtins.input', side_effect=['3', '2', 'Quito', 'SaoPaulo', '20', '25', '30', '60', '4'])
    def test_agregar_nueva_ruta(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.ejecutar()
            output = fake_out.getvalue()
            self.assertIn("Nueva ruta agregada: Quito - SaoPaulo", output)
    
    @patch('builtins.input', side_effect=['3', '3', '0', '4'])
    def test_bloquear_ruta(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.ejecutar()
            output = fake_out.getvalue()
            self.assertIn("Ruta bloqueada: BuenosAires - SaoPaulo", output)
    
    @patch('builtins.input', side_effect=['5', '4'])  # Opción inválida
    def test_opcion_invalida(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.ejecutar()
            output = fake_out.getvalue()
            self.assertIn("Opción no válida", output)

if __name__ == "__main__":
    unittest.main()