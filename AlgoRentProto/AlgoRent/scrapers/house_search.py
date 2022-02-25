import sys
from django import urls
import pandas as pd
import io
from redfin import Redfin
from redfin_houses import redfin 
from redfin_houses.house_filter import HouseFilter, PropertyTypeEnum, PriceEnum, SqftEnum, BathEnum, LotEnum
from redfin_houses.redfin import query_house_list
from geopy.geocoders import Nominatim
import scraper as sc
from linkpreview import link_preview

pd.options.display.max_columns = None
pd.options.display.max_rows = None
def convert_csv_to_dataframe(csv):
    f = io.StringIO(csv)
    df = pd.read_csv(f)
    return df

def preview_link(url):
    preview = link_preview(url, parser="lxml")
    print("title:", preview.title)
    print("description:", preview.description)
    print("image:", preview.image)
    print("force_title:", preview.force_title)
    print("absolute_image:", preview.absolute_image)

def get_property_by_zip_code(zipcode, filter):
    response = query_house_list("zipcode/{}".format(zipcode), filter)
    return response


def get_property_by_area(area, filter):
    print("Searching Area: ", area)
    geolocator = Nominatim(user_agent="http")
    location = geolocator.geocode(area)
    raw_data = location.raw['display_name'].split(" ")
    zips = {}
    for data in raw_data:
        data = data.replace(",","")
        if(str.isdecimal(data)):
            zips[data] = 1
    #print(zips)
    response = {}
    for zip in zips:
        try:
            houses_csv = get_property_by_zip_code(zip, filter)
            df = convert_csv_to_dataframe(houses_csv)
            df.rename(columns={'URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)': 'URL'})
            response[zip] = df
        except Exception as err:
            print('Error: ', err)
            pass
    return response

house_filter = HouseFilter(
        property_type_list=[PropertyTypeEnum.HOUSE],
        max_price=PriceEnum.PRICE_800k
        
    )

'''
area = "Queens, New York"
houses_by_area = get_property_by_area(area, house_filter)
address_url_pair = []
for index in houses_by_area:
    df = houses_by_area[index]
    #print(df['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'].values)
    addresses = df['ADDRESS'].values
    urls = df['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'].values
    for i in range(len(addresses)):
        address_url_pair.append((addresses[i],urls[i]))

print("Address to Url: ", address_url_pair)
first_url = address_url_pair[0][1]
'''
preview_link(sys.argv[1])