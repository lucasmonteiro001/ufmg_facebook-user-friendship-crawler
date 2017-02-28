import crawler as cr
import func0 as func
import networkx as nx

GRAPH_PATH = "graph_structure_02.gexf"

#g = cr.main_getGraph()
#func.saveGraphGEXF(g, GRAPH_PATH)

g = nx.read_gexf(GRAPH_PATH)
#cr.printGraphInfo(g)

#printInFile = True
printInFile = False
#printInFile = "1"

if printInFile == False:

    (avg, dist) =  func.avgDistanceAndDistribution(g)
    print "\n\nDistancia media " + str(avg) + "\n"
    func.printScalarDist("Distribuicao\nDistancia, Numero de aresta (nos)", dist)

    func.printIntervalDist("Distribuicao\nGrau, Quantidade de nos por grau", func.degreeDistribution(g))

    func.printScalarDist("Distribuicao\nTamanho Component, Quantidade de nos por componente", func.componentsDistribution(g))

    func.printIntervalDist("Distribuicao\nNeighborhood Overlap, Quantidade de arestas", func.neighborhoodOverlapDistribution(g))

    func.printScalarDist("Distribuicao\nNode, Betweenness", func.nodeBetweennessDistribution(g))

    func.printScalarDist("Distribuicao\nEdge, Betweenness", func.edgeBetweennessDistribution(g))

    func.printIntervalDist("Distribuicao\nClustering, Numero de nos", func.nodeClusteringDistribution(g))
    print("Coeficiente de clusterizacao global: " + str(func.graphGlobalClusteringCoeff(g))) + "\n\n"

    func.printScalarDist("Distribuicao\nBridgeSpan, Quantidade de arestas", func.bridgeSpanDistribution(g))

elif printInFile == True:

    (avg, dist) =  func.avgDistanceAndDistribution(g)
    print "Distancia media " + str(avg) + "\n"
    func.printScalarDist("Distribuicao\nDistancia, Numero de aresta (nos)", dist, "distance_between_all_nodes.csv")

    func.printIntervalDist("Distribuicao\nGrau, Quantidade de nos por grau", func.degreeDistribution(g), "node_degree.csv")

    func.printScalarDist("Distribuicao\nTamanho Component, Quantidade de nos por componente", func.componentsDistribution(g), "components.csv")

    func.printIntervalDist("Distribuicao\nNeighborhood Overlap, Quantidade de arestas", func.neighborhoodOverlapDistribution(g), "neighborhood_overlap.csv")

    func.printScalarDist("Distribuicao\nNode, Betweenness", func.nodeBetweennessDistribution(g), "node_betweenness.csv")

    func.printScalarDist("Distribuicao\nEdge, Betweenness", func.edgeBetweennessDistribution(g), "edge_betweenness.csv")

    func.printIntervalDist("Distribuicao\nClustering, Numero de nos", func.nodeClusteringDistribution(g), "node_clustering.csv")
    print("Coeficiente de clusterizacao global: " + str(func.graphGlobalClusteringCoeff(g)))

    func.printScalarDist("Distribuicao\nBridgeSpan, Quantidade de arestas", func.bridgeSpanDistribution(g), "bridge_span.csv")
