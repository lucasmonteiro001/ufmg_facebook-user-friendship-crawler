import matplotlib.pyplot as plt
from operator import itemgetter
import networkx as nx

GRAPH_PATH = "graph_structure_02.gexf"

G = nx.read_gexf(GRAPH_PATH)
# find node with largest degree
node_and_degree=G.degree()

(largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]
# Create ego graph of main hub
hub_ego=nx.ego_graph(G,largest_hub)
# Draw graph
pos=nx.spring_layout(hub_ego)
nx.draw(hub_ego,pos,node_color='b',node_size=50,with_labels=False)
# Draw ego as large and red
nx.draw_networkx_nodes(hub_ego,pos,nodelist=[largest_hub],node_size=300,node_color='r')
plt.savefig('ego_graph_less_lucas.png')
plt.show()
