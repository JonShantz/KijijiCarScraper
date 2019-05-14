import requests
from bs4 import BeautifulSoup
from csv import writer
import requests

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
    returns none and creates a CSV file, fname, with the data for all car ads, given a url.

    urlscraper: Str Str -> None


    :param url: A Kijiji URL that has Car Advertisements
    :param fname: Name of the CSV file that the data gets stored in. Remember to include .csv at the end
    :return: None
    :effects: Creates and writes to a CSV file
    """
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    LocationDatePosted = soup.find(class_="location").get_text().strip()
    DatePosted = soup.find(class_="location").find(class_="date-posted").get_text().strip()
    Location = LocationDatePosted[:LocationDatePosted.find(DatePosted)]

    def isasis(lod):
        """
        Returns True if "as is" is in the list of description words, lod. And false otherwise

        isasis: (listof Str) -> Bool
        requires: lod is a lower case list of Strs

        :param lod:
        :return:
        """
        length = len(lod)

        pos = 0
        while pos < (length-1):
            if lod[pos] == "as" and lod[pos+1] == "is":
                pos += 1
                return True
            else:
                pos += 1
        else:
            return False

    # List of posts from url

    # Going to each ad separately and pulling the data.
    with open(fname, 'w') as csv_file:
        csv_writer = writer(csv_file)
        headers = ["Location", "Price", "Make", "Model", "Year", "KMs", "Trim", "Transmission", "Body", "Color",
                   "Drivetrain", "Doors", "Seats", "isDealer", "isFlagged", "Address", "URL", "Description"]
        csv_writer.writerow(headers)

        # Grab the posts from the first page
        posts = soup.find_all(class_="info-container")

        for post in posts:
            try:
                if post is None:
                    pass
                else:
                    URLUnique = post.find('a')['href']
                    URLRoot = "https://www.kijiji.ca"
                    URL = URLRoot + URLUnique

                    CarResponse = requests.get(URL)
                    CarSoup = BeautifulSoup(CarResponse.text, 'html.parser')

                    # Pulling data on each car from the info panel
                    isDealer = post.find(class_="dealer-logo-image") is not None
                    # Want to pull description from CarSoup instead of from the homepage (Posts)
                    Description = process(CarSoup.find(class_="descriptionContainer-3544745383"))[11:]
                    if Description is not None:
                        isFlagged = isasis(Description.lower().split())
                    else:
                        isFlagged = False

                    if CarSoup.find(itemprop="address") is not None:
                        Address = CarSoup.find(itemprop="address").get_text()
                    else:
                        Address = "N/a"
                    CarData = CarSoup.find(class_="attributeListWrapper-1585172129")
                    Price = process(CarSoup.find(class_="priceContainer-2538502416"))
                    Year = process(CarData.find(itemprop="vehicleModelDate"))
                    Make = process(CarData.find(itemprop="brand"))
                    Model = process(CarData.find(itemprop="model"))
                    Trim = process(CarData.find(itemprop="vehicleConfiguration"))
                    Color = process(CarData.find(itemprop="color"))
                    Body = process(CarData.find(itemprop="bodyType"))
                    Doors = process(CarData.find(itemprop="numberOfDoors"))
                    Seats = process(CarData.find(itemprop="seatingCapacity"))
                    Drivetrain = process(CarData.find(itemprop="driveWheelConfiguration"))
                    Transmission = process(CarData.find(itemprop="vehicleTransmission"))
                    KMs = process(CarData.find(itemprop="mileageFromOdometer"))

                    # Writing the line to the file
                    csv_writer.writerow([Location, Price, Make, Model, Year, KMs, Trim, Transmission, Body, Color,
                                         Drivetrain, Doors, Seats, isDealer, isFlagged, Address, URL, Description])
            except RuntimeError:
                pass

        # Repeat as long as there are next pages to be done. This isn't elegant, and possibly not efficient, but
        #   should get the job done?

        # Not going to the next page correctly. Not sure where the problem is, although I suspect it might be something
        #    to do with the very beginning of this while loop (although it may be in the writing to CSV as well).

        # Seems to work with an if statement, but not with a while statement. Not sure why this is???

        # Just kidding, it seems to be working now, but I'm going to leave the previous comments in there just in
        #    case it stops working again, I want some amount of legacy information for troubleshooting.
        while soup.find(title="Next") is not None:
            pageunique = soup.find(title="Next")['data-href']
            pageroot = "https://www.kijiji.ca"
            page = pageroot + pageunique

            # This is the Page level
            response = requests.get(page)
            soup = BeautifulSoup(response.text, 'html.parser')

            posts = soup.find_all(class_="info-container")

            # This is the ad level ('Clicking' on each URL)
            for post in posts:
                try:
                    URLUnique = post.find('a')['href']
                    URLRoot = "https://www.kijiji.ca"
                    URL = URLRoot + URLUnique

                    CarResponse = requests.get(URL)
                    CarSoup = BeautifulSoup(CarResponse.text, 'html.parser')

                    # Pulling data on each car from the info panel
                    isDealer = post.find(class_="dealer-logo-image") is not None
                    # Take Char 11-End to remove "Description" which is at the beginning of each description.
                    Description = process(CarSoup.find(class_="descriptionContainer-3544745383"))[11:]
                    if Description is not None:
                        isFlagged = isasis(Description.lower().split())
                    else:
                        isFlagged = False
                    if CarSoup.find(itemprop="address") is not None:
                        Address = CarSoup.find(itemprop="address").get_text()
                    else:
                        Address = "N/a"
                    CarData = CarSoup.find(class_="attributeListWrapper-1585172129")
                    Price = process(CarSoup.find(class_="priceContainer-2538502416"))
                    Year = process(CarData.find(itemprop="vehicleModelDate"))
                    Make = process(CarData.find(itemprop="brand"))
                    Model = process(CarData.find(itemprop="model"))
                    Trim = process(CarData.find(itemprop="vehicleConfiguration"))
                    Color = process(CarData.find(itemprop="color"))
                    Body = process(CarData.find(itemprop="bodyType"))
                    Doors = process(CarData.find(itemprop="numberOfDoors"))
                    Seats = process(CarData.find(itemprop="seatingCapacity"))
                    Drivetrain = process(CarData.find(itemprop="driveWheelConfiguration"))
                    Transmission = process(CarData.find(itemprop="vehicleTransmission"))
                    KMs = process(CarData.find(itemprop="mileageFromOdometer"))

                    # Writing the line to the file
                    csv_writer.writerow([Location, Price, Make, Model, Year, KMs, Trim, Transmission, Body, Color,
                                         Drivetrain, Doors, Seats, isDealer, isFlagged, Address, URL, Description])
                except RuntimeError:
                    pass

    csv_file.close()
# Now I just need to make it automatically scroll through pages and grab EVERYTHING. Once I've done that, we're good!