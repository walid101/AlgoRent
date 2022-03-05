from audioop import add
import re
from webbrowser import get
import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as bs
import sys

def scrape_remax(url):
    proxy_s = "47.117.88.37:22"
    proxy = {"http": proxy_s, "https": proxy_s}
    page = requests.get(url, proxies=proxy, timeout=50000)
    soup = bs(page.content, "html.parser")
    print(soup.prettify())
    return None #Give a portion first -> gives independed sites
