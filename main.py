import requests
from bs4 import BeautifulSoup
base_url = 'https://www.billboard.com/charts/hot-100'
selected_year = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"{base_url}/{selected_year}")

selected_top_100 = response.text

soup = BeautifulSoup(selected_top_100, 'html.parser')

song_names_span = soup.find_all(name="span", class_="chart-element__information__song")


song_names = [song.getText() for song in song_names_span]
print(song_names)

