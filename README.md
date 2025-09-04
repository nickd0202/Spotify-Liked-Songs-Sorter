# Spotify Liked Songs Sorter

If you are anything like me then you have all your songs in one place and it can be annoying 
to find a specific genre. Whether its a late night drive or a house party.
This script turns your **Liked Songs** into different genre oriented playlists. You can choose to add or subtract 
genre based off of your preference.

## Start

1) **Spotify app keys**  
   - Go to https://developer.spotify.com/dashboard  
   - **Create an app** → open it → **Edit Settings**  
   - Add Redirect URI:  
    
     http://127.0.0.1:8888/callback
     
   - Copy your **Client ID** and **Client Secret** and fill it in the script.

2) ## Running the script
   ```bash
   python liked_songs.py
