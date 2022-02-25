from django.shortcuts import render
import scrapers.scraper as sc
# Create your views here.

def home(request):
    if(request.GET.get('home_search')):
        print("SEARCHING FOR A HOME!!")
        try:
            base_string = request.GET.get('home_search')
            print("Request is: ", base_string)
        except Exception as err:
            print(err)
    return render(request, 'home.html', {})