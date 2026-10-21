from urllib.parse import *
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests

#BeautifulSoup() - creates an object out of the html text
#.find() - finds a specified tag within the object
#.get_text() - gets the text from the tag.

class page_data(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(url: str,)-> str:
    #This needs touching up
    url = urlsplit(url)
    path = url.path
    if path.endswith('/'):
        path = path[:-1]
    return url.scheme + "://" + url.netloc + path

def get_html(url: str)-> str:
    #will need to change the headers later for general use.
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0",})
    #Error checking.
    if response.status_code >= 400 and response.status_code <= 499:
        raise Exception(f"client side error, status code is {response.status_code}")
    if response.status_code >= 500 and response.status_code <= 599:
        raise Exception(f"server side error, status code is {response.status_code}")
    if response.headers['Content-Type'] == None:
        raise Exception("content-type header is not text/html")
    return response.text

def get_heading_from_html(html: str)-> str:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.h1
    if h1 == None:
        return ""
    else:
        return h1.get_text(strip=True)

def get_first_paragraph_from_html(html: str)-> str:
    #Check inside <p> <main> <p> </p> </main> </p> first, then check <p> </p> if there is no main.
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find('main')
    if main:
        p = main.find('p')
        if p:
            return p.get_text(strip=True)
        else:
            #if p is after main and not within it, it is not the info we want for this function.
            return ""
    else:
        p = soup.find('p')
        if p:
            return p.get_text(strip=True)
        else:
            return ""

def get_urls_from_html(html: str, base_url: str)-> list[str]:
    #URLs in html can be absoute or relative,
    #we must join them with the base url to ensure they end up absolute.
    soup = BeautifulSoup(html, "html.parser")
    url_list = []
    for link in soup.find_all('a'):
        href = urljoin(base_url, link.get('href'))
        if href:
            url_list.append(href)
    return url_list

def get_images_from_html(html: str, base_url: str)-> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    img_list = []
    for link in soup.find_all('img'):
        src = urljoin(base_url, link.get('src'))
        if src:
            img_list.append(src)
    return img_list

def extract_page_data(html: str, base_url: str)-> dict[str]:
    return {
        "url": base_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, base_url),
        "image_urls": get_images_from_html(html, base_url)
    }