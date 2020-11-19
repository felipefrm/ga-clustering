from AG import *
from Clustering import *
from utils import *
from constants import *
import time

start = time.time()

(elements, clusters, attributesCount) = readDataset('dataset/iris.data')
clustering = Clustering(elements, clusters, attributesCount)

ag  = AG(POP_SIZE, GENERATIONS, MUTATION_RATE, CROSSOVER_RATE, WIN_RATE, len(elements), ELITISM)
new_population = ag.initPopulation(clustering.clusterCount)
for generation in range(ag.generations):
    ag.fitPopulation(new_population, clustering)
    bestIndividual = ag.getBestIndividual(new_population)

    print(f"Best individual of generation {generation}\t  →\tFitness: {bestIndividual.fitness}\tSolution: {bestIndividual.solution}]")

    current_population = new_population
    new_population = []

    while len(new_population) < ag.pop_size:
        parent = ag.selection(current_population)
        children = ag.crossover(parent[0], parent[1])
        new_population.extend(children)  
    
    ag.mutation(new_population, clustering.clusterCount)
    
    if (ag.elitism):
        out = randint(0, len(new_population)-1)              # pega um individuo aleatorio
        # out = ag.getIndexOfWorstIndividual(new_population)   # pega o pior inidivduo
        new_population[out] = bestIndividual             # substitui individuo pelo melhor individuo da ultima geracao

end = time.time()
print(f'\nTime elapsed: {end - start} seconds')
