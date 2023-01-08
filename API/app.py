import json
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from random import randint

app = FastAPI()
    

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



@app.get("/")
async def root():
    return {"message": "Welcome to the Lyrics API. Please see the documentation for the correct usage of this API."}

@app.get("/api/v1/lmorphine")
async def get_random_quote(lyric: str = Query(None, regex="random"), popularity: int = Query(None, ge=1, le=30), songs: str = Query(None, regex="all|random"), track: int = Query(None, ge=1, le=30)):

    try:
        if lyric == "random" and popularity == None and track == None:
            return randomlyric(artist="lmorphine", file="TOP30")

        elif lyric == "random" and popularity != None:
            print(popularity)
            return randomlyric(artist="lmorphine", file="TOP30", songs_amnt=popularity)

        elif lyric == "random" and popularity == None and track != None:
            return randomlyric(artist="lmorphine", file="TOP30", track_number=track)

        elif lyric == "random" and popularity != None and track != None:
            return randomlyric(artist="lmorphine", file="TOP30", track_number=track)

        elif lyric == None and popularity == None and track == None:
            if songs == "all":
                return songs_names(artist="lmorphine", file="TOP30")
            elif songs == "random":
                songsnames = songs_names(artist="lmorphine", file="TOP30")
                return songsnames[randint(0, len(songsnames)-1)]
            else:
                return {"message": "Please use the correct query parameters. See the documentation for more information."}

        else:
            return {"message": "Please use the correct query parameters. See the documentation for more information."}
    except Exception as e:
        print("Error occured in get_random_quote function", e)
        return {"message": "Please use the correct query parameters. See the documentation for more information."}



@app.exception_handler(404)
async def page_not_found(request, exc):

    return JSONResponse(
        status_code=404,
        content={"message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)