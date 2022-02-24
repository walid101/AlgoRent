import requests
from bs4 import BeautifulSoup as bs

def scrape_zillow(url):
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    print(str(soup.prettify()))

scrape_zillow("https://www.remax.com/homes-for-sale/ny/new-york/city/3651000")