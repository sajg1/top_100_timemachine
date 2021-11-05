import requests
from bs4 import BeautifulSoup
import os
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth

BASE_URL = 'https://www.officialcharts.com/charts/singles-chart/'
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
url_year = "".join(selected_year.split('-'))

response = requests.get(f"{BASE_URL}/{url_year}")

selected_top_100 = response.text

soup = BeautifulSoup(selected_top_100, 'html.parser')

song_names_div = soup.find_all(name="div", class_="title")

song_names = [song.getText().strip('\n') for song in song_names_div]

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
print(len(track_uri_list))
# create playlist
new_playlist = sp.user_playlist_create(user=user_id, name=f"{selected_year} Official Singles Charts", public=False, collaborative=False, description="")
new_playlist_id = new_playlist['id']
print(new_playlist_id)

# add songs to playlist

sp.playlist_add_items(playlist_id=new_playlist_id, items=track_uri_list, position=None)