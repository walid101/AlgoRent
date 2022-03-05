# AlgoRent 
AlgoRent is a django based webapp powered with a custom built Web Scraper and Web Surfer. The app takes an address as input and provides a list of house listings near that address.
AlgoRent converts listing prices from USD to ALG (AlgoRand) and acts a middleman for currency exchange during real estate buyins.
### Website Deployment : https://algorent.herokuapp.com/
## Challenges and Solutions:
Generic Webscrapers lack specificity, as a result AlgoRent applies its own custom Web Scraper for specific websites. Web urls are retrieved by a custom web surfer called 
superspider_nzk, which accepts a query (e.g "bird" or "real estate") generating a list of optimal websites to refer information from. A future solution to the current dynamic web 
scraping implementation is to use a database that acts as an intermediary cache. The database would retrieve house-dictionary objects if the address given by the user has been
scraped already.

## Download and Istallation:
1. To run the AlgoRent web app locally you will need to clone this repo : 
2. Install all libraries and dependencies by: `pip install -r requirements.txt`
3. Run django's local webhosting script in the root directory: `python manage.py runserver` 

### Browser Support
Chrome - Working <br>
Safari - Working <br>
Firefox - Working <br>
Opera - Working <br>
Edge - Working <br>
