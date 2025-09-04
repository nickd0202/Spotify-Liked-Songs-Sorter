import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
import time

# Replace with your credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = ''

# This is where you can add different genres and keywords to look for the genre
GENRE_GROUPS = {
    "Hip-Hop Mix": ["hip hop", "rap", "trap", "boom bap", "drill", "alternative hip hop", "alternative rap", 
                    "trap", "r&b", "pop rap", "trap soul", "southern hip hop", "political hip hop", "conscious hip hop", 
                    "hardcore hip hop", "rage rap"],
    "Pop Mix": ["pop", "dance pop", "electropop", "indie pop", "teen pop", "k-pop", "k pop", "pop rock"],
    "Rock Mix": ["rock", "alternative rock", "hard rock", "indie rock", "punk", "grunge", "irish rock"],
    "R&B Mix": ["r&b", "neo soul", "soul", "funk", "contemporary r&b"],
    "Electronic Mix": ["edm", "house", "techno", "electronic", "trance", "dubstep", "electro house"],
    "Hardstyle Mix": ["hardstyle", "hard trance", "hardcore techno"],
    "Orchestra Mix": ["orchestra", "symphonic", "classical orchestra", "piano", "solo piano", "piano cover", "soundtrack"],
    "Acoustic Mix": ["acoustic", "acoustic pop", "acoustic rock", "singer-songwriter"],
    "Jazz & Blues Mix": ["jazz", "blues", "swing", "bebop", "soul jazz"],
    "Country Mix": ["country", "alt-country", "country pop", "modern country rock"],
    "Reggae Mix": ["reggae", "dancehall", "roots reggae", "ska", "latin", "reggaeton", "latin pop", "salsa", "bachata", "cumbia"],
    "Metal Mix": ["metal", "heavy metal", "death metal", "black metal", "nu metal"],
    "Indie/Alt Mix": ["indie", "indie rock", "indie pop", "alternative", "lo-fi"],
    "Anime/Game Mix": ["anime", "j-pop", "j rock", "video game music", "vocaloid"]
}


auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read playlist-modify-public",
    show_dialog=True
)

auth_url = auth_manager.get_authorize_url()
print(f"🔗 Open this link in your browser:\n{auth_url}")
response_url = input("\n📋 After logging in, paste the full redirected URL here:\n")

code = auth_manager.parse_response_code(response_url)
token_info = auth_manager.get_access_token(code, as_dict=False)
sp = spotipy.Spotify(auth=token_info)


def get_liked_songs():
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)
    total = results['total']
    print(f"🎵 Found {total} liked songs...")
    count = 0

    while results:
        for item in results['items']:
            track = item['track']
            liked_songs.append(track)
            count += 1
            print(f"✅ Loaded {count}/{total} tracks", end='\r')
        results = sp.next(results) if results['next'] else None

    print(f"\n✅ Done loading liked songs.")
    return liked_songs


def get_genre(track, genre_cache):
    artist_id = track['artists'][0]['id']
    if artist_id in genre_cache:
        return genre_cache[artist_id]

    try:
        artist = sp.artist(artist_id)
        genres = artist.get('genres', [])
        genre_cache[artist_id] = genres
        time.sleep(0.2)  
        return genres
    except:
        return []

def match_genre_to_group(genres):
    for genre in genres:
        genre = genre.lower()
        for playlist, keywords in GENRE_GROUPS.items():
            for keyword in keywords:
                if keyword.lower() in genre:
                    return playlist
    return None


def create_playlists_by_grouped_genres(songs):
    playlist_map = defaultdict(list)
    unmatched_uris = []
    genre_cache = {}

    print(f"🔍 Grouping songs by genre category...")
    for i, song in enumerate(songs, 1):
        genres = get_genre(song, genre_cache)
        group = match_genre_to_group(genres)
        if group:
            playlist_map[group].append(song['uri'])
            print(f"🎶 {i}/{len(songs)} → {group}", end='\r')
        else:
            unmatched_uris.append(song['uri'])
            print(f"❌ {i}/{len(songs)} → Unsorted", end='\r')

    print(f"\n📂 Creating playlists...")
    user_id = sp.me()['id']

    for group, uris in playlist_map.items():
        print(f"📝 {group} → {len(uris)} songs")
        playlist = sp.user_playlist_create(user=user_id, name=group)
        for i in range(0, len(uris), 100):
            sp.playlist_add_items(playlist['id'], uris[i:i+100])

    if unmatched_uris:
        print(f"🗂 Creating Unsorted Mix → {len(unmatched_uris)} songs")
        playlist = sp.user_playlist_create(user=user_id, name="Unsorted Mix")
        for i in range(0, len(unmatched_uris), 100):
            sp.playlist_add_items(playlist['id'], unmatched_uris[i:i+100])

    print("✅ The playlists have been created!!")


liked_songs = get_liked_songs()
create_playlists_by_grouped_genres(liked_songs)
