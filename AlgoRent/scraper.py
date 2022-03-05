from audioop import add
import re
import time
from webbrowser import get
import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as bs
import sys

def scrape_remax(url):
	base_url = "https://www.remax.com"
	page = requests.get(url)
	soup = bs(page.content, "html.parser")
	href_stats = []
	for a in soup.find_all('a', href=True):
		if("home-details" in a['href']):
			href_stats.append(base_url+a['href'])
	return href_stats[0:15] #Give a portion first -> gives independed sites

def scrape_remax_fast(url):
	base_url = "https://www.remax.com"
	page = requests.get(url)
	soup = bs(page.content, "lxml")
	href_stats = []
	for a in soup.find_all('a', href=True):
		if("home-details" in a['href']):
			href_stats.append(base_url+a['href'])
	return href_stats[0:15] #Give a portion first -> gives independed sites


def process_remax_page(url):
	page = requests.get(url)
	soup = bs(page.content, "html.parser")
	soup_string = str(soup)
	info_list = {}
	image = []
	title = str(soup.find("title"))
	address = title[7:title.find(" |")]
	#price_start = soup_string.find("")
	#print(address)
	#soup_string = str(soup)
	for img in soup.find_all("img"):
		str_img = str(img)
		#print("Images: ", img)
		if("aws." in str(img) or "cloud" in str(img)):
			img_split = str_img.split(" ") #Need this?
			img_stripped = str(list(filter(lambda k: 'data-src' in k, img_split)))#Needs this?
			img_url = img_stripped[img_stripped.find("http"):len(img_stripped)-3]
			if(len(img_url) > 10):
				image.append(img_url)#We only need the first
				break
	info_list["image"] = image
	info_list["address"] =  address
	return info_list


def process_remax_page(url):
	page = requests.get(url)
	soup = bs(page.content, "html.parser")
	soup_string = str(soup)
	info_list = {}
	image = []
	title = str(soup.find("title"))
	address = title[7:title.find(" |")]
	#price_start = soup_string.find("")
	#print(address)
	#soup_string = str(soup)
	for img in soup.find_all("img"):
		str_img = str(img)
		#print("Images: ", img)
		if("aws." in str(img) or "cloud" in str(img)):
			img_split = str_img.split(" ") #Need this?
			img_stripped = str(list(filter(lambda k: 'data-src' in k, img_split)))#Needs this?
			img_url = img_stripped[img_stripped.find("http"):len(img_stripped)-3]
			if(len(img_url) > 10):
				image.append(img_url)#We only need the first
				break
	info_list["image"] = image
	info_list["address"] =  address
	return info_list

def process_remax_page_fast(url):
	page = requests.get(url)
	soup = bs(page.content, "lxml")
	soup_string = str(soup)
	info_list = {}
	image = []
	title = str(soup.find("title"))
	address = title[7:title.find(" |")]
	#price_start = soup_string.find("")
	#print(address)
	#soup_string = str(soup)
	for img in soup.find_all("img"):
		str_img = str(img)
		#print("Images: ", img)
		if("aws." in str(img) or "cloud" in str(img)):
			img_split = str_img.split(" ") #Need this?
			img_stripped = str(list(filter(lambda k: 'data-src' in k, img_split)))#Needs this?
			img_url = img_stripped[img_stripped.find("http"):len(img_stripped)-3]
			if(len(img_url) > 10):
				image.append(img_url)#We only need the first
				break
	info_list["image"] = image
	info_list["address"] =  address
	return info_list

def get_coords(address):
	#address = "32-22 204TH ST BAYSIDE, NY 11361"
	address.replace(" ", "+")
	geolocator = Nominatim(user_agent="html")
	location = geolocator.geocode("175 5th Avenue NYC")
	resp_json_payload = (location.latitude, location.longitude)
	return resp_json_payload

def get_complete_addr_link(address): #format of address : "country" "state" "city"  "zip": }
	try:
		geolocator = Nominatim(user_agent="html")
		possible_addr = address
		state = address["state"]
		city = address["city"]
		zip = address["zip"]
		possible_addr = city + " " + state  + " " + zip
		#print("ADDRESS IS: ", possible_addr)
		location = geolocator.geocode(possible_addr, addressdetails=True, language="en", timeout=9000)
		#final_location = location.raw["address"]
		#print("The Complete Address is: ", location.raw['address'])
		return location.raw['address']
	except Exception as err:
		print("Error Encountered: ", err)
		return None #Means Address is invalid

def house_info_from_address(address): #Initial: "Country, State, City, Zip" format of address : {"country": ,"state": , "city": , "zip": }
	if(isinstance(address,str)):
		#convert to dict
		stripped_address = address.replace(",","").replace("  ", " ").split(" ") #properly format string
		if(len(stripped_address) < 3):
			for i in range(3-len(stripped_address)):
				stripped_address.append("")
		dict_address = {"zip":stripped_address[-1], "city":stripped_address[-2], "state":stripped_address[-3]}
		dict_address["country"] = "US"
		address = dict_address
		#ReCheck this later (recheck)
	
	comp_address = get_complete_addr_link(address) if "state" not in address or "city" not in address or "zip" not in address else address
	state = comp_address["state"].replace(" ", "+") if "state" in comp_address else address["state"]
	city = comp_address["city"].replace(" ", "+") if "city" in comp_address else address["city"]
	#zip = comp_address["postcode"].replace(" ", "+")
	zip = address["zip"] if address["zip"] != None and len(address["zip"]) == 5 else comp_address["postcode"].replace(" ", "+")
	BASE_URL = "https://www.remax.com"
	EXTENDED_URL = "/homes-for-sale/"+state+"/"+city+"/zip/"+zip
	SEARCH_URL = BASE_URL+EXTENDED_URL
	#print("Search Link: ", SEARCH_URL)
	display_page_links = scrape_remax_fast(SEARCH_URL)
	#print("Links Obtained: ", display_page_links)
	house_info = []
	for link in display_page_links:
		house_info.append(process_remax_page_fast(link))
	#print("Images Gathered: ", house_info)
	return house_info



'''
address = {"country": "US", "state": "", "city" : "", "zip":"11432"}
img_urls_from_address(address)
args = sys.argv[1:]
if(len(args) > 0):
	#get_complete_addr_link(address)
	#pages = scrape_remax("https://www.remax.com/homes-for-sale/ny/queens/zip/11432")
	#print(pages)
	#process_remax_page("https://www.remax.com/ny/jamaica/home-details/84-50-169th-st-102-jamaica-ny-11432/9637000322339336887/M00000489/3378032")
				 #"BASE URL = https://www.remax.com"
				 #"BASE_URL + /homes-for-sale/<state>/<city>/zip/<zipcode>"
				 #data-src filter
'''
#process_remax_page("https://www.remax.com/ny/jamaica/home-details/84-50-169th-st-102-jamaica-ny-11432/9637000322339336887/M00000489/3378032")
'''
start = time.time()
scrape_remax("https://www.remax.com/ny/jamaica/home-details/84-50-169th-st-102-jamaica-ny-11432/9637000322339336887/M00000489/3378032")
end = time.time()
print("Time Taken Normal Parser: ", (end - start) * 1000)

start = time.time()
scrape_remax_fast("https://www.remax.com/ny/jamaica/home-details/84-50-169th-st-102-jamaica-ny-11432/9637000322339336887/M00000489/3378032")
end = time.time()
print("Time Taken FAST Parser: ", (end - start) * 1000)
'''
#Value: KEY WORD: value:"$
#Address: <title> tag -> |

#house_info_from_address("US, NY, Buffalo, 14212")
#address = {"country": "US", "state": "New York", "city" : "Jamaica", "zip":"11432"}
#get_complete_addr_link(address)