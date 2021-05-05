import ast
from radon.visitors import ComplexityVisitor
import re
import os
import networkx as nx
import matplotlib.pyplot as plt

class Vert:
    def __init__(self, name, size, path ,edges):
        self.name = name
        self.size = size
        self.path = path
        self.edges = edges

rootDir = "/home/ask/Git/Zeeguu-API/"




from pathlib import Path

def extract_importandClass_from_line(unline):

    x = re.search("^import (\S+)", unline) 
    x = re.search("^from (\S+)", unline) 
    return x.group(1)#, c.group(1).split('(')[0]
def extractClass(inline):
    c = re.search("^class (\S+)", inline) 
    return c.group(1).split('(')[0]


def importsAndClass(file):
    lines = [line for line in open(file)]
    classes = []
    all_imports = []
    for line in lines:
        try:
            imports = extract_importandClass_from_line(line)
            all_imports.append(imports.rsplit('.',1)[-1])
        except:
            try:
                class1 = extractClass(line)
                classes.append(class1)
            except:
                continue  
  
    return all_imports, classes

G = nx.DiGraph()
nodes = set()
nodeNames = set()
for file in Path(rootDir).rglob("*.py"):
    # Opening file, and looking at contents
    f = open(file, "r")
    s = f.read()
    # analyzing complexity
    analyzer = ComplexityVisitor.from_code(s)
    # getting the file name 
    splitFile = os.path.splitext(file.name)
    #getting imports    
    imports, classes = importsAndClass(file)
    if splitFile[0] not in nodeNames:
        nodeNames.add(splitFile[0])
        v = Vert(splitFile[0], analyzer.total_complexity, file, imports)
    else:
        nodeNames.add(file)
        v = Vert(file, analyzer.total_complexity, file, imports)
    

    #creating vertex
    
    nodes.add(v)


for vert in nodes:
    G.add_node(vert.name)
    for i in vert.edges:
        if i in nodeNames:
            G.add_edge(vert.name, i)

node_sizes = [V.size * 100  for V in nodes]


plt.figure(figsize=(100,100))
nx.draw(G, font_weight='bold', with_labels = True, node_size=node_sizes)
plt.savefig('model.png', bbox_inches='tight')

#plt.show()



#zeeguu_core.bookmark_quality.negative_qualities

