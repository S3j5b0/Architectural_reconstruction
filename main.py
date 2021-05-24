import ast
from radon.visitors import ComplexityVisitor
import re
import os
from pyvis.network import Network
from pydriller import RepositoryMining


class Vert:
    def __init__(self, name, id, size ,edges,importedDirs,directory):
        self.name = name
        self.size = size
        self.edges = edges
        self.id = id
        self.importedDirs = importedDirs
        self.parentDir = directories
        
from pathlib import Path

rootDir = "/home/ask/Git/tweeda/"
directories = set()
# this is horrible
for file in Path(rootDir).rglob("*.py"):
    try:
        x = re.match("(.*\/)", str(file).replace(rootDir, '')).group(1)[:-1]
        directories.add(x)
    except AttributeError:
        continue
    except:
        print("error in making dir ")
        quit()    

#    print(str(file).replace(rootDir, ""))
 #   localDirs = str(file).split('/')

def extract_importandClass_from_line(unline):

    x = re.search("^import (\S+)", unline) 
    x = re.search("^from (\S+)", unline) 
    return x.group(1)#, c.group(1).split('(')[0]
def extractClass(inline):
    c = re.search("^class (\S+)", inline) 
    return c.group(1).split('(')[0]


def importsAndClassAndgetParent(file):
    lines = [line for line in open(file)]
    classes = []
    all_imports = []
    ParentDir = ""
    try:
        
        ParentDir = re.match("(.*\/)", str(file).replace(rootDir, '')).group(1)[:-1]
    except:
        print("error in creating parent: " + str(file))
      #  print("error making parent for: " + str(file))
        
    for line in lines:
        try:
            imports = extract_importandClass_from_line(line)
            tmp = imports.rsplit('.',1)
            importEnd = tmp[-1]
            importsFormatted = imports.replace('.', '/')
            all_imports.append(importsFormatted)
        except:
            try:
                class1 = extractClass(line)
                classes.append(class1)
            except:
                continue  
  
    return all_imports, classes, ParentDir
    
churn_per_file = {}
for commit in RepositoryMining("/home/ask/Git/Zeeguu-API").traverse_commits():
    for modified_file in commit.modifications:
        churn = modified_file.removed + modified_file.added
        if modified_file.new_path not in churn_per_file: # Here you should keep track of renaming, add a new "if-else"
            churn_per_file[modified_file.new_path] = 0
        churn_per_file[modified_file.new_path] = churn_per_file[modified_file.new_path] + churn


net = Network(directed=True, height="1500px", width="100%")
nodes = {}
idsInDirectory = {} #(directory, set(id))

importedNodes = set() # I use this to keep track of files that have been imported somewhere
nodeNames = set()
counter = 0

for file in Path(rootDir).rglob("*.py"):
    # Opening file, and looking at contents
    f = open(file, "r")
    s = f.read()
    # analyzing complexity
    filename = str(file).replace(rootDir, "")
    analyzer = ComplexityVisitor.from_code(s)



    # getting the file name 
    splitFile = os.path.splitext(file.name)
    #getting imports    
    imports, classes, ParentDirectory = importsAndClassAndgetParent(file)

    importedNodes.update(set(imports))




    nodeNames.add(str(filename))
    v = Vert(str(filename), counter,analyzer.total_complexity, imports,[], "")
    #creating vertex
    nodes[v.name] = v
    counter = counter + 1 
    

    if ParentDirectory in idsInDirectory and ParentDirectory != "":
        idsInDirectory[ParentDirectory].append(counter)
    else:
        idsInDirectory[ParentDirectory] = [counter]
    colorval = (255 - (50 + churn_per_file[v.name]  * 2)) % 255
    print()

    net.add_node(v.id, label=v.name, size=v.size*2, scaling={"label": {"min": 100000, "max": 200000}}, color='#%02x%02x%02x' % (colorval, colorval, colorval))


dirNodes = {} # (id, label)
importedDirs = set()
for k, v in nodes.items():
    for i in v.edges:
        withPY = i + ".py"
        
        try:
            to = nodes[withPY].id 
            net.add_edge(v.id, to, color="#ec320a")
        except:
            if str(i) in directories and str(i) not in importedDirs and v.name.replace(".py", "") not in importedNodes:
                counter = counter + 1 

                net.add_node(counter, label=str(i),size=15, shape="box", color="#eff542")
                net.add_edge(v.id, counter,color="#ec320a")
                importedDirs.add(str(i))

                for b in idsInDirectory[str(i)]:
                    net.add_edge(counter, b,color="#eff542")

            else:
                print("could not add edge to:" + str(i))    
        
net.barnes_hut(overlap=1)
#net.force_atlas_2based(overlap= 1)
net.show("network.html")