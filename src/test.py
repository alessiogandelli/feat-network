
#%%
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


class Artist:
    dicArtists = {} # this 
    dicName = {}
    names = {}
    id_iter = itertools.count()


    def __init__(self, artist_uri, autoload=0):
       
        artist_raw = spotify.artist(artist_uri)
        print(self.name,'creating artist')

        self.id = next(Artist.id_iter)
        self.name = artist_raw['name']
        self.uri = artist_raw['uri']
        self.genres = artist_raw['genres']
        self.followers = artist_raw['followers']['total']
        self.popularity = artist_raw['popularity']
        self.tracks = []
        self.feat = {}
        self.audio_features = {'danceability': 0, 'energy': 0, 'tempo': 0}

        Artist.dicArtists[self.uri] = self
        Artist.names[self.uri] = self.name
        Artist.dicName[self.id] = self.name

        if autoload > 0:
            self.getTracks(autoload - 1)
            #self.get_audio_features()

    # fill the self.feat dictionary with the artists that have collaborated with this artist
    def getFeat(self):
       
        if len(self.feat) == 0:
            print(self.name, 'getting feat')
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
            print(self.name,'getting tracks')
            # get albums and  singles and merge 
            album_raw_album = spotify.artist_albums(self.uri, album_type= 'album', country='it', limit=50)
            album_raw_single = spotify.artist_albums(self.uri, album_type= 'single', country='it', limit=50)
            album_raw = album_raw_album['items'] + album_raw_single['items']


            albums_uri = [album['uri'] for album in album_raw]

           


            # print(self.name, 'found', str(len(albums_uri)), ' albums ')

            ## get tracks from albums because i need the date 
            tracks_uri = []
            tracks_names = set()
           
            for a in albums_uri:
                print(self.name, a)
                tracks =  spotify.album_tracks(a, limit=50, offset=0, market='it')['items']
                n_tracks = len(tracks)

                for i in range(n_tracks):
                    if tracks[i]['name'] not in tracks_names:
                        tracks_uri.append(tracks[i]['uri'])
                    tracks_names.add(tracks[i]['name'])

                        # create track objects


            # # get audio information about the tracks in batch of 50 tracks
            if len(tracks_uri) > 0:   
            #     pass
                a = 0
                b = 50
                c = 50
                tracks_raw = []
                audio_features = []

                while a!=b:
                    tracks_raw += spotify.tracks(tracks_uri[a:b])['tracks']
            #     audio_features += spotify.audio_features(tracks_uri[a:b])
                
                    b = len(tracks_uri) if b + c > len(tracks_uri) else b + c
                    a = a + c if a + c < len(tracks_uri) else len(tracks_uri)

            # add  audio features to tracks_raw
            # for i in range(len(tracks_raw)):
            #     tracks_raw[i]['audio_features'] = audio_features[i]

            # create track objects  
                self.tracks = [Track(t, autoload) if t['uri'] not in Track.dicTracks else Track.dicTracks[t['uri']] for t in tracks_raw]

                print( self.name, 'found ', str(len(self.tracks)), ' tracks ')
        return self.tracks

    def reset():
        Artist.dicArtists = {}
        Artist.dicName = {}
        Artist.names = {}
        Artist.id_iter = itertools.count()

    def get_audio_features(self):
        audio_features = {}
        danceability = 0
        energy = 0
        tempo = 0
        for track in self.getTracks(-1):
            danceability += track.audio_features['danceability']
            energy += track.audio_features['energy']
            tempo += track.audio_features['tempo']
        
        audio_features['danceability'] = danceability / len(self.getTracks(-1))
        audio_features['energy'] = energy / len(self.getTracks(-1))
        audio_features['tempo'] = tempo / len(self.getTracks(-1))
        self.audio_features = audio_features


    def __repr__(self) -> str:
        return f'Artist: {self.name}'
    
    def __str__(self) -> str:
        return self.name 

class Track:
    dicTracks = {}
    track_name = {}

    def __init__(self, track_raw, autoload=0):
        self.name = track_raw['name']
        self.uri = track_raw['uri']
        # self.album = track_raw['album']['name']
        self.duration = track_raw['duration_ms']
        self.artistsRaw = track_raw['artists']
#        self.popularity = track_raw['popularity']
        self.release_date = track_raw['album']['release_date']
        self.artists = None
       # self.audio_features = track_raw['audio_features']
        Track.dicTracks[self.uri] = self
        Track.track_name[self.uri] = self.name




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
        return self.name

    def reset():
        Track.dicTracks = {}

# %%
Artist.reset()
Track.reset()
uri_tedua = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7'
tedua = Artist("spotify:artist:0gm1lHoOXAdy5OB4AwFYRr", 3)
# %%


# create a dataframe  with audio feature  and the name as index  of all tracks of the artist
df = pd.DataFrame([t.audio_features for t in tedua.getTracks()]).set_index('uri')
df['name'] = [Track.track_name[uri] for uri in df.index]
df.set_index('name', inplace=True)





# %%
Artist.reset()
Track.reset()
artista = Artist(uri_tedua, 2)
print('found ', str(len(Artist.dicArtists)))
# %%

g = ig.Graph()
nodes = Artist.dicArtists
for artist in nodes.values():
    g.add_vertex(artist.name,   popularity = artist.popularity, 
                                genres = artist.genres, 
                                followers = artist.followers
                                )

for artist in nodes.values():
    print(artist.name, 'ore prendiamo i suoi feat ')
    for feat in artist.getFeat().items():
        if feat[0] in nodes:
            print(artist.name, 'feat', nodes[feat[0]].name, feat[1])
            # add edge between artist and featured artist
            g.add_edge(artist.name, nodes[feat[0]].name, weight=feat[1])



g.vs['degree'] = g.degree()
                
# %%
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
    #edge_width = [a for a in g.es['weight']],
    #vertex_color = ['green' if 'italian hip hop' in gen else 'grey' for gen in g.vs['genres']],
    vertex_color = ['#425df5' if artist > 3 else 'grey' for artist in g.vs['degree']]
)
# %%
