#%%
from random import seed
from pyvis.network import Network
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
# %%

# read csv pandas
df = pd.read_csv('/Users/alessiogandelli/Desktop/cantiere/feat-network/data/feat_sixseven.csv', index_col=0)
# %%

G = nx.from_pandas_adjacency(df) 
# %%
pos = nx.spring_layout(G)
nx.draw(G, pos)
plt.show()
# %%
