import os
import requests
import sys
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
sys.setrecursionlimit(10000)  # set the recursion limit to 10,000 or higher

# Define the website to be cloned
url = 'https://www.ton-mine.com'

# Define the directory to save the website in
base_dir = 'salonplex'

# Define a function to download a web page and all its dependencies
def download_page(url):
    # Make a request to the page
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Get all the links on the page
    links = soup.find_all('a')
    # Loop through each link
    for link in links:
        # Get the URL of the link
        href = link.get('href')
        # If the link is relative, make it absolute
        if not urlparse(href).netloc:
            href = urljoin(url, href)
        # Get the filename of the link
        filename = os.path.join(base_dir, urlparse(href).path.lstrip('/'))
        # Create the directory to save the file in
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # If the link is a page, download it recursively
        if href.endswith('/') and not href.startswith('mailto:'):
            download_page(href)
        # If the link is a file, download it
        elif not href.startswith('mailto:'):
            response = requests.get(href, headers={'User-Agent': 'Mozilla/5.0'})
            with open(filename, 'wb') as f:
                f.write(response.content)

# Download the website
download_page(url)
