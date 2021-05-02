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


#Path(ZEEGUU_CORE_FOLDER).rglob("*.py")


from pathlib import Path

def extract_importandClass_from_line(unline):
    # TODO: think about how to detect imports when
    # they are inside a function / method
    x = re.search("^import (\S+)", unline) 
    x = re.search("^from (\S+)", unline) 
    return x.group(1)#, c.group(1).split('(')[0]
def extractClass(inline):
   # print(inline)
    c = re.search("^class (\S+)", inline) 
    return c.group(1).split('(')[0]


def importsAndClass(file):
    lines = [line for line in open(file)]
    classes = []
    all_imports = []
    for line in lines:
        try:
            imports = extract_importandClass_from_line(line)
            all_imports.append(imports)

        except:
            try:
                class1 = extractClass(line)
                classes.append(class1)
            except:
                continue  
  

    return all_imports, classes



G = nx.DiGraph()
nodes = set()
allImports = set()

for file in Path(rootDir).rglob("*.py"):
    f = open(file, "r")
    s = f.read()
    print("_____________________________________________")
    nodes.add(file.name.split)
    print(file)
    print(type(file))
    print(os.path.splitext(file.name)[0])
    ANALyzer = ComplexityVisitor.from_code(s)
    print("complexity: " + str(ANALyzer.total_complexity))
    iss, classes = importsAndClass(file)
    for i in iss:
        allImports.add(i)
    print("classes:")
    print(classes)
    print("imports:")
    print(iss)
    print("_____________________________________________")


#zeeguu_core.bookmark_quality.negative_qualities

print(nodes)
print(len(nodes))

print(allImports)
print(len(allImports))
print("=================================")
for i in allImports:
    if not i in nodes:
        print(i)
f = open("sampleFile.py", "r")

