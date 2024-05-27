# JPBG v1.0
# Este archivo contiene la configuración del algoritmo evolutivo 

import operator
from deap import base
from deap import creator
from deap import tools
from deap import gp
import random

# Función que genera un número flotante aleatorio entre 0 y 1
def generate_random_float():
    return random.uniform(0, 1)   

# Se definen las primitivas a usar para la expresión a generar
# La expresión a generar tendrá dos incognitas, por eso la línea es ("MAIN", 2)
pset = gp.PrimitiveSet("MAIN", 2)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.mul, 2)
pset.addEphemeralConstant("rand", generate_random_float)

# Se renombran las incognitas
pset.renameArguments(ARG0='Dhash',ARG1='fsim')

# Se define que el algoritmo debe maximizar los resultados, se controla con weights=(1.0,)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

toolbox = base.Toolbox()

# La expresión se genera mediante arboles, por lo que se define como se genera el arbol y 
# los limites del arbol (min y max)
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=1)

# Se define la función con la que se creará cada individuo
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)

# Se define la función con la que se creará la población
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# "gp.compile" permite evaluar la expresión con los valores que se le proporcionen 
toolbox.register("compile", gp.compile, pset=pset)

# Forma de selcción de la población
toolbox.register("select", tools.selBest)

# Se define con que función se realizará el cruzamiento
toolbox.register("mate", gp.cxOnePoint)

# Se define con que función se realizará la mutación
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

# Estás lineas límitan la profundidad de los arboles después de realizar 
# mutación o cruzamiento
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=3))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=3))