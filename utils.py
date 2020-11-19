def readDataset(filename):
    elements = []
    clusters = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip().split(',')
            attributes = line[:-1]
            elements.append(attributes)
            if line[-1] not in clusters:
                clusters.append(line[-1])
        
    return (elements, clusters, len(attributes))