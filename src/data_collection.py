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


# %%
class Artist:
    dicArtists = {}
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
        self.tracks = None
        self.feat = {}
        Artist.dicArtists[self.uri] = self
        Artist.names[self.uri] = self.name

        if autoload > 0:
            self.getTracks(autoload - 1)

    def getFeat(self):

        if len(self.feat) == 0:
            for track in self.getTracks():
                for artist in track.getArtists():
                    if artist.uri != self.uri:


                        if artist.name in self.feat:
                            self.feat[artist.uri] += 1
                        else:
                            self.feat[artist.uri] = 1
        return self.feat

    def getTracks(self, autoload=0):
        if self.tracks is None:
            #query = 'artist:' + self.name

            # raw_tracks1 = spotify.search( query, limit=50, type='track', market='it', offset=0)['tracks']['items']
            # raw_tracks2 = spotify.search( query, limit=50, type='track', market='it', offset=50)['tracks']['items']
            # raw_tracks = raw_tracks1 + raw_tracks2

            album_raw_album = spotify.artist_albums(self.uri, album_type= 'album', country='it', limit=50)
            album_raw_single = spotify.artist_albums(self.uri, album_type= 'single', country='it', limit=50)
            album_raw = album_raw_album['items'] + album_raw_single['items']
            albums_uri = [album['uri'] for album in album_raw]
            tracks_raw = []
            for a in albums_uri:
                 tracks_raw += spotify.album_tracks(a, limit=50, offset=0, market='it')['items'] 

    

            print(len(tracks_raw), 'tracks found of', self.name)
            self.tracks = []


            self.tracks = [Track(t, autoload) if t['uri'] not in Track.dicTracks else Track.dicTracks[t['uri']] for t in tracks_raw]
        return self.tracks


    def __repr__(self) -> str:
        return f'Artist: {self.name}'


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

    def getArtists(self, autoload=0):
        if self.artists is None:
            self.artists = [
                Artist(uri, autoload) if uri not in Artist.dicArtists else Artist.dicArtists[uri]
                for uri in [artist_raw['uri'] for artist_raw in self.artistsRaw]
            ]
        return self.artists

    def __repr__(self) -> str:
        return f'Track: {self.name}'

# %%
# get related to tedua


tedua_uri = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7'


tedua = Artist(tedua_uri, 3)
len(Artist.dicArtists)

#%%

marra_uri = 'spotify:artist:5AZuEF0feCXMkUCwQiQlW7'
marra = Artist(marra_uri, 4)


# %% possibile list of artists of all the album
n_vertices = len(tedua.getFeat()) +1
edges = []
for i, feat in enumerate(tedua.getFeat()):
    edges.append((0, i))
g = ig.Graph(n_vertices, edges)

g.vs['name'] = ['tedua']+ list(tedua.getFeat())

# %%
fig, ax = plt.subplots(figsize=(5,5))
ig.plot(
    g,
    target=ax,
    layout="circle", # print nodes in a circular layout
    vertex_size=0.1,
    vertex_frame_width=4.0,
    vertex_frame_color="white",
    vertex_label=g.vs["name"],
    vertex_label_size=7.0,

)



# %%
n_vertices = len(Artist.dicArtists)
edges = []
nodes =  Artist.dicArtists.copy()


#%%
for artist in nodes.values():
    for feat in nodes[artist.uri].getFeat():
        if feat in nodes:
            edges.append((artist.id, nodes[feat].id))

g = ig.Graph(n_vertices, edges)
g.vs['name'] = [ n.name for n in nodes.values()]

# %%

# %%
