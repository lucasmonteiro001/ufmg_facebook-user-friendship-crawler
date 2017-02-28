import urllib, json
import sys
import networkx as nx
import time
from sets import Set

ACCESS_TOKEN = "CAACEdEose0cBALvnni2V7Bh7AccJYDPv2L0mZBXY7n9D8zNZAed5ywOZCpZBFvsnApOlSwx4jxIYLrZCYRDf2XHsUbAmAW1ZC4vrXPxFjmaN1nWX7BveBiH1VmNpyD9X6AjJpNySxPoQjrv2UIxLALJp7DWhGcZAlYpjSp1WreFNZAdUne50CzQVM9MChhUhZCBzucWpaSgXpRQZDZD"
PARAMS_PHOTOS = "&debug=all&fields=photos%7Btags%2Cfrom%7D&format=json&method=get&pretty=0&suppress_http_code=1"
PARAMS_VIDEOS = "&debug=all&fields=videos%7Bfrom%2Ctags%7D&format=json&method=get&pretty=0&suppress_http_code=1"
PARAMS_POSTS = "&debug=all&fields=posts%7Bfrom%2Cwith_tags%7D&format=json&method=get&pretty=0&suppress_http_code=1"
PARAMS_TAGGED = "&debug=all&fields=tagged%7Bfrom%2Cwith_tags%7D&format=json&method=get&pretty=0&suppress_http_code=1"
MY_FB_ID = "850911658301019"
MY_FB_NAME = "Lucas Monteiro"

def buildURL(access_token, parameters):
	url = "https://graph.facebook.com/v2.4/me?access_token=" + access_token + parameters
	return url

def getFirstPages(element, access_token, parameters):
	try:
		previousPage = None
		url = buildURL(access_token, parameters)
		response = urllib.urlopen(url)
		data = json.loads(response.read())

		nextPage = data[element]["paging"]["next"]

		return (previousPage, nextPage, data)
	except Exception as e:
		raise e
		print "Problems with internet connection!"

def getNextPage(currentPageURL):
	try:
		response = urllib.urlopen(currentPageURL)
		currPageData = json.loads(response.read())
		nextPage = currPageData["paging"]["next"]
		# agora a pagina atual sera a pagina anterior
		previousPage = currentPageURL

		return (previousPage, nextPage, currPageData)
	except Exception as e:
		raise e
		print "Problems with internet connection!"

def printPages(p1, p2):
	print str(p1) + "\n" + str(p2) + "\n"

def makeConnections(lst, graph):
	# faz as conexoes entre todos os elementos da lista
	for i in xrange(len(lst)):
		for j in xrange(len(lst)):
			# desconsidera self-loops
			if lst[i] != lst[j]:
				if not graph.has_edge(lst[i], lst[j]):
					graph.add_edge(lst[i], lst[j])

# Essa funcao sempre deve receber o array que contem os dados principais
# ex: [photos][data]
def extract(data, graph):
	numberOfElements = len(data)

	# obtem os dados de cada elemento, salvando
	# as ids de from e tags | with_tags
	for i in xrange(numberOfElements):
		# salva os dados do criador do post/photo/tag se ha mais de uma tag
		_from = data[i]["from"]

		all_tagged_elements = Set([(_from["name"]).encode('ascii', 'ignore').decode('ascii')])

		key = None

		if "tags" in data[i]:
			key = "tags"
		elif "with_tags" in data[i]:
			key = "with_tags"
		else:
			key = None

		if key != None:
			tags = data[i][key]["data"]
			# cria uma lista (sem elementos duplicados), com todos os nos
			# da relacao
			for j in xrange(len(tags)):
				all_tagged_elements.add((tags[j]["name"]).encode('ascii', 'ignore').decode('ascii'))
				all_tagged_elements.add((MY_FB_NAME).encode('ascii', 'ignore').decode('ascii'))

			makeConnections(list(all_tagged_elements), graph)
		# parte especifica para tratar elementos do mode tagged
		elif _from["id"] != MY_FB_ID:
			makeConnections([(_from["name"]).encode('ascii', 'ignore').decode('ascii'),(MY_FB_NAME).encode('ascii', 'ignore').decode('ascii')], graph)

def printGraphInfo(graph):
	print "=========================="
	print "\n"
	print "Numero de nos: " + str(len(graph.nodes()))
	print "Numero de arestas: " + str(len(graph.edges())) + "\n"
	print "Nos: " + str(graph.nodes())
	print "\n\n"
	for node in graph.nodes():
		print node + " [" + str(len(graph.neighbors(node))) + "]"
		print graph.neighbors(node)
		print
	print "\n"
	print "Numero de nos: " + str(len(graph.nodes()))
	print "Numero de arestas: " + str(len(graph.edges())) + "\n"
	print "=========================="

def collect(mode, access_token, params, graph):

	(previousPage, nextPage, data) = getFirstPages(mode, access_token, params)

	extract(data[mode]["data"], graph)

	hasNext = True

	print "\n\nInitializing crawler in mode: " + mode + "\n"

	i = 0
	# processo para ler as paginas da web
	while hasNext:
		try:
			print i

			(previousPage, nextPage, data) = getNextPage(nextPage)

			extract(data["data"], graph)

			# Se a pagina anterior for igual a pagina inicial,
			# nao ha mais pagina para se percorrer e encerra a leitura
			if nextPage != previousPage:
				previousPage = nextPage
				i = i + 1
			else:
				hasNext = False
		except Exception as inst:
			print "Finish reading"
			print inst
			hasNext = False

# Funcao principal que retorna o grafo coletado
def main_getGraph():
	graph = nx.Graph()
	collect("posts", ACCESS_TOKEN, PARAMS_POSTS, graph)
	collect("photos", ACCESS_TOKEN, PARAMS_PHOTOS, graph)
	collect("tagged", ACCESS_TOKEN, PARAMS_TAGGED, graph)

	return graph
