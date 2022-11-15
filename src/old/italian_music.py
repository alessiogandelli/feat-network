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
from utils import Artist, Track
load_dotenv()


# Login to the spotify API
cid = os.environ.get("CLIENT_ID")
secret = os.environ.get("CLIENT_SECRET")
spotify = spotipy.Spotify( client_credentials_manager=SpotifyClientCredentials(cid, secret))



#%%
def get_related_artists(artist):
    rel = spotify.artist_related_artists(artist) # get related artists
    artists = {} # dict for saving all artists 

    #add related artists 
    for artist in rel['artists']:
        artists[artist['name']] = artist['uri']

    return artists


uri_tedua = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7'
uri_jova = 'spotify:artist:7tmMPdOmFvdRvbj2aWoiRi'
uri_coez =  'spotify:artist:5dXlc7MnpaTeUIsHLVe3n4'


Artist()

def get_graph(n_vertices, nodes):



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


# %%
jova_rel = get_related_artists(uri_jova)


for artist in jova_rel.values():
    a = Artist(artist, 3)
# %%

g = get_graph(len(Artist.dicArtists), Artist.dicArtists)

# %%
plot_graph(g)

#%%
#export graph to gephi
g.write_gml('graph.gml')

# %%


g
# %%
uri_tedua = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7' #tedua 
tedua = get