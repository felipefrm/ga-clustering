class Clustering():
    def __init__(self, elements, clusters, attributesCount):
        self.elements = elements
        self.clusters = clusters
        self.attributesCount = attributesCount
        self.clusterCount = len(clusters)

    def calculateCentroids(self, ind):
            parameters = [[] for i in range(self.clusterCount)]
            for idx, val in enumerate(ind.solution):
                parameters[val].append(self.elements[idx])
            for cluster in range(self.clusterCount):
                sumAttribute = [0 for i in range(self.attributesCount)]
                for element in range(len(parameters[cluster])):
                    for i in range(self.attributesCount):
                        sumAttribute[i] += float(parameters[cluster][element][i])
                meanAttribute = []
                for i in range(self.attributesCount):
                    if (len(parameters[cluster]) == 0):
                        meanAttribute.append(0)
                    else:
                        meanAttribute.append(sumAttribute[i]/len(parameters[cluster]))
                ind.centroids.append(meanAttribute)
