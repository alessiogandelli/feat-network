# %%
import os
import string
import spotipy
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import json

load_dotenv()

# Login to the spotify API
cid = os.environ.get("CLIENT_ID")
secret = os.environ.get("CLIENT_SECRET")

spotify = spotipy.Spotify( client_credentials_manager=SpotifyClientCredentials(cid, secret))


# %%
class Artist:
    dicArtists = {}

    def __init__(self, artist_uri, autoload=0):
        artist_raw = spotify.artist(artist_uri)
        print('creating artist', artist_raw['name'])

        self.name = artist_raw['name']
        self.uri = artist_raw['uri']
        self.genres = artist_raw['genres']
        self.followers = artist_raw['followers']['total']
        self.popularity = artist_raw['popularity']
        self.tracks = None
        self.feat = {}
        Artist.dicArtists[self.uri] = self

        if autoload > 0:
            self.getTracks(autoload - 1)

    def getFeat(self):

        if len(self.feat) == 0:
            for track in self.getTracks():
                for artist in track.getArtists():
                    if artist.uri != self.uri:
                        if artist.uri in self.feat:
                            self.feat[artist.uri] += 1
                        else:
                            self.feat[artist.uri] = 1
        return self.feat

    def getTracks(self, autoload=0):
        if self.tracks is None:

            raw_tracks1 = spotify.search( self.name, limit=50, type='track', market='it', offset=0)['tracks']['items']
            raw_tracks2 = spotify.search( self.name, limit=50, type='track', market='it', offset=50)['tracks']['items']
            raw_tracks = raw_tracks1 + raw_tracks2

            print(len(raw_tracks), 'tracks found')
            self.tracks = []


            self.tracks = [Track(t, autoload) if t['uri'] not in Track.dicTracks else Track.dicTracks[t['uri']] for t in raw_tracks]
        return self.tracks

    def __repr__(self) -> str:
        return f'Artist: {self.name}'


class Track:
    dicTracks = {}

    def __init__(self, track_raw, autoload=0):
        print('creating track', track_raw['name'])
        self.name = track_raw['name']
        self.uri = track_raw['uri']
        self.album = track_raw['album']['name']
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


# %% possibile list of artists of all the album

