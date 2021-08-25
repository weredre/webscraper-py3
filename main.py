import requests
from bs4 import BeautifulSoup


URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

print(page.text)
