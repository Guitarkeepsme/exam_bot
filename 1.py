from bs4 import BeautifulSoup
import requests

url = "https://rus-ege.sdamgia.ru/test?theme=289"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")

links = soup.find_all('span', {"class": "prob_nums"})
print(links)