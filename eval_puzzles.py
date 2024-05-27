# JPBG v1.0
# Este código evalua los rompecabezas con una expresión a evaluar

import piece_functions as functions
import quadrant_functions as cuadrantes
import matplotlib.pyplot as plt 

# Filas y columnas del rompecabezas a resolver
COLUMNS = 2
ROWS = 2

# Función que resuelve los rompecabezas
# Recibe como parametros las piezas de los rompecabezas y sus bordes, 
# los rompecabezas correctos y la expresión a evaluar (individual)
def solve_puzzle(pieces,puzzles,borders,individual):

    #expr = individual

    # Variable que almacena la cantidad de rompecabezas resueltos 
    solved = 0

    # Se recorren los rompecabezas; cantidad maxima = 110
    for i in range(0,10):

        # Función que evalua un solo rompecabezas, recibe las piezas del rompecabezas
        # y sus bordes, retorna una imagen con el rompecabezas resuelto
        solved_puzzle = cuadrantes.eval_puzzle(individual,pieces[i],borders[i])

        # Se evalua el rompecabezas generado por la funcion "eval_puzzle" y el rompecabezas
        # correcto 
        if (cuadrantes.simility_check(solved_puzzle,puzzles[i]) < 10):
            solved += 1

        # Se muestra el rompecabezas generado     
        plt.imshow(solved_puzzle)
        plt.show()

    # Expresión con la que se resuelven los rompecabezas
    #print(expr)
            
    # Se retorna la cantidad de rompecabezas resuletos correctamente
    return solved,

# Este fragmento de codigo se usa para evaluar la expresión generada por el algoritmo de
# programacion genetica
if __name__ == "__main__":
    pieces = []
    puzzles = []
    borders = []
    # Se cargan los rompecabezas con sus respectivas piezas y bordes
    # recibe como parametro el tamaño del rompecabezas
    pieces,puzzles,borders = functions.load(ROWS,COLUMNS)

    # Se resuelven los rompecabezas con la expersión que se usará para evaluar
    solve_puzzle(pieces,puzzles,borders,"Dhash*fsim")
