# Similar to KijijiCarScraper.py except that this will email the URL for all new 
# Ads to the specified email address

import requests
from bs4 import BeautifulSoup
from csv import writer
from datetime import date


# Returns the Text if non-empty, and "-" if empty
def process(rawdata):
    if rawdata is None:
        return "N/A"
    else:
        return rawdata.get_text()

 
# Flagged Word List = "As is", "Rebuild", "Rebuilt", "Salvaged". "Salvage"
# This might be good to implement later, but would also take a lot of computation time, so right now just
#    looking for "as is"


def urlscraper(url, fname):
    """
    returns none and creates a CSV file, fname, with the data for all car ads on the first page of a given url.

    urlscraper: Str Str Str -> None


    :param url: A Kijiji URL that has Car Advertisements
    :param fname: Name of the CSV file that the data gets stored in. Remember to include .csv at the end
    :return: None
    :effects: Creates and writes to a CSV file
    """

    # Pulling the raw html given a URL
    response = requests.get(url)
    html_text = BeautifulSoup(response.text, 'html.parser')
    posts = html_text.find_all(class_="info-container")

    # List of posts from url

    # Going to each ad separately and pulling the data.
    with open(fname, 'w') as csv_file:
        csv_writer = writer(csv_file)
        headers = ["price", "make", "model", "year", "km", "trim", "transmission",
                   "drivetrain", "url", "description"]
        csv_writer.writerow(headers)

        # We're going to want to compare each posts URL against the already existing URLs, and email us if it's new.


        for post in posts:
            url_unique = post.find('a')['href']
            url_root = "https://www.kijiji.ca"
            url = url_root + url_unique

            post_response = requests.get(url)
            post_html_text = BeautifulSoup(post_response.text, 'html.parser')
            post_data = post_html_text.find(class_="attributeListWrapper-1585172129")

            if post_data is None: 
                pass
            else:
                price = process(post_html_text.find(class_="priceContainer-2538502416"))
                make = process(post_data.find(itemprop="brand"))
                model = process(post_data.find(itemprop="model"))
                year = process(post_data.find(itemprop="vehicleModelDate"))
                km = process(post_data.find(itemprop="mileageFromOdometer"))
                trim = process(post_data.find(itemprop="vehicleConfiguration"))
                transmission = process(post_data.find(itemprop="vehicleTransmission"))
                description = process(post_html_text.find(class_="descriptionContainer-3544745383"))[11:]
                
                drivetrain = process(post_data.find(itemprop="driveWheelConfiguration"))

                # Writing the line to the file
                csv_writer.writerow([price, make, model, year, km, trim, transmission,
                                    drivetrain, url, description])

        # Repeat as long as there are next pages to be done. This isn't elegant, and possibly not efficient, but
        #   should get the job done?

        # Not going to the next page correctly. Not sure where the problem is, although I suspect it might be something
        #    to do with the very beginning of this while loop (although it may be in the writing to CSV as well).

        # Seems to work with an if statement, but not with a while statement. Not sure why this is???

        # Just kidding, it seems to be working now, but I'm going to leave the previous comments in there just in
        #    case it stops working again, I want some amount of legacy information for troubleshooting.

today = str(date.today())

create_todays_file = urlscraper("https://www.kijiji.ca/b-cars-trucks/london/forester/k0c174l1700214?price=__7000&price-type=fixed", "LondonSubarus"+today)

# Now I need to compare today's file with yesterday's file. 

def new_cars(today_cars, yesterday_cars):
    '''
    Returns none and creates a new CSV file with all the cars in today's file which were
    not included in yesterdays file
    '''

def email_new_cars(new_cars, email_address)
    '''
    returns None and emails a copy of the new_cars CSV file to the specified email_adddress.
    '''