#%%
# import networkx as nx
from random import seed
from pyvis.network import Network
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.
import pandas as pd
import networkx as nx
# %%
df = pd.read_csv('/Users/alessiogandelli/Desktop/cantiere/feat-network/data/feat_tedua.csv', index_col=0)
# %%
G0 = nx.from_pandas_adjacency(df) 

# set lenght of the edges based on the weight

# %%


# use attribute length for edge length pyvis
G = Network(notebook=True, height='750px', width='100%', bgcolor='#222222', font_color='white')
G.from_nx(G0)

# %%
net = Network('1000px', '1000px', filter_menu=True)
net.from_nx(G0)
net.barnes_hut()
net.show('test.html')
# %%
import matplotlib.pyplot as plt



for u, v, d in G0.edges(data=True):
    d['len'] = 1 + 10/ (d['weight']+1)

remove = [node for node,degree in dict(G0.degree()).items() if degree == 0]
G0.remove_nodes_from(remove)
G0.remove_edges_from(list(nx.selfloop_edges(G0)))


plt.figure(figsize=(100,100))
pos = nx.spring_layout(G0, weight= 'len',seed=420)

nx.draw(G0, 
        pos,
        with_labels = True, 
        font_size=40,
        prog='neato',
        )
#%%
import pygraphviz as PG
G = PG.AGraph()
#take fata from G1 and plot
G.add_nodes_from(G0.nodes())
G.add_edges_from(G0.edges())
G.layout(prog='neato')
G.draw('test.png')


# %%
import networkx as NX
import pygraphviz as PG

G = PG.AGraph()
nlist = "A B C D E".split()
a, b = "A A B", "B C D"
elist = zip(a.split(), b.split())

G.add_nodes_from(nlist)
G.add_edges_from(elist)
G.node_attr.update(color="red", style="filled")
G.edge_attr.update(color="blue", len="2.0", width="2.0")

print(G.edge_attr)
# returns {'color': 'red', 'width': '', 'len': '2.0'}

# add new edge with custom length (all others have length=2.0):
G.add_edge("C", "E", len="3.0", color="blue", width="2.0")

edge = G.get_edge("C", "E")
print(edge_attr)
# returns {'color': 'blue', 'width': '2.0', 'len': '3.0'}

# and you can confirm that introspection by drawing & printing this graph:
G.draw('somefolderandfilename.png', format='png', prog='neato')



# %%
