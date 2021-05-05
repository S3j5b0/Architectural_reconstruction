
class Vert:
  
    # default constructor
    def __init__(self, name, size, edges):
        self.name = name
        self.size = size
        self.edges = edges


import networkx as nx
import matplotlib.pyplot as plt

nodes = []
nodes.append(Vert('A', 1, ['B', 'C']))
nodes.append(Vert('B', 3, ['D']))
nodes.append(Vert('C', 4, ['D']))
nodes.append(Vert('D', 7, []))
nodes.append(Vert('Y', 64, []))

G = nx.DiGraph()
for v  in nodes:
    G.add_node(v.name, s='v')
    for e in v.edges:
        G.add_edge(v.name, e)

node_sizes = [V.size * 100 for V in nodes]
shapes = set((aShape[1]["s"] for aShape in G.nodes(data = True)))



nx.draw(G, font_weight='bold', with_labels = True, node_size=node_sizes, node_shape= shapes)

#plt.savefig('plot.png', bbox_inches='tight')
plt.show()





