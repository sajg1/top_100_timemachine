import requests
from bs4 import BeautifulSoup
base_url = 'https://www.billboard.com/charts/hot-100'
selected_year = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"{base_url}/{selected_year}")

selected_top_100 = response.text

print(selected_top_100)