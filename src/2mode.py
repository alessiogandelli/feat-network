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

g.vs['danceability'] = [song.audio_features['danceability'] for song in incidence_matrix.index] + [artist.audio_features['danceability'] for artist in incidence_matrix.columns]
g.vs['energy'] = [song.audio_features['energy'] for song in incidence_matrix.index] + [artist.audio_features['energy'] for artist in incidence_matrix.columns]
g.vs['tempo'] = [song.audio_features['tempo'] for song in incidence_matrix.index] + [artist.audio_features['tempo'] for artist in incidence_matrix.columns]
g.vs['release_date'] = [song.release_date for song in incidence_matrix.index] 

# print release date attriburte



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
g.write_gml('marra.gml')
