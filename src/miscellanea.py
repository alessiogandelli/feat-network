def featuring_clean(artist_id):
    album_uri = []
    all_albums= clean_album_gae(artist_id)
    
    #uri delle vari album
    for album in all_albums:
        album_uri.append(album[1])
    
    #nome dell'artista
    artist_name = spotify.artist(artist_id)['name']
    
    dict_feat = {}
    
    for i in album_uri:
        results = spotify.album_tracks(i)
        for tracks in results['items']:
            for b in tracks['artists']:
                if(b['name'] != artist_name):
                    if b['name'] in dict_feat.keys():
                        dict_feat[b['name']] += 1
                    else:
                        dict_feat[b['name']] = 1
                        
    dict_feat = dict(sorted(dict_feat.items(), key=lambda item: item[1]))
    
    return dict_feat, artist_name

def clean_album_ale(albums):
    titles = []
    for album in albums['items']:
        titles.append(album['name'])#.translate(str.maketrans('', '', string.punctuation))

    titles.sort(key=lambda s: len(s)) # sort according to length

    toremove = []

    for title in titles:
        a = set(title.translate(str.maketrans('', '', string.punctuation)).split(' '))
        for title2 in titles:
            b = set(title2.translate(str.maketrans('', '', string.punctuation)).split(' '))

            if a.issubset(b) and a != b:
                print('rimuovo ', title2)
                toremove.append(title2)


    return list(set(titles)-set(toremove))