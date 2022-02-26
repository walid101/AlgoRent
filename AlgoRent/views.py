from audioop import add
from random import randrange
from django.shortcuts import render
import sys
import os

from numpy import half
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from AlgoRent.scraper import house_info_from_address as hs
# Create your views here.
#sqlite -> ok, #mongo
#sql -> join tables and search
#SELECT DISTINCT FROM WHERE
async def home(request):
    info = []
    half = 5
    if(request.GET.get('home_search')):
        #print("SEARCHING FOR A HOME!!")
        try:
            base_string = request.GET.get('home_search')
            #print("Request is: ", base_string)
            info = hs(base_string)
            #print(info)
        except Exception as err:
            print(err)
    else:
        try:
            base_string = "NY, Buffalo, 14212"
            #print("Request is: ", base_string)
            info = hs(base_string) 
            #print(info)
        except Exception as err:
            #error supression
            print(err)
    for info_s in info:
        info_s["price"] = randrange(85000, 800000)
    return render(request, 'home.html', context={"house_info_a": info[0:half], "house_info_b": info[half:2*half],
                                                 "house_info_c": info[2*half:]})