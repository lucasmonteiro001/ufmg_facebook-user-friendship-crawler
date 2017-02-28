import networkx as nx
import numpy as np # round float
import re # get rid off special chars
import math
from collections import OrderedDict
from sets import Set
import sys

# Todos os floats do programa sao arredondados para 3 casas decimais
precision = 3

# Imprime Distribuicoes que tem a chave representando um intervalo
def printIntervalDist(message, el, file_output = None):

    if file_output != None:

        file_output = "results/less_LucasMonteiro/" + file_output

        with open(file_output, 'w') as f:
            f.write(message + "\n")
            for key, val in el.iteritems():
                f.write("[" + str(key[0]) + "-" + str(key[1]) + ")," + str(val) + "\n")
    else:

        print (message + "\n")
        for key, val in el.iteritems():
            print ("[" + str(key[0]) + "-" + str(key[1]) + ")," + str(val) + "\n")

# Imprime Distribuicoes que tem a chave representando um escalar
def printScalarDist(message, el, file_output = None):

    if file_output != None:

        file_output = "results/less_LucasMonteiro" + file_output

        with open(file_output, 'w') as f:
            f.write(message + "\n")
            for key, val in el.iteritems():
                f.write(str(key) + "," + str(val) + "\n")
    else:

        print (message + "\n")
        for key, val in el.iteritems():
            print (str(key) + "," + str(val) + "\n")

# Retorna um intervalo no qual o valor deve pertencer
# ex: groupBy(5, 2) retorna [4, 6). Esse eh um intervalo
# que comeca em zero e aumenta de 2 em 2.
def groupBy(val, interval):
    if val < interval:
        return (((0 / interval)), ((np.round(interval,precision))))
    else:
        x = (int(val / interval))
        return (((x * interval)), ((np.round(x * interval + interval,precision))))

# Retorna a distribuicao no seguinte formato
# Dist[<span>] = qut de arestas que possuem esse spam
# Para imprimir, utilize a funcao: printScalarDist()
def bridgeSpanDistribution(graph):

    Dist = {}

    min_bridge_span = 2 # inclusivo

    # percorre os nos do grafo
    for node in graph.nodes():
        # percorre os vizinhos
        for neighbor in list(nx.all_neighbors(graph, node)):
            # remove a aresta entre node e neighbor para calculcar a distancias
            graph.remove_edge(node, neighbor)
            try:
                distance = nx.shortest_path_length(graph, node, neighbor)
            except Exception as e:
                # INF significa que nao ha outra conexao entre os nos, o que diz,
                # com certeza, que essa aresta eh uma ponte
                distance = "INF"

            # Para calcular o numero de bridges, considera-se 0.5 ao inves de
            # 1, pois como o grafo eh bidirecional, vai-se calcular a mesma aresta
            # duas vezes.
            if distance == "INF" or distance >= min_bridge_span:
                try:
                    Dist[distance] = Dist[distance] + 0.5
                    #Dist[distance] = Dist[distance] + [(node, neighbor)]
                except Exception as e:
                    Dist[distance] = 0.5
                    #Dist[distance] = [(node, neighbor)]

            # volta a aresta retirada
            graph.add_edge(node, neighbor)

    return OrderedDict(sorted(Dist.items(), key=lambda t: t[0]))

# Calcula a distancia media do grafo
# Retorna uma tupla (avg_dist, Dist)
# avg_dist = distancia media do grafo
# Dist = distribuicao das distancias do grafo
# Para imprimir, utilize a funcao: printScalarDist()
def avgDistanceAndDistribution(graph):

    try:

        total_distance = 0

        Dist = {}

        for i in graph.nodes():
            for j in graph.nodes():
                # desconsidera a distancia de um no para ele msm
                distance = 0
                if i != j:
                    try:
                        distance = nx.shortest_path_length(graph, i, j)
                        try:
                            Dist[distance] = Dist[distance] + 1
                        except Exception as a:
                            Dist[distance] = 1
                    # se nao ha conexao entre os nos
                    except Exception as e:
                        try:
                            Dist["INF"] = Dist["INF"] + 1
                        except Exception as ee:
                            Dist["INF"] = 1

        avg_distance = nx.average_shortest_path_length(graph)

        return (avg_distance, OrderedDict(sorted(Dist.items(), key=lambda t: t[0])))

    except Exception as e:
        raise e
        print "Not a valid list"

# Calcula a distribuicao de componentes do grafo
# Retorna a distribuicao
# Para imprimir, utilize a funcao: printScalarDist()
def componentsDistribution(graph):
    # obtem todos os componentes
    components = list(nx.connected_component_subgraphs(graph))

    Dist = {}

    for component in components:
        try:
            Dist[len(component.nodes())] = 1 + \
                Dist[len(component.nodes())]
        except Exception as e:
            Dist[len(component.nodes())] = 1

    return Dist

# Calcula a distribuicao de nos por intervalo de graus 5 a 5.
# Retorna Dist[(<valor_inclusivo>, <valor_exclusivo>), Quantidade]
# Para imprimir, utilize a funcao: printIntervalDist()
def degreeDistribution(graph):

    # intervalo que sera considerado para impressao, nesse caso
    # retorna intervalos no seguinte formato:
    # [0, 5), [5, 10) ...
    interval = 5

    Dist = {}

    nodes = graph.nodes()

    for n in nodes:
        degree = graph.degree(n)
        try:
            Dist[groupBy(degree, interval)] = Dist[groupBy(degree, interval)] + 1
        except Exception as e:
            Dist[groupBy(degree, interval)] = 1

    return OrderedDict(sorted(Dist.items(), key=lambda t: t[0]))

# Calcula e retorna a Distribuicao de neighborhoodOverlap par cada no do grafo.
# O intervalo eh de 0.1 em 0.1 para a Distribuicao.
# Para imprimir, utilize a funcao: printIntervalDist()
def neighborhoodOverlapDistribution(graph):

    Dist = {}

    interval = 0.1

    # percorre todos os nos do grafo
    for n in graph.nodes():
        all_neighbors = list(nx.all_neighbors(graph, n))
        # percorre os vizinhos de cada no para calculcar o overlap
        for neighbor in all_neighbors:
            common_neighbors = list(nx.common_neighbors(graph, n, neighbor))

            # checa divisao por zero
            calc = 0.0
            try:
                #calc = (len(list(common_neighbors))) / (len(list(all_neighbors)) +
                    #(len(list(nx.all_neighbors(graph, neighbor)))) - len(list(common_neighbors)) - 2.0)
                calc = (len(list(common_neighbors))) / ((len((set(all_neighbors)) | (set(nx.all_neighbors(graph, neighbor))))) - 2.0)
            except Exception as e:
                calc = 0.0

            try:
                Dist[groupBy(calc, interval)] = Dist[groupBy(calc, interval)] + 1
            except Exception as e:
                Dist[groupBy(calc, interval)] = 1

    return OrderedDict(sorted(Dist.items(), key=lambda t: t[0]))

# Calcula o node betweenness de cada no
# Para imprimir, utilize a funcao: printScalarDist()
def nodeBetweennessDistribution(graph):
    Dist = {}

    betweenness = nx.betweenness_centrality(graph, len(graph.nodes()))

    for key, val in betweenness.iteritems():

        try:
            Dist[np.round(val, precision)] = Dist[np.round(val, precision)] + 1
        except Exception as e:
            Dist[np.round(val, precision)] = 1

    return OrderedDict(sorted(Dist.items(), key=lambda t: t[0]))

# Calcula o edge betweenness de cada aresta
# Para imprimir, utilize a funcao: printScalarDist()
def edgeBetweennessDistribution(graph):
    Dist = {}

    betweenness = nx.edge_betweenness_centrality(graph)

    for key, val in betweenness.iteritems():

        try:
            Dist[np.round(val, precision)] = Dist[np.round(val, precision)] + 1
        except Exception as e:
            Dist[np.round(val, precision)] = 1

    return OrderedDict(sorted(Dist.items(), key=lambda t: t[0]))

# Calcula o coeficiente de clusterizacao para cada no e
# retorna uma Distribuicao por intervalos de 0.1 a 0.1
def nodeClusteringDistribution(graph):

    interval = 0.1

    Dist = {}

    for key, val in nx.clustering(graph).iteritems():

        try:
            Dist[groupBy(val, interval)] = Dist[groupBy(val, interval)] + 1
        except Exception as e:
            Dist[groupBy(val, interval)] = 1

    return OrderedDict(sorted(Dist.items(), key=lambda t: t[0]))

def graphGlobalClusteringCoeff(graph):
    return np.round(nx.average_clustering(graph), precision)

def saveGraphGEXF(graph, path):
    print "\nSaving graph"
    nx.write_gexf(graph, path)
    print "Graph saved into: " + str(path) + "\n"

# g = nx.Graph()
# g.add_edge("a","b"), g.add_edge("a","c"), g.add_edge("a","d")
# g.add_edge("a","e"), g.add_edge("a","f"), g.add_edge("b","h")
# g.add_edge("b","i"), g.add_edge("b","l"), g.add_edge("b","m")
# g.add_edge("c","d"), g.add_edge("c","e"), g.add_edge("c","f")
# g.add_edge("d","e"), g.add_edge("f","j"), g.add_edge("f","g")
# g.add_edge("g","j"), g.add_edge("g","h"), g.add_edge("g","k")
# g.add_edge("h","i"), g.add_edge("h","k"), g.add_edge("i","l")
# g.add_edge("i","m"), g.add_edge("l","m")
