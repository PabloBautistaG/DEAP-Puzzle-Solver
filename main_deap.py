# JPBG v.1.0
# Archivo main, contiene el algoritmo genetico

import random
from matplotlib import pyplot as plt
import numpy
import pruebas as solver
import piece_functions as functions
from deap_config import toolbox
from deap import algorithms
from deap import tools
from deap import gp
import networkx as nx
from sympy import sympify

# Diccionario usado para simplificar la expresión generada por el algoritmo
locals = {
    'sub': lambda x, y : x - y,
    'div': lambda x, y : x/y,
    'mul': lambda x, y : x*y,
    'add': lambda x, y : x + y,
    'neg': lambda x    : -x,
    'pow': lambda x, y : x**y,
}

pieces = None
puzzles = None
borders = None

def main():
    random.seed(318)

    # Tamaño de la población
    pop = toolbox.population(n=100)

    # Almacena la expresión con el mejor resultado a lo largo del algoritmo genetico
    hof = tools.HallOfFame(1)

    # Se cargan los rompecabezas con sus respectivas piezas y bordes
    # recibe como parametro el tamaño del rompecabezas 
    pieces,puzzles,borders = functions.load(2,2)

    # Se registra la funcón de aptitud
    toolbox.register("evaluate", solver.solve_puzzle,pieces,puzzles,borders)

    # Las siguientes líneas permiten almcenar las estadisticas de cada generación
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    # Función del algoritmo genetico, recibe el tamaño de la población, "toolbox" son todas 
    #  las funciones para generar la población, individuos, mutación, etc.
    # 0.6 = Probabilidad de cruzamiento ; 0.4 = Probabilidad de mutación
    # halloffame = Almacena la mejor expresión
    pop, log = algorithms.eaSimple(pop, toolbox, 0.6, 0.4, 50, stats=mstats,
                                   halloffame=hof, verbose=True)
    
    # Se imprimen las estadisticas del algoritmo
    print(log)

    # Se recupera e imprime la mejor expresión generada por el algoritmo
    best_individual = hof[0]
    print(best_individual)

    # Se simplifica con el diccionario definido
    expr_ = sympify(str(best_individual) , locals=locals)
    print(f'simplified: {expr_}')

    # Se genera el arbol de la mejor expresión
    best_tree = gp.PrimitiveTree(best_individual)
    best_nodes, best_edges, best_labels = gp.graph(best_tree)

    # Se muestra en pantalla el arbol de la expresión
    g = nx.Graph()
    g.add_nodes_from(best_nodes)
    g.add_edges_from(best_edges)
    pos = nx.nx_agraph.graphviz_layout(g, prog="dot")

    nx.draw_networkx_nodes(g, pos)
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos, best_labels)
    plt.show()

if __name__ == "__main__":
    main()