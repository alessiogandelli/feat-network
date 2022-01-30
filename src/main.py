#%%

import os
from re import A
from dotenv import load_dotenv
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

id = os.getenv('CLIENT_ID')
secret = os.getenv('CLIENT_SECRET')

#%%
tedua = 'spotify:artist:1AgAVqo74e2q4FVvg0xpT7'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(id,secret))

get_uri = {} 
feat = {} # brutto che sia globale cosi 

#given an artist  retrurs a dictionary with all feats of an artists example: feat['marra'] = [gue, blanco, sfera]
def get_feat(artist_uri):
    artist_name = spotify.artist(artist_uri)['name']
    all_albums = spotify.artist_albums(artist_uri, album_type='album')

    for album in all_albums['items']:
        tracks = spotify.album_tracks(album['uri'])
        for track in tracks['items']:
            for artist in track['artists']:
                
                if(artist['name'] != artist_name):
                    feat.setdefault(artist_name, []).append(artist['name'])  # 

                if artist['name'] not in get_uri.keys():
                    get_uri[artist['name']] = artist['uri']

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
    
    return artists

# #init get_uri
# get_feat(tedua)

# # first giro 
# get_uri2 = get_uri.copy()
# for rapper in get_uri2.values():
#     get_feat(rapper)

# # second giro ci mette un botto è c'è un sacco di gente che non cin interessa 
# get_uri2 = get_uri.copy()
# for rapper in get_uri2.values():
#     get_feat(rapper)
# %%




# %%

artists = get_related_artists(tedua)
get_feat(tedua)

for artist in artists.values():
    get_feat(artist)
# %%
