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





def get_graph(nodes):
    g = ig.Graph()

    for artist in nodes.values():
        g.add_vertex(artist.name,   popularity = artist.popularity, 
                                    genres = artist.genres, 
                                    followers = artist.followers)

    for artist in nodes.values():
        for feat in artist.getFeat().items():
            if feat[0] in nodes:
                # add edge between artist and featured artist
                g.add_edge(artist.name, nodes[feat[0]].name, weight=feat[1])
                
         

    return g

# print all the nodes 
def print_nodes(g):
    for v in g.vs:
        print(v['name'], v['popularity'], v['genres'], v['followers'])



def plot_graph(g):
    fig, ax = plt.subplots(figsize=(100,100))
    ig.plot(
        g,
        target=ax,
        #layout="kamada_kawai", # print nodes in a circular layout
        layout="fr",
        vertex_size=  ['1' if artist > 3 else '0.5' for artist in g.vs['degree']],
        vertex_frame_width=4.0,
        vertex_frame_color="white",
        vertex_label=g.vs["name"],
        vertex_label_size=30.0,
        edge_width = [a for a in g.es['weight']],
        #vertex_color = ['green' if 'italian hip hop' in gen else 'grey' for gen in g.vs['genres']],
        vertex_color = ['#425df5' if artist > 3 else 'grey' for artist in g.vs['degree']],

    )


def generate(uri, depth=3):
    Artist.reset()
    Track.reset()
    artista = Artist(uri, depth)
    print('found ', str(len(Artist.dicArtists)))
    return artista


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
#tedua = generate(uri_tedua,2)
marra = generate(uri_marra,2)

#%%
uri_giorgia = "https://open.spotify.com/artist/0gm1lHoOXAdy5OB4AwFYRr?si=Sdc9yvflRZiVQ_HkrgORjw"
generate(uri_giorgia, 3)

uri_articolo31= 'https://open.spotify.com/artist/1Ij5ZIGlPTkoZibay58zHe?si=m1f7nzqpRDerrSO01ytDAg'
Artist(uri_articolo31, 3)

uri_cugini = 'https://open.spotify.com/artist/3PxABgbDMeYxPK9GGjNg4j?si=MfEaWDmXSSKSvvAJYgXLEQ'
Artist(uri_cugini, 3)

uri_colapesce = 'https://open.spotify.com/artist/2KX2VLr3Eu6sn6EtxzCtvf?si=xCr_S5jhT36egpJixcZiEQ'
Artist(uri_colapesce, 3)

uri_moda = 'https://open.spotify.com/artist/3ALm6zJLaJMWV0r89kuYtu?si=VpcwpcIOThacd3Nul3fNRA'
Artist(uri_moda, 3)

uri_elodie = 'https://open.spotify.com/artist/7GgpsUpkj3olseoaTY7TEY?si=kxtROXZXTtOyiPEe62zCGQ'
Artist(uri_elodie, 3)

url_ultimo = 'https://open.spotify.com/artist/3hN3iJMbbBmqBSAMx5veDa?si=jY-37NoPQaWW3sW2GuxMZQ'
Artist(url_ultimo, 3)

url_mengoni ='https://open.spotify.com/artist/3xGlLcG9CUrs5MvFkSLOS5?si=GCuDnknSQF-21F5yucO8_Q'
Artist(url_mengoni, 3)

url_madame = 'https://open.spotify.com/artist/1vgQksyJ0IVz8y9XerEOy3?si=Lm3Fkz6dQNaStoBl5BsK8g'
Artist(url_madame, 3)

url_grignani = 'https://open.spotify.com/artist/0H1InhXaXQPL1aj0mvHemU?si=lwaE2EVlQ8GdRd7xx04TXA'
Artist(url_grignani, 3)

url_tananai = 'https://open.spotify.com/artist/35V1WomiedCJeGfupcPm7s?si=hInDNsDWQtaPfZO9bdwp9Q'
Artist(url_tananai, 3)

url_ariete = 'https://open.spotify.com/artist/2T4kh33TYdnDesvlQyRst8?si=lkQd9vieRqq8U_xBXV4JGA'
Artist(url_ariete, 3)

uri_mara = 'https://open.spotify.com/artist/0zoMmzmyi8N8LwzhyXPvtk?si=GXNM32maTguBIAPxk4QvbQ'
Artist(uri_mara, 3)

uri_lazza = 'https://open.spotify.com/artist/0jdNdfi4vAuVi7a6cPDFBM?si=n8Zjo7ApTMSEFn8DlP1n_Q'
Artist(uri_lazza, 3)

uri_mrain = 'https://open.spotify.com/artist/59MLbXG0jLVwJup3KAd6m1?si=DodOwQ7HQrSCZg3Zs99wkQ'
Artist(uri_mrain, 3)

uri_comacose = 'https://open.spotify.com/artist/0Sv8sjzMHBbAWXt4CGB9Us?si=sYADHL-3RtKP8LGJqi_l1g'
Artist(uri_comacose, 3)

uri_gassman = 'https://open.spotify.com/artist/5i0snp4GKBLiFsAZAwuJ5b?si=wNY31NnrS9e1OB2OE1vlnA'
Artist(uri_gassman, 3)

uri_rosa = 'https://open.spotify.com/artist/5gYADZXuZoaJwrwfAPbKuH?si=s_2XSjWUSMGcCoEAPvDRJw'
Artist(uri_rosa, 3)

uri_oxa = 'https://open.spotify.com/artist/6iuybPv0Mii8x21mztjaUN?si=MBQPLBA0R4y7m3jIja2rxQ'
Artist(uri_oxa, 3)

uri_paola = 'https://open.spotify.com/artist/6sXWE3eSY59H6zy1tiRPue?si=Ga7h1ZldQCGkJxAqfKobVw'
Artist(uri_paola, 3)

uri_lda = 'https://open.spotify.com/artist/5FwDaIGy29GQC5d0MR7fKf?si=H9OCuBeSSye5sNfbCgeYJQ'
Artist(uri_lda, 3)


#%%
g = get_graph(Artist.dicArtists)
g.vs['degree'] = g.degree()
plot_graph(g)

#%%


#%%

























































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





#%%
#create dataframe 
df = pd.DataFrame(columns = ['player', 'game', 'points'])

for player in data.keys():
    for i, game in enumerate(data[player]):
        for turn in game:
            df = df.append({'player': player, 'game': i+1, 'points': turn}, ignore_index=True)


#plot df 


sns.set(style="whitegrid")
ax = sns.boxplot(x="game", y="points", data=df)
ax = sns.swarmplot(x="game", y="points", data=df, color=".25")
#shape dots based on players
ax = sns.swarmplot(x="game", y="points", data=df, hue='player', palette=['red', 'blue'], size=10, marker='D')

plt.show()
#set the size of the plot
plt.figure(figsize=(10,10))






#%%
#adjacency_matrix = pd.DataFrame( np.zeros((len(nodes), len(nodes)), np.int32),index=nodes, columns=nodes,)

g = ig.Graph()

for artist in nodes.values():
    g.add_vertex(artist.name)

for artist in nodes.values():
    for feat in artist.getFeat().items():
        if feat[0] in nodes:
            # add edge between artist and featured artist
            g.add_edge(artist.name, nodes[feat[0]].name, weight=feat[1])
            

            


          
#%%

# create object graph 
g = ig.Graph(n_vertices, edges)

#%%
g.vs['name'] = [nodes[artist].name for artist in adjacency_matrix.index]
# %%
