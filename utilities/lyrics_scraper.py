import os
try:
    import lyricsgenius
    import json
except ImportError:
    print("Please install the required packages.")
    os.system("pip install -r requirements.txt")
try:
    from authentication import genius_token
    if genius_token == "YOUR_TOKEN_HERE":
        raise ValueError

except Exception:
    print("Please add your Genius API token to the authentication.py file.")
    exit()

path = os.path.dirname(os.path.abspath(__file__)).replace("utilities", "data/")


def artist_f(artist_name, max_songs, sort="popularity", include_features=True, token=genius_token):
    genius = lyricsgenius.Genius(token)
    artist = genius.search_artist(
        artist_name, 
        max_songs=max_songs, 
        sort=sort, 
        include_features=include_features)
    return artist

def list_song_names(artist, max_songs):
    artist = artist_f(artist, max_songs)
    songs_list = [song.title for song in artist.songs]
    return songs_list



def lyrics_to_json(artist, max_songs: int, songs_list: list = None):
    if songs_list != None:
        max_songs = 0

    artist = artist_f(artist, max_songs)
    name = artist.name
    for char in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
        name = name.replace(char, "")
        name = name.replace(" ", "")
        artistname = name.lower()

    if songs_list == None:
        songs_list = [song.title for song in artist.songs]
    else:
        songs_list = songs_list
    json_song_lyrics = []
    for song in songs_list:
        song_title = song
        song_lyrics = artist.song(song)
        # Filter
        unique_lines = set(song_lyrics.lyrics.splitlines())
        unique_lines = [line for line in unique_lines if line]
        unique_lines = list(unique_lines)
        unique_lines = [line for line in unique_lines if len(line.split()) > 1]
        unique_lines = [line for line in unique_lines if not line.startswith("[")]
        unique_lines = [line for line in unique_lines if not line.startswith("Translations")]
        unique_lines = [line.replace("You might also like94Embed", "") for line in unique_lines]
        
        json_song_lyrics.append({"title": song_title, "lyrics": unique_lines})

    os.makedirs(path + artistname, exist_ok=True)
    with open(f"{path}{artistname}/data.json", "w", encoding="utf-8") as f:
        json.dump(json_song_lyrics, f, ensure_ascii=False, indent=4)

# lyrics_to_json("dollypran", 1, ['Yeah Ho!', 'Chiico', 'Khari', 'A.C.N.D', 'Taach', 'Napoli', 'Trax', 'Noir O Cloppe', 'Foufou', '20B13', 'Breakdance', 'Drill Hood', 'Trump', 'Yeah Ho V2', 'Cash', 'Power Rangers', 'Alfrido', 'SiSi'])
