import json
from random import randint


def loadjson(artist, file):
    filename = f"data/{artist}/{file}.json"
    file = open(filename, encoding="utf8")
    data = json.load(file)
    return data

def number_of_songs(data):
    keys = []
    for key, value in data:
        keys.append(key)
    songs = len(keys)
    return songs

def songs_names(artist, file):
    data = loadjson(artist, file)
    songs = number_of_songs(data)
    songs_names = []
    for i in range(0, songs):
        song = data[i]['title']
        songs_names.append({f"{i+1}": f"{song}"})
    return songs_names

def randomlyric(artist, file, songs_amnt: int = None, track_number: int = None):
    try:
        data = loadjson(artist=artist, file=file)
        songs = number_of_songs(data)
        if songs_amnt != None and track_number == None:
            if songs_amnt > songs:
                songs = 30
            elif songs_amnt < 1:
                songs = 1
            else:
                songs = songs_amnt
        if songs_amnt != None and track_number != None:
            song = data[track_number-1]['title']
        else:
            songs = songs

        random_song = randint(0, songs-1)
        if track_number == None:
            random_song = random_song
        elif track_number != None:
            random_song = track_number - 1
        elif track_number < 1:
            random_song = 0
        elif track_number > songs:
            random_song = songs - 1
        elif track_number == "random":
            random_song = randint(0, songs-1)
        else:
            random_song = random_song

        lyrics = data[random_song]['lyrics']
        song = data[random_song]['title']
        line = randint(0, int(len(lyrics))-1)
        line = lyrics[line]
        random_lyric = {"Quote": f"{line}", "Song": f"{song}", "By": f"{artist}"}
    except Exception as e:
        print("Error occured in random_lyric function", e)
    return random_lyric
