import requests
from bs4 import BeautifulSoup
import re

import json

# Replace 'your_url_here' with the actual URL of the HTML page you want to scrape
url = 'your_url_here'

with open("./colorcine.html", encoding="utf8") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

# Find all image elements and their corresponding titles
# This assumes images are in <img> tags and titles are in a specific tag like <h2>
# You may need to adjust selectors based on the actual HTML structure
images = soup.find_all('img')
names = soup.find_all("span", class_='name')

images = [tag["src"] for tag in images]
names = [re.sub("\n","",re.sub(" +", " ", tag.text)) for tag in names]

mapping = {}

for i in range(len(images)):
    mapping[names[i]] = images[i]

with open("map.json", "w") as fp:
    json.dump(mapping, fp)