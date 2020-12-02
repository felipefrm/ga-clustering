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

    def calculateFitness(self, data, ind):
        fo = 0
        for idx, val in enumerate(ind.solution):
            data.elements[idx] = [float(i) for i in data.elements[idx]]
            dist = [(a - b)**2 for a, b in zip(data.elements[idx], ind.centroids[val])]
            fo += sqrt(sum(dist))
        return fo                

    def fitPopulation(self, population, data):
        # Calculo centroide
        for ind in population:
            Clustering.calculateCentroids(data, ind)
            ind.fitness = self.calculateFitness(data, ind)

    def tourney(self, population):
        # o ultimo individuo não terá adversário, logo é automaticamente escolhido
        if len(population) == 1:
            selected = population[0]
            population.remove(population[0])
            return selected

        random = sample(range(len(population)), 2)  # sorteia 2 numeros aleatorios distintos
        individual1 = population[random[0]]
        individual2 = population[random[1]]

        # 2 individuos duelam, o que possui a maior avaliação na Fo tem maior de chance vencer o duelo
        # o fator de probabilidade de vitória está guardada no atributo "win_rate" da classe self
        r = randint(0, 100)

        if individual1.fitness < individual2.fitness:
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

    def selection(self, current_population):
        parent1 = self.roulette(current_population)
        parent2 = self.roulette(current_population)
        return [parent1, parent2]

    def roulette(self, population):
        fit = sum(abs(1/ind.fitness) for ind in population)
        roulette = []
        for ind in population:
            roulette.append((abs(1/ind.fitness))/fit)
        r = uniform(0, 1)
        control = index = 0
        while (control < r):
            control += roulette[index]
            index += 1
        return population[index-1]


    def getBestIndividual(self, population):
        # busca o melhor individuo da geração
        fitness = []
        for ind in population:
            fitness.append(ind.fitness)

        val, idx = min((val, idx) for (idx, val) in enumerate(fitness))
        bestIndividual = population[idx]     # salva o melhor individuo, independente se é viavel ou não

        return bestIndividual

    def getIndexOfWorstIndividual(self, population):
        # busca o pior individuo da geração
        fitness = []
        for ind in population:
            fitness.append(ind.fitness)

        val, idx = max((val, idx) for (idx, val) in enumerate(fitness))

        return idx

    def getMeanIndividuals(self, population):    
        fit_total = sum(ind.fitness for ind in population)
        return fit_total/len(population)


    def crossover(self, parent1, parent2):

        if randint(0, 100) <= self.cross_rate:
            # realiza o cruzamento entre dois individuos
            cut = []
            cut.append(randint(0, self.nbits))
            cut.append(randint(cut[0], self.nbits))

            children = []
            children1_s = parent1.solution[:cut[0]] + parent2.solution[cut[0]:cut[1]] + parent1.solution[cut[1]:] 
            children1 = Individual(children1_s)
            children.append(children1)

            children2_s = parent2.solution[:cut[0]] + parent1.solution[cut[0]:cut[1]] + parent2.solution[cut[1]:] 
            # print(len(children2_s))
            children2 = Individual(children2_s)
            children.append(children2)
            
            return children

        else:
            return [parent1, parent2]


    def mutation(self, population,clusterCount):
        for ind in population:
            if randint(0,100) <= self.mutation_rate: # cada individuo tem x% de chance de ser selecionado para mutacao
                for j in range(0, self.nbits//self.mutation_rate): # cada bit tem x% de chance de ser mutado
                    obj = randint(0, self.nbits-1)
                    ind.solution[obj] = randint(0, clusterCount-1)
