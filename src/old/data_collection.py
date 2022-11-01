# %%

import os
import string
import spotipy
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials 
import json

load_dotenv()
#%% methods and classes 


def get_related_artists(artist):
    rel = spotify.artist_related_artists(artist) # get related artists
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
    
    artists['Tedua'] = artist
    return artists

def get_feat(artist_uri,df):
    artist_name = spotify.artist(artist_uri)['name']

    for album in albums(artist_uri).names():
        tracks = spotify.album_tracks(str(album[1]))

        for track in tracks['items']:
            for ft in track['artists']:
                if ft['name'] in artists.keys():
                    df.at[ft['name'], artist_name] += 1 

def get_artists_data(artists_uri_list):
    artists = []
    for artist_uri in artists_uri_list.values():
        artist = spotify.artist(artist_uri)
        artist.pop('images')
        artists.append(artist)
    
    return artists

def get_all_data_together(artists_data, feat):
    project = {}
    project['description'] = 'Data about artists and their features'
    project['attributes'] = {}
    project['attributes']['Name'] = [x['name'] for x in artists_data ]
    project['attributes']['popularity'] = [x['popularity'] for x in artists_data ]
    project['attributes']['genre1'] = [x['genres'][0] if len(x['genres']) > 0 else [''] for x in artists_data ]
    project['attributes']['genre2'] = [x['genres'][1] if len(x['genres']) > 1 else [''] for x in artists_data ]
    project['attributes']['genre3'] = [x['genres'][2] if len(x['genres']) > 2 else [''] for x in artists_data ]
    project['attributes']['followers'] = [x['followers']['total'] for x in artists_data ]
    project['feat'] = feat.to_numpy().tolist()

    return project
    
class albums:
    def __init__(self, uri_artist):

        self.artist = spotify.artist(uri_artist)['name']
        self.uri_artist = uri_artist
        self._number = None
        self._names = None
        
    def names(self):

        if self._names is None:

            all_albums = spotify.artist_albums(self.uri_artist, album_type='album')
            
            #URIs di tutti gli albums collegati all'artista
            
            album_names = list([album['name'], album['uri']] for album in all_albums['items'])

            #Pulizie dei nomi all'interno degli album

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

            self._names = titles
            self._number = len(titles)

            return self._names 


#%%
#Login to the spotify API
cid = os.environ.get("CLIENT_ID")
secret = os.environ.get("CLIENT_SECRET")

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(cid,secret))

#%%
# get related to tedua
tedua = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7'
artists = get_related_artists(tedua)

artists_data = get_artists_data(artists)#json data aout artists



# %% csv data about featurings 
                      
df = pd.DataFrame(0, columns = artists.keys(), index = artists.keys() )

for artist in artists.values():
     get_feat(artist,df)

# %%
#Export of the dataframe
df.to_csv('data/feat_tedua.csv')

with open("data/artists.json", "w") as outfile:
    json.dump(artists_data, outfile)


#%%
feat_network = get_all_data_together(artists_data, df)
with open("data/feat_network.json", "w") as outfile:
    json.dump(feat_network, outfile)


# %% NON UTILIZZATA


sixseven = 'spotify:artist:211p9eSLzwF6iuXzzP5xTl'
artists = get_related_artists(sixseven)
artists_data = get_artists_data(artists)
# %%
df = pd.DataFrame(0, columns = artists.keys(), index = artists.keys() )

for artist in artists.values():
     get_feat(artist,df)
# %%
df.to_csv('./../data/feat_sixseven.csv')
# %%
