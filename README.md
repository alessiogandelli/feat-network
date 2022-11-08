# feat_network
create a network with Spotify artists as nodes and featuring as tie

There are 2 classes: Artist and Track 

you can start creating a set of Artist and Track from a single URI from a single artist 

Given an artist let's say tedua and a depth you can build different graphs 

Artist(tedua, 0) creates just Artist tedua 
Artist(tedua, 1) creates artist tedua and all his tracks 

Artist(tedua, 2) creates artist tedua and all his tracks + all artists he made a song with 
Artist(tedua, 3) creates artist tedua and all his tracks + all artists he made a song with + their tracks 

Basically in Artist(tedua, n)  you can get n/2 level away from tedua, if n is even you do not get the tracks of the last layer



