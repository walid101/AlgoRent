import sys
from google_images_download import google_images_download
from bing_images import bing
from selenium import webdriver
#DEPRECATED - Walid Khan 2/24/22
response = google_images_download.googleimagesdownload() 
def downloadimages(query):
    # keywords is the search query
    # format is the image file format
    # limit is the number of images to be downloaded
    # print urs is to print the image file url
    # size is the image size which can
    # be specified manually ("large, medium, icon")
    # aspect ratio denotes the height width ratio
    # of images to download. ("tall, square, wide, panoramic")
    arguments = {"keywords": query,
                 "format": "jpg",
                 "limit":4,
                 "print_urls":True,
                 "size": "medium",
                 "aspect_ratio":"panoramic"}
    try:
        response.download(arguments)
      
    # Handling File NotFound Error    
    except FileNotFoundError: 
        arguments = {"keywords": query,
                     "format": "jpg",
                     "limit":4,
                     "print_urls":True, 
                     "size": "medium"}
                       
        # Providing arguments for the searched query
        try:
            # Downloading the photos based
            # on the given arguments
            response.download(arguments) 
        except:
            pass

def bing_img_search(query):
    urls = bing.fetch_image_urls(query, limit=10, file_type='png')
    print("{} images.".format(len(urls)))
    counter = 1
    for url in urls:
        print("{}: {}".format(counter, url))
        counter += 1

bing_img_search("Cat")