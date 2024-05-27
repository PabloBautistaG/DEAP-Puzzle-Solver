# JPBG v1.0
# Este archivo contiene las funciones necesarias para obtener las piezas del rompecabezas, 
# sus bordes. Así como las funciones que permiten su visualización

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import piece_functions as functions

# Se obtienen las pizas del rompecabezas, recibe como parametros la imagen con las piezas
# y el tamaño del rompecabezas
def obtain_pieces(image, rows, columns):

    # Se calculan las dimensiones del rompecabezas
    height, width = image.size
    pieces = []

    # Se calculan las dimensiones de cada piezas
    width_piece = width//columns
    height_piece = height//rows
    for fila in range(rows):
        for columna in range(columns):
            # Calcular las coordenadas de la pieza actual
            x1 = columna * width_piece
            y1 = fila * height_piece
            x2 = x1 + width_piece
            y2 = y1 + height_piece

            # Recortar la imagen para obtener la pieza actual
            piece = image.crop((x1, y1, x2, y2))

            # Agregar la pieza a la lista
            pieces.append(piece)

    # Devolver la lista de piezas
    return pieces

# Función que permite imprimir las piezas, recibe las piezas y el tamaño del rompecabezas
def print_pieces(pieces, rows, columns):
    
    # Creacion de la figura para mostrar las piezas
    fig, axs = plt.subplots(1, 4, figsize=(10, 10))

    for i in range(rows*columns):
        axs[i].imshow(pieces[i])
        axs[i].set_title('Piece '+ str(i))
    
    plt.show()
    return

# Función que permite obtener los bordes de cada pieza
def obtain_borders(pieces,rows,columns):
    borders = []

    for piezas in range(rows*columns):

        # Se define el tamaño del borde, en este caso solo toma dos pixeles de ancho para 
        # las piezas izquierdo y derecho por el tamaño de alto de la piezas. Para las piezas
        # inferior y superior toma dos pixeles de alto por el tamaño del ancho de la pieza
        piece = np.asarray(pieces[piezas])
        borde_superior = piece[0:2,:,:]
        borde_inferior = piece[-2:, :, :]
        borde_izquierdo = piece[:, 0:2, :]
        borde_derecho = piece[:, -2:, :] 

        # Se convierten los bordes a instancias de PIL (Pillow)
        bord = [Image.fromarray(borde_superior),
                Image.fromarray(borde_inferior),
                Image.fromarray(borde_izquierdo),
                Image.fromarray(borde_derecho)]
        
        # Se almacenan los bordes en una lista
        borders.append(bord)
    
    # Se retorna la lista
    return borders

# Función que permite imprimir las piezas y sus respectivos bordes
def print_all_borders(pieces, borders, rows, columns):

    for i in range(rows*columns):

        fig = plt.figure() 
        axs = fig.subplots(1, 5)

        piece = np.asarray(pieces[i])
        borde_superior = borders[i][0]
        borde_inferior = borders[i][1]
        borde_izquierdo = borders[i][2]
        borde_derecho = borders[i][3]
        
        axs[0].imshow(piece)
        axs[0].set_title('Imagen original')

        axs[1].imshow(borde_superior)
        axs[1].set_title('Borde superior')

        axs[2].imshow(borde_inferior)
        axs[2].set_title('Borde inferior')

        axs[3].imshow(borde_izquierdo)
        axs[3].set_title('Borde izquierdo')

        axs[4].imshow(borde_derecho)
        axs[4].set_title('Borde derecho')
        
        plt.show()

    return


def print_borders(pieces, borders, rows, columns):

    for i in range(rows*columns):

        fig = plt.figure() 
        axs = fig.subplots(1, 5)

        piece = np.asarray(pieces[i])
        borde_superior = borders[i][0]
        borde_inferior = borders[i][1]
        borde_izquierdo = borders[i][2]
        borde_derecho = borders[i][3]
        
        axs[0].imshow(piece)
        axs[0].set_title('Piece ' + str(i))

        axs[1].imshow(borde_superior)
        axs[1].set_title('top border')

        axs[2].imshow(borde_inferior)
        axs[2].set_title('Bottom border')

        axs[3].imshow(borde_izquierdo)
        axs[3].set_title('Left border')

        axs[4].imshow(borde_derecho)
        axs[4].set_title('Right border')
        
        plt.show()

    return

# Función que muestra en pantalla las piezas en cuadrantes, según el orden proporcionado
def print_ord_pieces(order, pieces):
    
    # Creacion de la figura para mostrar las piezas
    fig, axs = plt.subplots(1, 4, figsize=(10, 10))

    axs[0].imshow(pieces[order[0]])
    axs[0].set_title('I ')
    axs[1].imshow(pieces[order[1]])
    axs[1].set_title('II')
    axs[2].imshow(pieces[order[2]])
    axs[2].set_title('III')
    axs[3].imshow(pieces[order[3]])
    axs[3].set_title('IV')
    
    plt.show()
    return

# Función que a partir de las piezas y un orden definido crea una imagen 
# Su uso es para generar el rompecabezas una vez obtenido el orden correcto
def create_image(corr_order,pieces):

    # Se acomodan las piezas según el orden propuesto
    corr_pieces = [pieces[corr_order[0]],pieces[corr_order[1]],pieces[corr_order[2]],pieces[corr_order[3]]]

    # Se crea un subconjunto de piezas para la parte inferior y superior
    sup_pieces = corr_pieces[:2]
    inf_pieces = corr_pieces[2:]

    # Se combinan las piezas de cada subconjunto
    superior = np.concatenate(sup_pieces, axis=1)
    inferior = np.concatenate(inf_pieces, axis=1)

    # Se crea la imagen completa
    image_completa = np.concatenate([superior, inferior], axis=0)

    return Image.fromarray(image_completa)

# Función que se encarga de obtener los rompecabezas, y apartir de ellos obtener las piezas
# y sus bordes
def load(ROWS,COLUMNS):
    pieces = []
    puzzles = []
    borders = []
    for i in range(0,10):
        # Imagen con las piezas en desorden
        my_image = Image.open("Kaggle_Dataset_JigsawPuzzle/Gravity Falls/puzzle_2x2/train/" + str(i) + ".jpg")
        # Imagen del rompecabezas correcto, su uso es para determinar si la solución generada
        # por el algoritmo es correcta
        image_complete = Image.open("Kaggle_Dataset_JigsawPuzzle/Gravity Falls/correct/" + str(i) + ".png")
        puzzles.append(image_complete)

        # Se obtienen las piezas
        obtained_pieces = functions.obtain_pieces(my_image,COLUMNS,ROWS)
        pieces.append(obtained_pieces)

        # Se obtienen los bordes a partir de las piezas
        obtained_borders = functions.obtain_borders(pieces[i],COLUMNS,ROWS)
        borders.append(obtained_borders)

    return pieces,puzzles,borders