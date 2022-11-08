# %%
import os
import string
import spotipy
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import json
import igraph as ig
import matplotlib.pyplot as plt
import itertools

load_dotenv()

# Login to the spotify API
cid = os.environ.get("CLIENT_ID")
secret = os.environ.get("CLIENT_SECRET")

spotify = spotipy.Spotify( client_credentials_manager=SpotifyClientCredentials(cid, secret))


class Artist:
    dicArtists = {}
    dicName = {}
    names = {}
    id_iter = itertools.count()


    def __init__(self, artist_uri, autoload=0):
        artist_raw = spotify.artist(artist_uri)
        #print('creating artist', artist_raw['name'])

        self.id = next(Artist.id_iter)
        self.name = artist_raw['name']
        self.uri = artist_raw['uri']
        self.genres = artist_raw['genres']
        self.followers = artist_raw['followers']['total']
        self.popularity = artist_raw['popularity']
        self.tracks = []
        self.feat = {}
        Artist.dicArtists[self.uri] = self
        Artist.names[self.uri] = self.name
        Artist.dicName[self.id] = self.name

        if autoload > 0:
            self.getTracks(autoload - 1)

    # fill the self.feat dictionary with the artists that have collaborated with this artist
    def getFeat(self):

        if len(self.feat) == 0:
            for track in self.getTracks(-1):
                for artist in track.getArtists():
                    if artist.uri != self.uri:


                        if artist.uri in self.feat:
                            self.feat[artist.uri] += 1
                        else:
                            self.feat[artist.uri] = 1
        return self.feat

    # get all tracks of the artist
    def getTracks(self, autoload=0):
        if len(self.tracks) == 0 and autoload >= 0:

            # get albums and singles 
            album_raw_album = spotify.artist_albums(self.uri, album_type= 'album', country='it', limit=50)
            album_raw_single = spotify.artist_albums(self.uri, album_type= 'single', country='it', limit=50)
            album_raw = album_raw_album['items'] + album_raw_single['items']
        
            albums_uri = [album['uri'] for album in album_raw]

            # get all tracks of the artist
            tracks_raw = []
            for a in albums_uri:
                 tracks_raw += spotify.album_tracks(a, limit=50, offset=0, market='it')['items'] 

    
            print(len(tracks_raw), 'tracks found of', self.name)

            # create track objects
            self.tracks = []
            self.tracks = [Track(t, autoload) if t['uri'] not in Track.dicTracks else Track.dicTracks[t['uri']] for t in tracks_raw]
        return self.tracks

    def reset():
        Artist.dicArtists = {}
        Artist.dicName = {}
        Artist.names = {}
        Artist.id_iter = itertools.count()

    # da testare 
    def ego_graph(self):
        g = ig.Graph(directed=True)
        g.add_vertices(len(Artist.dicArtists))
        g.vs['name'] = [Artist.dicName[i] for i in range(len(Artist.dicArtists))]
        g.vs['label'] = g.vs['name']
        g.vs['label_size'] = 8
        g.vs['size'] = 10
        g.vs['color'] = 'lightblue'
        g.vs['shape'] = 'circle'
        g.vs['label_dist'] = 1.5
        g.vs['label_angle'] = 0
        g.vs['label_color'] = 'black'

        for artist in self.feat:
            g.add_edge(self.id, Artist.dicArtists[artist].id, weight=self.feat[artist])

        return g


    def __repr__(self) -> str:
        return f'Artist: {self.name}'
    
    def __str__(self) -> str:
        return 'Artist: ' + self.name + ' - ' + str(len(self.tracks)) + ' tracks'


class Track:
    dicTracks = {}

    def __init__(self, track_raw, autoload=0):
        self.name = track_raw['name']
        self.uri = track_raw['uri']
       # self.album = track_raw['album']['name']
        self.duration = track_raw['duration_ms']
        self.artistsRaw = track_raw['artists']
        self.artists = None
        Track.dicTracks[self.uri] = self

        if autoload > 0:
            self.getArtists(autoload - 1)

    # get all artists of the track
    def getArtists(self, autoload=0):
        if self.artists is None:
            self.artists = [
                Artist(uri, autoload) if uri not in Artist.dicArtists else Artist.dicArtists[uri]
                for uri in [artist_raw['uri'] for artist_raw in self.artistsRaw]
            ]
        return self.artists

    def __repr__(self) -> str:
        return f'Track: {self.name}'

    def reset():
        Track.dicTracks = {}

#%%
def get_graph():
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
# %%


Artist.reset()
Track.reset()
tedua_uri = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7'


tedua = Artist(tedua_uri, 3)
len(Artist.dicArtists)

#%%

Artist.reset()
Track.reset()
marra_uri = 'spotify:artist:5AZuEF0feCXMkUCwQiQlW7'
marra = Artist(marra_uri, 3)



# %%
g = get_graph()
plot_graph(g)

