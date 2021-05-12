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
s = set()

s.add(50)
s.add(1)

s.add(22)
s.add(1000)

s.add(0)


w= sorted(s)

print(w)