from audioop import add
from django.shortcuts import render
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from AlgoRent.scraper import house_info_from_address as hs
# Create your views here.

async def home(request):
    info = []
    if(request.GET.get('home_search')):
        print("SEARCHING FOR A HOME!!")
        try:
            base_string = request.GET.get('home_search')
            print("Request is: ", base_string)
            state_pos = int(base_string.find(","))
            city_pos = int((base_string[state_pos+1:]).find(",") + state_pos + 1)
            zip_pos = int(city_pos + 1)
            #print("State: ", state_pos, " City: ", city_pos, " Zip: ", zip_pos)
            state = base_string[0:state_pos].replace(",","")
            city = base_string[state_pos+1:zip_pos].replace(",","")
            zip = base_string[zip_pos:].replace(",","").replace(" ","")
            address = {"country":"US", "state":state, "city":city, "zip":zip}
            print("Address: ", address)
            info = hs(address)
            #print(info)
        except Exception as err:
            print(err)
    return render(request, 'home.html', context={"house_info": info})