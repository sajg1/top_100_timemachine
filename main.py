import requests
from bs4 import BeautifulSoup
import os
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth

BASE_URL = 'https://www.billboard.com/charts/hot-100'
CLIENT_ID = os.environ.get('CLIENT_ID_TOP100')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET_TOP100')

# Authorisation for Spotify
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://example.com",
    cache_path='token.txt',
    show_dialog=True,
    scope="playlist-modify-private"
)

sp = spotipy.Spotify(auth_manager=auth_manager)

user_id = sp.current_user()['id']

# Get response from user and scrape relevant top 100 song names from Billboard.com

selected_year = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"{BASE_URL}/{selected_year}")

selected_top_100 = response.text

soup = BeautifulSoup(selected_top_100, 'html.parser')

song_names_span = soup.find_all(name="span", class_="chart-element__information__song")

song_names = [song.getText() for song in song_names_span]

# Get each songs track uri from the spotify API
year = selected_year.split("-")[0]
track_uri_list = []
for song in song_names:
    result = sp.search(q=f"track: {song} year:{year}", type="track")
    try:
        track_uri = result['tracks']['items'][0]['uri']
        track_uri_list.append(track_uri)
    except IndexError:
        print("Not on spotify")

# create playlist
sp.user_playlist_create(user=user_id, name=f"{selected_year} Billboard 100", public=False, collaborative=False, description="")

