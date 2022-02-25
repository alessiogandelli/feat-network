#%%

import os
from re import A
from dotenv import load_dotenv
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials
import string
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network
from networkx.algorithms import community #This part of networkx, for community detection, needs to be imported separately.

load_dotenv()

id = os.getenv('CLIENT_ID')
secret = os.getenv('CLIENT_SECRET')

#%%
tedua = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(id,secret))

# brutto che sia globale cosi 

#given an artist  retrurs a dictionary with all feats of an artists example: feat['marra'] = [gue, blanco, sfera]
def get_feat(artist_uri,df):
    artist_name = spotify.artist(artist_uri)['name']
    #raw_albums = spotify.artist_albums(artist_uri, album_type='album')

    all_albums = clean_album_gae(artist_uri)
    friends = {}
    for album in all_albums:
        tracks = spotify.album_tracks(str(album[1]))
        for track in tracks['items']:
            for ft in track['artists']:
                
                #if(artist['name'] != artist_name):
                if ft['name'] in artists.keys():
                    if ft['name'] in friends.keys():
                        friends[ft['name']] += 1
                    else:
                        friends[ft['name']] = 1
                    #df.at[ft['name'], artist_name] += 1
                    #df.at[artist_name, artist['name']] = 1
                    #feat.setdefault(artist_name, []).append(ft['name'])  # qui fare +1
                    

                #get uri
                if ft['name'] not in get_uri.keys():
                    get_uri[ft['name']] = ft['uri']
    feat[artist_name] = friends

# faccio i related dei related e ritorna un dizionario nome->uri
def get_related_artists(artist_uri):
    rel = spotify.artist_related_artists(artist_uri) # get related artists
    artists = {} # dict for saving all artists 

    #add related artists 
    for artist in rel['artists']:
        artists[artist['name']] = artist['uri']

    artists2 = artists.copy() #altrimenti non posso iterare ed aggiugere

    #for each related artist add its related artists 
    for artist in artists2.values():
        rel = spotify.artist_related_artists(artist)
        for art in rel['artists']:
            artists[art['name']] = art['uri']

    artists3 = artists.copy() #altrimenti non posso iterare ed aggiugere

    #for each related artist add its related artists 
    for artist in artists3.values():
        rel = spotify.artist_related_artists(artist)
        for art in rel['artists']:
            artists[art['name']] = art['uri']
    
    artists['Tedua'] = artist_uri
    return artists


def clean_album_gae(artist_id):

    album_names = []
    all_albums = spotify.artist_albums(artist_id, album_type='album')
    
    #uri delle vari album
    for album in all_albums['items']:
        album_names.append([album['name'], album['uri']])

    rip = []
    titles = []
    for album in album_names:
        titles.append([album[0].translate(str.maketrans('', '', string.punctuation)), album[1]])
    titles.sort(key=lambda s: len(s[0]))

    for i in range(len(titles)):
        for b in range(len(titles)):
            if(i < b):
                if(set(titles[i][0].split(' ')).issubset(set(titles[b][0].split(' '))) == True):
                    rip.append(b)
    rip = list(set(rip))

    for ele in sorted(rip, reverse = True):
        del titles[ele]
    return titles

#compute df adjacency matrix 
def get_df(artist_uri):
 
    df = pd.DataFrame(columns=artists.keys())

    #get featurings
    for artist in artists.values():
        get_feat(artist,df)

    #fill dataframe
    for artist, friends in feat.items():
        for friend, nfeat in friends.items():
            df.at[artist, friend] = nfeat
    

            
    df = df.fillna(0)
    print(df)
    return df

# %% start from tedua and get related artists 
artists = get_related_artists(tedua)
get_uri = {} 
feat = {} 
df = get_df(tedua)



# %% crea grafo nel file html
# 
# 
#considera solo chi ha fatto più di uno due e tre feat 
df3 = df -3 
df3[df3 < 0] = 0

df2 = df -2 
df2[df2< 0] = 0

df1 = df -1 
df1[df1 < 0] = 0

G0 = nx.from_pandas_adjacency(df) # graph
G1= nx.from_pandas_adjacency(df1) # graph
G2 = nx.from_pandas_adjacency(df2) # graph
G3 = nx.from_pandas_adjacency(df3) # graph

#%% graph analysis 
G = G0
print(nx.info(G))
print(nx.density(G))

#centrality
degree_dict = dict(G.degree(G.nodes()))
betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality

degree_sort =sorted(degree_dict.items(), key= lambda item: item[1], reverse=True)
between_sort = sorted(betweenness_dict.items(),key= lambda item: item[1], reverse=True)
eigen_sort = sorted(eigenvector_dict.items(),key= lambda item: item[1], reverse=True)

nx.set_node_attributes(G, degree_dict, 'degree')
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')


#communities
communities = community.greedy_modularity_communities(G)

modularity_dict = {} 
for com,artists in enumerate(communities): 
    for name in artists: 
        modularity_dict[name] = com

nx.set_node_attributes(G, modularity_dict, 'modularity')



#%%create html file to visualize network topology
net = Network('100%', '100%') # network
net.barnes_hut()
net.show_buttons()
net.from_nx(G, lambda x: list(nx.get_node_attributes(G, 'degree').items())[x][1], lambda y: list(nx.get_edge_attributes(G, 'weight').items())[y][1])
net.show('feat.html')
# %%
