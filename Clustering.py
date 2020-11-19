class Clustering():
    def __init__(self, elements, clusters):
        self.elements = elements
        self.clusters = clusters
        self.centroids = None
        self.clusterCount = len(clusters)