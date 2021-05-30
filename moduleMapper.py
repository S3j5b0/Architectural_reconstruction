import os
import sys
import re
import networkx as nx
from pyvis.physics import Physics
from radon.visitors import ComplexityVisitor
import matplotlib.pyplot as plt
from pyvis.network import Network
from datetime import datetime

#/home/ask/Git/Zeeguu-API"
rootDir = sys.argv[1]
depth = int(sys.argv[2])
showdeps = False
try:
    dflag = sys.argv[3]
    if dflag == "-d" or "--d" or "-D" or "--D" or "-Directories":
        showdeps = True
except:
    showdeps = False


class directory:
    def __init__(self,path, ParentDir = None,ChildrenDirs = [] , PyChildren = []) -> None:
        self.path = path
        self.parentDir = ParentDir
        self.pyChildren = ChildrenDirs
        self.pyChildren = PyChildren


def getComplexityoffile(file : str):
    f = open(file, "r")
    s = f.read()
    return ComplexityVisitor.from_code(s).total_complexity        
 
def getParentOfDir(dir: str):
    cutlast = dir.split("/")[:-1]
    join = "/".join(cutlast)
    if join:
        return join
    else:
        return "./"

def extract_importandClass_from_line(unline):

    x = re.search("^import (\S+)", unline) 
    x = re.search("^from (\S+)", unline) 
    return x.group(1)#, c.group(1).split('(')[0]



def getimportsforfile(file):
    lines = [line for line in open(file)]
    classes = []
    all_imports = []

        
    for line in lines:
        try:
            imports = extract_importandClass_from_line(line)
            tmp = imports.rsplit('.',1)
            importEnd = tmp[-1]
            # importsimports
            importsFormatted = imports.replace('.', '/')
            finalimport = importsFormatted[1:] if importsFormatted.startswith('/') else importsFormatted
            all_imports.append(importsFormatted)
        except:
            continue
            
  
    return all_imports


churn_per_file = {}
from pydriller.metrics.process.code_churn import CodeChurn

metric = CodeChurn(path_to_repo =rootDir, 
                   since=datetime(2008, 1, 1), 
                   to=datetime.now(), 
                   ignore_added_files=True)

churn_per_file = metric.count()





NodesAndComplexity = {} # (node/complexity in folder)

# ting jeg vil bruge til at holdestyr på dependencies
Map_Dirs_And_Files_To_Displaybledirs = {}
pythonFile_to_imports = {} # (Fille importing, file/dir imported)




dirsForDisplay = set()
# mapping files to parent directories
parenDirToChildDir = {} # (parent, [list of children])

# churn metrics
noChurnCounter  = 0
DisplayableDirToChurn = {}
G = nx.DiGraph()
isRoot = True
for root, dirs, files in os.walk(rootDir):
    pyfiles = list(filter(lambda a : a.endswith('.py'), files)) 
    thisDir = root.replace(rootDir, '')
    splitDIR = thisDir[1:].split("/")[:depth]
    if not isRoot:
        displayableDir = "/" + "/".join(splitDIR)
    else:
        displayableDir = "./"
        isRoot = False
    # if there is python files on this directory 

    referentialDIr = thisDir[1:] if thisDir.startswith('/') else thisDir

    Map_Dirs_And_Files_To_Displaybledirs[referentialDIr] = displayableDir
    if (pyfiles):
        accumulateComplexity = 0
        for f in pyfiles:
            churnPath = thisDir[1:] + "/"+ f
            # getting churn for file:
            if churnPath in churn_per_file:
                if displayableDir == "/zeeguu_core_test/rules":
                    print("this right here")
                if displayableDir not in DisplayableDirToChurn:
                    DisplayableDirToChurn[displayableDir] = abs(churn_per_file[churnPath])
                 #   print(abs(churn_per_file[churnPath]))
                  #  print(displayableDir + " | "+str(DisplayableDirToChurn[displayableDir]) )
                else:
                    DisplayableDirToChurn[displayableDir] = DisplayableDirToChurn[displayableDir] + abs(churn_per_file[churnPath])
                  #  print(abs(churn_per_file[churnPath]))
                   # print(displayableDir + " | "+str(DisplayableDirToChurn[displayableDir]) )

   
            filepath = root + "/"+ f
            imports = getimportsforfile(filepath)
            logFile = thisDir + "/" + f[:-3]
            accumulateComplexity = accumulateComplexity + getComplexityoffile(filepath)

            removedslashFromLogfile = logFile[1:] if logFile.startswith('/') else logFile
            Map_Dirs_And_Files_To_Displaybledirs[removedslashFromLogfile] = displayableDir
            pythonFile_to_imports[removedslashFromLogfile] = imports

        if displayableDir not in NodesAndComplexity:
            NodesAndComplexity[displayableDir] = accumulateComplexity
            
        else:
            NodesAndComplexity[displayableDir] = NodesAndComplexity[displayableDir] + accumulateComplexity
          


        if (displayableDir not in dirsForDisplay):
            dirsForDisplay.add(thisDir)
            G.add_node(displayableDir, Physics=False, scaling={"label": {"min": 800000000, "max": 200000000000}})
            if not isRoot and displayableDir != "./":
                parent = getParentOfDir(displayableDir)
                G.add_edge(parent, displayableDir, color='black')


# setting node sizes

if showdeps:
    for importingfile, importlist in  pythonFile_to_imports.items():

        for importt in importlist:
            if importt in Map_Dirs_And_Files_To_Displaybledirs:
                fromf = Map_Dirs_And_Files_To_Displaybledirs[importingfile]
                to =  Map_Dirs_And_Files_To_Displaybledirs[importt]
                if fromf != to:
                    G.add_edge(Map_Dirs_And_Files_To_Displaybledirs[importingfile],Map_Dirs_And_Files_To_Displaybledirs[importt], color="red")


for k,v in DisplayableDirToChurn.items():
    print(k + " | " + str(v))

for node in G.nodes:
    try:
        churnMin = 255- abs(int(DisplayableDirToChurn[node]/3))
        G.nodes[node]["color"]  ='#%02x%02x%02x' % (churnMin, churnMin, churnMin)
       
    except KeyError:
        G.nodes[node]["color"]  ='#%02x%02x%02x' % (255, 255, 255)

                   

for node, complexity in NodesAndComplexity.items():
    complexixtyDisplay = complexity / 2
    G.nodes[node]["size"] = complexixtyDisplay


Displayer = Network(directed=True, height="1500px", width="100%")

Displayer.from_nx(G)
Displayer.barnes_hut(overlap=1)

Displayer.show_buttons(filter_=["physics"])
Displayer.show("Depth_1_graph_Depend2.html")    


