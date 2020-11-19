from AG import *
from Clustering import *
from utils import *

(elements, clusters) = readDataset('dataset/iris.data')
clustering = Clustering(elements, clusters)
ag  = AG(100, 100, 10, 100, 90, len(elements), True)
new_population = ag.initPopulation(clustering.clusterCount)
for generation in range(ag.generations):
    ag.fitPopulation(new_population, clustering)
    bestIndividual = ag.getBestIndividual(new_population)

    print(f"Best individual of generation {generation}\t  →\tFitness: {bestIndividual.fitness}\tSolution: {bestIndividual.solution}]")

    current_population = new_population
    new_population = []

    while len(new_population) < ag.pop_size:
        parent = ag.selection(current_population, new_population)
        children = ag.crossover(parent[0], parent[1])
        new_population.extend(children)  
    
    ag.mutation(new_population)
    
    if (ag.elitism):
        random = randint(0, len(new_population)-1)  # sorteia um individuo
        new_population[random] = bestIndividual    # substitui individuo sorteado pelo melhor individuo
