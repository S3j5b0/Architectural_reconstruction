from pyvis.network import Network
'''
net = Network(directed=True)


net.add_node(0, label="two")

net.add_node(1, label="two")
net.add_node(2, label="two", shape="box", color="#e9ec0a")

net.add_edge(1, 2)
try:
    net.add_edge(1, 3)
except:
    print("courld not add")    

net.show("basic.html")


'''
import re
l = {}

l["hi"] = [10]
l["pik"] = [90]
l["hi"].append(1000)
print(len(l))


print(l["hi"])



for k,v in l.items():
    print("k: " + str(k) + " v: " + str(v))


print("_______________________________-")


for k in l:
    print("k: " + str(k))