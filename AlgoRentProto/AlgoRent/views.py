from django.shortcuts import render
import requests
from pyzillow.pyzillow import ZillowWrapper
# Create your views here.
zillow_data = ZillowWrapper("X1-ZWz1iofwv8d6a3_1sm5d") # Deprecated gg
def home(request):
    if(request.GET.get('home_search')):
        print("SEARCHING FOR A HOME!!")
        try:
            #print(zillow_data.get_deep_search_results('87-23 167th St, Jamaica', '11432', False))
            url = "http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=X1-ZWz1iofwv8d6a3_1sm5d&citystatezip=Seattle%2C+WA"
            page = requests.get(url)
            print(page)
        except Exception as err:
            print(err)
    return render(request, 'home.html', {})