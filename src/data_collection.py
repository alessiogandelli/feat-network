# %%
import pandas as pd
import igraph as ig
import numpy as np
from utils import Artist, Track
import matplotlib.pyplot as plt
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import os
import itertools
load_dotenv()


# Login to the spotify API
cid = os.environ.get("CLIENT_ID")
secret = os.environ.get("CLIENT_SECRET")
spotify = spotipy.Spotify( client_credentials_manager=SpotifyClientCredentials(cid, secret))




#%%
def get_graph(n_vertices, nodes):
    n_vertices = len(Artist.dicArtists)
    nodes =  Artist.dicArtists.copy()


    edges = []
    weights = []

    # add egges 
    for artist in nodes.values():

        for feat in artist.getFeat().items():
            if feat[0] in nodes:
            
                edges.append((artist.id, nodes[feat[0]].id))
                weights.append(feat[1])
                
         

    # create object graph 
    g = ig.Graph(n_vertices, edges)
    g.vs['name'] = [ n.name for n in nodes.values()]
    g.es['weight'] = weights
    g.vs['popularity'] = [ n.popularity for n in nodes.values()]
    g.vs['genres'] = [n.genres if len(n.genres) > 0 else ['none'] for n in nodes.values()]
    g.vs['followers'] = [n.followers for n in nodes.values()]

    return g


def plot_graph(g):
    fig, ax = plt.subplots(figsize=(30,30))
    ig.plot(
        g,
        target=ax,
        layout="kamada_kawai", # print nodes in a circular layout
        vertex_size=  [p/100 for p in g.vs['popularity']],
        vertex_frame_width=4.0,
        vertex_frame_color="white",
        vertex_label=g.vs["name"],
        vertex_label_size=15.0,
        edge_width = [a/2-2 for a in g.es['weight']],
        vertex_color = ['green' if 'italian hip hop' in gen else 'grey' for gen in g.vs['genres']],

    )


def generate(uri, depth=3):
    Artist.reset()
    Track.reset()
    artista = Artist(uri, depth)
    print('found ', str(len(Artist.dicArtists)))
    return artista

# %%

def membership_to_colour(membership):
    # membership to pandas dataframe
    df = pd.DataFrame(membership, columns=['cluster'])
    # get the number of clusters
    n_clusters = len(df['cluster'].unique())
    # create a list of colours
    colours = [plt.cm.Spectral(each) for each in np.linspace(0, 1, n_clusters)]

    return colours

#%%

uri_tedua = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7' #tedua 
uri_marra = 'spotify:artist:5AZuEF0feCXMkUCwQiQlW7' #marra
tedua = generate(uri_tedua,2)







#%%



# create incidence matrix betwee tracks and artists with labels
#%%
incidence_matrix = pd.DataFrame(0, index=Track.dicTracks.values(), columns=Artist.dicArtists.values())
song_pop = []
artist_pop = {}

for track in Track.dicTracks.values():
    if len(track.getArtists()) > 0 :
        for artist in track.getArtists():
            incidence_matrix[artist][track] = track.popularity
            artist_pop[artist] = artist.popularity



# remove tracks with all zeros
incidence_matrix = incidence_matrix.loc[:, (incidence_matrix != 0).any(axis=0)]

#%%
g = ig.Graph.Incidence(incidence_matrix.values.tolist(), mode=ig.ADJ_UNDIRECTED, weighted = True)

# add names to the vertices the vertexes are songs and then artists 
g.vs['name'] =  incidence_matrix.index.tolist()+ incidence_matrix.columns.tolist()
g.vs['popularity'] = list(incidence_matrix.max(axis=1))+ list(artist_pop.values())


#%% plot bipartite graph 
fig, ax = plt.subplots(figsize=(50,50))
ig.plot(
    g,
    target=ax,
    layout= "auto", 
    vertex_label=g.vs["name"],
    vertex_shape = ['circle' if v else 'square' for v in g.vs['type']],
    vertex_color = ['green' if v else 'red' for v in g.vs['type']],
    vertex_size=  [p/50 for p in g.vs['popularity']],
    vertex_label_size=25.0,

)

# plot different shape in the bipartite graph
#%%
#export to gml
g.write_gml('tedua.gml')






















































# %%

n_vertices = len(Artist.dicArtists)
nodes =  Artist.dicArtists.copy()

g = get_graph(n_vertices, nodes)

# compute centrality measures
g.vs['degree'] = g.degree()
g.vs['betweenness'] = g.betweenness()
g.vs['closeness'] = g.closeness()
g.vs['eigenvector_centrality'] = g.eigenvector_centrality()


# %%
# community detection using edge betweenness

dendrogram = g.community_edge_betweenness()
clusters = dendrogram.as_clustering()
membership = clusters.membership
g.vs['membership'] = membership



# %%
# print all with colored clusters 
colours = membership_to_colour(membership)
fig, ax = plt.subplots(figsize=(30,30))
ig.plot(
    g,
    target=ax,
    layout="kamada_kawai", # print nodes in a circular layout
    vertex_size=  [p/100 for p in g.vs['popularity']],
    vertex_frame_width=4.0,
    vertex_frame_color="white",
    vertex_label=g.vs["name"],
    vertex_label_size=15.0,
    edge_width = [a/2-2 for a in g.es['weight']],
    vertex_color = colours,
    )
# %%
# select members of cluster 0 and create a subgraph
g0 = g.vs.select(membership=0).subgraph()
plot_graph(g0)






