import heapq  # Biblioteca para manejar la cola de prioridad

# Definir los costos de los diferentes tipos de terreno
COSTOS = {
    "camino": 1,  # Camino normal con costo bajo
    "agua": 10,  # Agua con costo alto
    "edificio": float('inf'),  # Edificio, intransitable
}

class Mapa:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.mapa = self.generar_mapa()

    def generar_mapa(self):
        # Creo una matriz de tamaño n x n llena de caminos transitables con el menor costo
        return [[COSTOS["camino"] for _ in range(self.tamaño)] for _ in range(self.tamaño)]

    def añadir_obstaculos(self, tipo_obstaculo, cantidad):
        for _ in range(cantidad):  # Repito para la cantidad de obstáculos introducidos
            x, y = self.obtener_coordenadas(f"Introduce las coordenadas del obstáculo {tipo_obstaculo} (formato: x y): ")
            self.mapa[y][x] = COSTOS[tipo_obstaculo]  # Asigno el costo del obstáculo específico a la celda correspondiente

    def obtener_coordenadas(self, mensaje):
        while True:  # Repito hasta que se ingresen coordenadas válidas
            try: # Utilizo try/except para manejar la posibilidad de errores
                x, y = map(int, input(mensaje).split())  # Leo y divido con split la entrada en x e y
                x -= 1  # Ajusto x para índice basado en 0. No quiero que mi matriz funcione desde 0,0 para el usuario final
                y -= 1  # Lo mismo pero para y
                if 0 <= x < self.tamaño and 0 <= y < self.tamaño:  # Verifico si las coordenadas están dentro del mapa
                    return (x, y)  # Devuelvo las coordenadas ajustadas
                else:
                    print(f"Por favor, introduce coordenadas válidas entre 1 y {self.tamaño}.")
            except ValueError:  # Manejo errores de formato, es decir si ingreso un formato no válido utilizo el manejo de "ValueError"
                print("Entrada inválida. Por favor, introduce dos números separados por un espacio.")

    def imprimir_mapa(self):
        for fila in self.mapa:
            print(" ".join(["." for _ in fila]))  # Imprimo cada celda como un punto ya que es mi mapa vacío

    def imprimir_mapa_con_obstaculos(self):
        for fila in self.mapa:
            print(" ".join(["E" if celda == float('inf') else "A" if celda == 10 else "." for celda in fila]))  # Imprimo "E" para edificios, "A" para agua, "." para caminos una vez que adiciono los obstáculos

    def imprimir_mapa_con_camino(self, camino, inicio, meta): # Imprimo el mapa ya con el camino encontrado
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[y])):
                if (x, y) == inicio:
                    print("I", end=" ")  # Imprimo "I" para el punto de inicio
                elif (x, y) == meta:
                    print("D", end=" ")  # Imprimo "D" para el punto de destino
                elif (x, y) in camino:
                    print("C", end=" ")  # Imprimo "C" para el camino
                elif self.mapa[y][x] == float('inf'):
                    print("E", end=" ")  # Imprimo "E" para edificios
                elif self.mapa[y][x] == 10:
                    print("A", end=" ")  # Imprimo "A" para agua
                else:
                    print(".", end=" ")  # Imprimo "." para caminos
            print()

class AEstrella:
    def __init__(self, mapa):
        self.mapa = mapa

    class Nodo:
        def __init__(self, posicion, g, h):
            self.posicion = posicion  # Posición del nodo en el mapa
            self.g = g  # Costo desde el inicio hasta el nodo
            self.h = h  # Costo heurístico hasta la meta
            self.f = g + h  # Costo total

        def __lt__(self, otro):
            return self.f < otro.f  # Comparo nodos por su costo total

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) # En esta implementación utilizamos la distancia Manhattan como heurística

    def obtener_vecinos(self, posicion):
        vecinos = []
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Posibles direcciones de movimiento (derecha, abajo, izquierda, arriba)
        for direccion in direcciones:
            vecino = (posicion[0] + direccion[0], posicion[1] + direccion[1])  # Obtengo la posición del vecino
            if 0 <= vecino[0] < len(self.mapa.mapa) and 0 <= vecino[1] < len(self.mapa.mapa[0]) and self.mapa.mapa[vecino[1]][vecino[0]] != float('inf'):
                vecinos.append(vecino)  # Añado vecino si está dentro del mapa y si no tiene obstáculos que lo hagan instransitable, en mi caso, edificios
        return vecinos

    def reconstruir_camino(self, de_donde_viene, inicio, meta):
        actual = meta
        camino = []
        while actual != inicio:  # Mientras no llegue al inicio
            camino.append(actual)  # Añado el nodo actual al camino
            if actual not in de_donde_viene:  # Si no hay registro de de dónde viene el nodo
                return None  # No puedo reconstruir el camino
            actual = de_donde_viene[actual]  # Me muevo al nodo anterior y repito el bucle
        camino.append(inicio)  # Añado el nodo inicial ya que éste no tiene nodo padre, para tener el camino completo
        camino.reverse()  # Invierto el camino para que vaya del inicio a la meta
        return camino

    def resolver(self, inicio, meta):
        lista_abierta = []  # Inicializo la lista abierta (sería mi open set, una cola de prioridad)
        heapq.heappush(lista_abierta, self.Nodo(inicio, 0, self.heuristica(inicio, meta)))  # Añado el nodo inicial
        de_donde_viene = {}  # Diccionario para rastrear de dónde viene cada nodo, es decir, la relación nodos padre-hijo
        costo_hasta_ahora = {inicio: 0}  # Diccionario para almacenar el costo hasta cada nodo en el que nos encontremos

        while lista_abierta:  # Mientras haya nodos por explorar
            actual = heapq.heappop(lista_abierta).posicion  # Obtengo el nodo con el menor costo total (f)

            if actual == meta:  # Si llego a la meta
                return self.reconstruir_camino(de_donde_viene, inicio, meta)  # Reconstruyo y devuelvo el camino llamando a este método

            for vecino in self.obtener_vecinos(actual):  # Obtengo los vecinos del nodo actual con este método, iterando por cada uno
                nuevo_costo = costo_hasta_ahora[actual] + self.mapa.mapa[vecino[1]][vecino[0]]  # Calculo el nuevo costo
                if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:  # Si el nuevo costo es menor
                    costo_hasta_ahora[vecino] = nuevo_costo  # Actualizo el costo hasta el vecino
                    heapq.heappush(lista_abierta, self.Nodo(vecino, nuevo_costo, self.heuristica(vecino, meta)))  # Añado el vecino a la lista abierta
                    de_donde_viene[vecino] = actual  # Registro de dónde viene el vecino

        return None  # Si no encuentro un camino, devuelvo None

# Generar el mapa
tamaño = int(input("Introduce el tamaño del mapa: "))  # Pido el tamaño del mapa al usuario
mapa = Mapa(tamaño)  # Creo el mapa

# Imprimir el mapa vacío
print("Mapa vacío:")
mapa.imprimir_mapa()

# Añadir obstáculos
cantidad_edificios = int(input("Introduce la cantidad de edificios: "))  # Pido la cantidad de edificios
mapa.añadir_obstaculos("edificio", cantidad_edificios)  # Añado edificios al mapa

cantidad_agua = int(input("Introduce la cantidad de áreas de agua: "))  # Pido la cantidad de áreas de agua
mapa.añadir_obstaculos("agua", cantidad_agua)  # Añado áreas de agua al mapa

# Imprimir el mapa con obstáculos
print("Mapa con obstáculos:")
mapa.imprimir_mapa_con_obstaculos()

# Obtener las coordenadas de inicio y meta
inicio = mapa.obtener_coordenadas("Introduce las coordenadas de inicio (formato: x y): ")
meta = mapa.obtener_coordenadas("Introduce las coordenadas de destino (formato: x y): ")

# Resolver el problema con el algoritmo A*
a_estrella = AEstrella(mapa)  # Creo la instancia de AEstrella
camino = a_estrella.resolver(inicio, meta)  # Resuelvo el problema

# Imprimir el mapa con el camino encontrado
if camino:
    print("Mapa con el camino encontrado:")
    mapa.imprimir_mapa_con_camino(camino, inicio, meta)
else:
    print("No se encontró un camino desde el inicio hasta la meta.")
