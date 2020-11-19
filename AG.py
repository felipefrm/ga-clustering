from random import randint, sample, random, uniform
from math import sqrt
from Individual import Individual
from Clustering import Clustering

class AG():
    def __init__(self, pop_size, generations, mutation_rate, cross_rate, win_rate, nbits, elitism):
        self.pop_size = pop_size
        self.nbits = nbits
        self.population = None
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.cross_rate = cross_rate
        self.win_rate = win_rate
        self.elitism = elitism

    def initPopulation(self, clusterCount):
        # gera a populacao de individuos em binarios de nbits
        self.population = [[randint(0, clusterCount-1) for x in range(self.nbits)] for y in range(self.pop_size)]
        individual = []
        for ind in self.population:
            individual.append(Individual(ind))
        return individual

    def fitPopulation(self, population, data):
        # Calculo centroide
        for ind in population:
            Clustering.calculateCentroids(data, ind)
            fo = 0
            for idx, val in enumerate(ind.solution):
                data.elements[idx] = [float(i) for i in data.elements[idx]]
                # print(f'esta é a solucao: {data.elements[idx]} / este é o centroide: {ind.centroids[val]}')
                # print(ind.solution)
                dist = [(a - b)**2 for a, b in zip(data.elements[idx], ind.centroids[val])]
                fo += sqrt(sum(dist))
            ind.fitness = fo                
  
    def tourney(self, population):
        # o ultimo individuo não terá adversário, logo é automaticamente escolhido
        if len(population) == 1:
            selected = population[0]
            population.remove(population[0])
            return selected

        sample = sample(range(len(population)), 2)  # sorteia 2 numeros aleatorios distintos
        individual1 = population[sample[0]]
        individual2 = population[sample[1]]

        # 2 individuos duelam, o que possui a maior avaliação na Fo tem maior de chance vencer o duelo
        # o fator de probabilidade de vitória está guardada no atributo "win_rate" da classe self
        r = randint(0, 100)

        if individual1.fitness >= individual2.fitness:
            selected = individual1
            if (r >= self.win_rate):
                selected = individual2
            population.remove(selected)
        
        else:
            selected = individual2
            if (r >= self.win_rate):
                selected = individual1
            population.remove(selected)

        return selected

    def selection(self, current_population, new_population):
        parent1 = self.tourney(current_population)
        if (self.pop_size % 2 != 0 and len(new_population)+1 == self.pop_size):
            parent2 = parent1     # caso o tamanho da populacao seja impar, na ultima iteração do while vai sobrar acontecer só 1 torneio
        else:               # entao, o parent2 será o mesmo que o parent1
            parent2 = self.tourney(current_population)
        return [parent1, parent2]

    def getBestIndividual(self, population):
        # busca o melhor individuo da geração
        fitness = []
        for ind in population:
            fitness.append(ind.fitness)

        val, idx = max((val, idx) for (idx, val) in enumerate(fitness))
        bestIndividual = population[idx]     # salva o melhor individuo, independente se é viavel ou não

        return bestIndividual

    def getWorstIndividual(self, population):
        # busca o pior individuo da geração
        fitness = []
        for ind in population:
            fitness.append(ind.fitness)

        val, idx = min((val, idx) for (idx, val) in enumerate(fitness))

        return population[idx]

    def getMeanIndividuals(self, population):    
        fit_total = sum(ind.fitness for ind in population)
        return fit_total/len(population)


    def crossover(self, parent1, parent2):

        if randint(0, 100) <= self.cross_rate:
            # realiza o cruzamento entre dois individuos
            cut = randint(0, self.nbits)

            children = []

            children1_s = parent1.solution[:cut] + parent2.solution[cut:]
            children1 = Individual(children1_s)
            children.append(children1)

            children2_s = parent2.solution[:cut] + parent1.solution[cut:]
            children2 = Individual(children2_s)
            children.append(children2)
            
            return children

        else:
            return [parent1, parent2]


    def mutation(self, population,clusterCount):
        # muda um elemento aleatorio de cluster 
        for ind in population:
            if randint(0,100) <= self.mutation_rate:
                obj = randint(0, self.nbits-1)
                ind.solution[obj] = randint(0, clusterCount-1)
