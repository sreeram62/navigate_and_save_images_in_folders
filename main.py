import requests
import os
from bs4 import BeautifulSoup

URL = "http://your-website/en/media/photo/"
response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

# Get all the divs which contain years
divs = soup.findAll('div', {"class": "spoiler-wrap"})

# Loop through all the years
for div in divs:

    # Get the year from the link text
    year_div = div.find("div", {"class": "spoiler-head"})
    year = year_div.find("a").getText()

    # Prepare the path of the year folder
    year_name = "images/" + year + "/"

    # Check if the year folder exists and create if folder does not exist
    isExist = os.path.exists(year_name)
    if not isExist:
        os.makedirs(os.path.dirname(year_name))

    # Get all the events which contain in that year
    links_p = div.find_all("p")

    # Loop through all the events
    for link_p in links_p:

        # Get the event name from the link text
        link = link_p.find("a")
        folder = link.getText().strip()

        # Check if the event folder exists and create if folder doesn/t exist
        folder_name = "images/" + year + "/" + folder + "/"
        isExist = os.path.exists(folder_name)
        if not isExist:
            os.makedirs(os.path.dirname(folder_name))

        # Prepare the event link and navigate to that link
        link_photos = "http://your-website/" + link['href']
        response_photos = requests.get(link_photos)
        website_html_photos = response_photos.text
        soup_photos = BeautifulSoup(website_html_photos, "html.parser")

        # Get the div content in which actually event images are present
        div_photos = soup_photos.find('div', {"class": "photo-section"})

        # Get all the images
        images = div_photos.find_all('img')

        # Loop on all the images
        for img in images:

            # Get the image url and the image
            img_url = "http://your-website" + img['src']
            data = requests.get(img_url).content

            # Prepare the name of the image how it needs to be stored
            name = img['src'].split("/")[-1]
            local_filename = "images/" + year + "/" + folder + "/" + name

            # Store the image on the local file
            with open(local_filename, 'wb') as f:
                f.write(data)
