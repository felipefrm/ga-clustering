def readDataset(filename):
    elements = []
    clusters = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip().split(',')
            elements.append(line[:-1])
            if line[-1] not in clusters:
                clusters.append(line[-1])
    return (elements, clusters)