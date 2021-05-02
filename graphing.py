
class Vert:
  
    # default constructor
    def __init__(self, name, size, edges):
        self.name = name
        self.size = size
        self.edges = edges


import networkx as nx
import matplotlib.pyplot as plt

nodes = []
nodes.append(Vert('A', 100, ['B', 'C']))
nodes.append(Vert('B', 300, ['D']))
nodes.append(Vert('C', 400, ['D']))
nodes.append(Vert('D', 700, []))




G = nx.DiGraph()
for v  in nodes:
    G.add_node(v.name)
    for e in v.edges:
        G.add_edge(v.name, e)



nx.shortest_path(G, 'A', 'D', weight='weight')



node_sizes = [V.size for V in nodes]
plt.figure(figsize=(20,20))
nx.draw(G, font_weight='bold', with_labels = True, node_size=node_sizes)
plt.show()





