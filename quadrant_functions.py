# JPBG v1.0
# Este archivo contiene las funciones relacionadas con el calculo de cada cuadrante

import imagehash
import sys
import piece_functions as functions
import matplotlib.pyplot as plt
from torchvision import transforms
import piq
from deap_config import toolbox

expression = None
transformacion = transforms.ToTensor()

# Función que evalua la similitud entre dos imagenes con los metodos dhash y fsim, para después 
# evaluar esos resultados según la expresión generada por el algoritmo
def simility(image1,image2):
    # Calculo del hash de cada imagen, con un tamaño del hash de 16 bits
    b1_hash = imagehash.average_hash(image1,hash_size=16)
    b2_hash = imagehash.average_hash(image2,hash_size=16)

    # Se obtiene la diferencia entre los hashes, donde un valor más cercano a 0 indica que 
    # las imagenes comparadas son más similares, generalemnte un valor menor a 10 indica que ambas
    # imagenes son similares
    hamming_distance = b1_hash - b2_hash

    # Se normaliza el valor del hash, el rango de la metrica ahora es de 0 a 4, en la mayoría de los 
    # casos
    hash_size = int(len(b1_hash)*4 / (16))
    normalized_distance = hamming_distance / hash_size

    # Se convierte cada imagen a un tensor
    tensor = transformacion(image1).unsqueeze(0)
    tensor2 = transformacion(image2).unsqueeze(0)

    # Se obtiene la metrica FSIM, la metrica retorna un valor flotante de 0 a 1, donde un valor más 
    # cercano a 1 indica que las imagenes son similres
    fsim_r = piq.fsim(tensor,tensor2).item()

    # Para que ambas metricas sigan un mismo rango se multiplica la metrica por 4. 
    # Se resta 4 menos el valor de FSIM para que ambas metricas tomen el valor más cercano a 0
    # para indicar una mayor similitud de las imagenes
    fsim_r = fsim_r * 4
    fsim_r = 4 - fsim_r

    """print(normalized_distance)
    print(fsim_r)
    print(expression)"""

    # Se compila la expresión, es decir, se genera el arbol
    func = toolbox.compile(expression)
    # Se evalua con los valores de Dhash y FSIM
    result = func(normalized_distance,fsim_r)
    #print(result)

    # Se retorna el valor obtenido tras evaluar la expresión
    return result   

"""def plots(borde1, borde2):
    fig = plt.figure() 
    axs = fig.subplots(1, 2)

    axs[0].imshow(borde1)
    axs[0].set_title('Inferior')

    axs[1].imshow(borde2)
    axs[1].set_title('Superior')

    plt.show()

    return 0"""

# Funcion que obtiene la pieza más similar a través de la comparación de su borde inferior, con
# el borde superior de las posibles piezas
def encuentra_inf(no_pieza,borders,posibilidades):
    umbral = sys.maxsize
    best = sys.maxsize
    for i in posibilidades:
        if i != no_pieza:
            res = simility(borders[no_pieza][1],borders[i][0])
            if(res < umbral):
                umbral = res
                best = i

    res = umbral
    return best,res

# Funcion que obtiene la pieza más similar a través de la comparación de su borde izquierdo, con
# el borde derecho de las posibles piezas
def encuentra_izq(no_pieza,borders,posibilidades):
    umbral = sys.maxsize
    best = sys.maxsize
    for i in posibilidades:
        if i != no_pieza:
            res = simility(borders[no_pieza][2],borders[i][3])
            if(res < umbral):
                umbral = res
                best = i

    res = umbral
    return best,res

# Funcion que obtiene la pieza más similar a través de la comparación de su borde derecho, con
# el borde izquierdo de las posibles piezas
def encuentra_der(no_pieza,borders,posibilidades):
    umbral = sys.maxsize
    best = sys.maxsize
    for i in posibilidades:
        if i != no_pieza:
            res = simility(borders[no_pieza][3],borders[i][2])

            if(res < umbral):
                umbral = res
                best = i

    res = umbral
    return best,res

# Funcion que obtiene la pieza más similar a través de la comparación de su borde superior, con
# el borde inferior de las posibles piezas
def encuentra_sup(no_pieza,borders,posibilidades):
    # El umbral controla que se escoja la mejor opcion
    umbral = sys.maxsize

    # Best almacena la posicion de la pieza con la mejor similitud 
    best = sys.maxsize

    # Se toman las posiciones de las posibles piezas
    for i in posibilidades:
        # Se asegura que no se compare la pieza consigo misma
        if i != no_pieza:
            # Funcion que compara los bordes, "res" almacena el valor calculado por la metrica
            res = simility(borders[no_pieza][0],borders[i][1])
            # Un menor valor de "res" indica que la pieza comparada tiene mayor similitud
            if(res < umbral):
                # Se actualiza el valor del umbral para que en las siguientes comparaciones
                # solo cambie la pieza actual si encuentra una con mejor similitud
                umbral = res
                best = i
    
    res = umbral
    return best,res

# Funcion utilizada para encontrar la mejor combinacion de piezas, 
# asumiendo que la pieza escogida pertenece al cuadrante IV
def Cuadrante_IV(pieza,borders):
    elegible_pieces = [0,1,2,3]
    piezas_correctas = [0,1,2,3]

    aux = 0
    prob = 0

    elegible_pieces.remove(pieza)
    piezas_correctas[3] = pieza
    best,aux = encuentra_sup(pieza,borders,elegible_pieces)
    prob += aux

    elegible_pieces.remove(best)
    piezas_correctas[1] = best 
    prob += aux
    aux = 0
    
    best,aux = encuentra_izq(pieza,borders,elegible_pieces)
    prob += aux

    elegible_pieces.remove(best)
    piezas_correctas[2] = best

    best,aux = encuentra_izq(piezas_correctas[1],borders,elegible_pieces)
    prob += aux

    piezas_correctas[0] = elegible_pieces[0]

    return piezas_correctas,prob

# Funcion utilizada para encontrar la mejor combinacion de piezas, 
# asumiendo que la pieza escogida pertenece al cuadrante III
def Cuadrante_III(pieza,borders):
    elegible_pieces = [0,1,2,3]
    piezas_correctas = [-1,-1,-1,-1]

    aux = 0
    prob = 0

    elegible_pieces.remove(pieza)
    piezas_correctas[2] = pieza
    best,aux = encuentra_sup(pieza,borders,elegible_pieces)

    elegible_pieces.remove(best)
    piezas_correctas[0] = best
    prob += aux
    aux = 0

    best,aux = encuentra_der(pieza,borders,elegible_pieces)
    prob += aux

    elegible_pieces.remove(best)
    piezas_correctas[3] = best

    best,aux = encuentra_sup(piezas_correctas[3],borders,elegible_pieces)
    prob += aux

    piezas_correctas[1] = elegible_pieces[0]

    return piezas_correctas,prob

# Funcion utilizada para encontrar la mejor combinacion de piezas, 
# asumiendo que la pieza escogida pertenece al cuadrante II
def Cuadrante_II(pieza,borders):
    # Arreglos usados para almacenar las posibles piezas y las piezas en su orden correcto
    elegible_pieces = [0,1,2,3]
    piezas_correctas = [0,1,2,3]

    # Variables para almacenar la probabilidad de que la pieza sea correcta
    aux = 0
    prob = 0

    # Se remueve la pieza elegida de la lista de piezas posibles
    elegible_pieces.remove(pieza)

    # Se añade a la lista de piezas correctas, 
    # se asume que la pieza elegida esta en la posición 1, que corresponde al cuadrante II
    piezas_correctas[1] = pieza

    # Se busca la pieza que corresponda con el borde inferior entre las posibles piezas
    best,aux = encuentra_inf(pieza,borders,elegible_pieces)

    # Se remueve la pieza obtenida para que no vuelva a ser comparada y se asigna en la posicion 3,
    # que corresponde al cuadrante IV
    elegible_pieces.remove(best)
    piezas_correctas[3] = best 

    # Se suma la metrica de la pieza anterior
    prob += aux
    aux = 0
    
    # Se busca la pieza que corresponda con el borde izquiedo entre las posibles piezas
    best,aux = encuentra_izq(pieza,borders,elegible_pieces)

    # Se suma la metrica de la pieza anterior
    prob += aux
    
    # Se remueve la pieza obtenida para que no vuelva a ser comparada y se asigna en la pisición 0
    # que corresponde al cuadrante I
    elegible_pieces.remove(best)    
    piezas_correctas[0] = best

    # Se asume que la pieza restante pertenece al cuadrante III, sin embargo, se compara la pieza
    # en el cuadrante IV con la pieza restante para obtener su metrica y poder obtener una mejor
    # presición al comparar los posibles resultados entre los bordes
    best,aux = encuentra_izq(piezas_correctas[3],borders,elegible_pieces)
    prob += aux

    # Se asigna la pieza restante al cuadrante III
    piezas_correctas[2] = elegible_pieces[0]
    
    
    # Se retorna una lista con el mejor orden encontrado y la probabilidad absoluta de todas las piezas
    return piezas_correctas,prob

# Funcion utilizada para encontrar la mejor combinacion de piezas, 
# asumiendo que la pieza escogida pertenece al cuadrante I
def Cuadrante_I(pieza,borders):
    elegible_pieces = [0,1,2,3]
    piezas_correctas = [0,1,2,3]

    aux = 0
    prob = 0

    elegible_pieces.remove(pieza)
    piezas_correctas[0] = pieza
    best,aux = encuentra_inf(pieza,borders,elegible_pieces)

    elegible_pieces.remove(best)
    piezas_correctas[2] = best
    prob += aux
    aux = 0

    best,aux = encuentra_der(pieza,borders,elegible_pieces)
    prob += aux

    elegible_pieces.remove(best)
    piezas_correctas[1] = best

    best,aux = encuentra_inf(piezas_correctas[1],borders,elegible_pieces)
    prob += aux

    piezas_correctas[3] = elegible_pieces[0]

    return piezas_correctas,prob

# Función que evalua cada rompecabezas en base a sus piezas y sus respectivos bordes
def eval_puzzle(individual,pieces,borders):
    expr = individual
    global expression
    expression = expr

    pieza = 2
    corr = []
    aux_ = []
    prob = sys.maxsize
    aux = sys.maxsize

    # Evaluacion en el cuadrante I
    aux_,aux = Cuadrante_I(pieza,borders)
    if(aux < prob):
        corr = aux_
        prob = aux
        aux = 0

    # Evaluacion en el cuadrante II    
    aux_,aux = Cuadrante_II(pieza,borders)
    if(aux < prob):
        corr = aux_
        prob = aux
        aux = 0

    # Evaluacion en el cuadrante III
    aux_,aux = Cuadrante_III(pieza,borders)
    if(aux < prob):
        corr = aux_
        prob = aux
        aux = 0
    
    # Evaluacion en el cuadrante IV
    aux_,aux = Cuadrante_IV(pieza,borders)
    if(aux < prob):
        corr = aux_
        prob = aux
        aux = 0

        if(corr == []):
            corr = aux_

    # Al evaluar los cuatro cuadrantes se obtiene el orden propuesto de las piezas, en base a 
    # ello se crea una imagen con las piezas en el orden correcto
    solved_puzzle = functions.create_image(corr,pieces)

    # Se retorna la posible solución del rompecabezas
    return solved_puzzle

# Función que determina que tan similares son dos imagenes usando dhash, su uso principal es 
# determinar si la posible solución del rompecabezas es verdadera en base a la comparación 
# de la propuesta con la respuesta correcta
def simility_check(image1,image2):
    try:
        b1_hash = imagehash.average_hash(image1,hash_size=16)
        b2_hash = imagehash.average_hash(image2,hash_size=16)

        hamming_distance = (b1_hash - b2_hash)

        #print("Hamming distance = " + str(hamming_distance))   
    except Exception as e:
        print(f"Error: {e}")
        hamming_distance = 0
    return hamming_distance