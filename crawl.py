from urllib.parse import *
from bs4 import BeautifulSoup
from typing import TypedDict
import aiohttp
import asyncio

#BeautifulSoup() - creates an object out of the html text
#.find() - finds a specified tag within the object, first instance of it.
#.find_all() - finds all instances of the specified tag.
#.get_text() - gets the text from the tag.

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

class AsyncCrawler():
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.visited = set() #Sets are unique lists, prevent duplicate crawls.
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency #How many http get requests  can be ran simultaneously.
        self.semaphore = asyncio.Semaphore(self.max_concurrency) #Semaphore is like a counter. Counts down to 0.
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop == True:
                return False
            if len(self.visited) == self.max_pages:
                self.should_stop = True
                print(f"Max number of pages ({self.max_pages}) crawled. Stopping.")
                return False
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True
    
    async def get_html(self, url: str)-> str:
        #####DON'T UNDERSTAND#####
        async with self.session.get(url, headers={}) as response:
        #####DON'T UNDERSTAND#####

            #Error checking.
            if response.status >= 400 and response.status <= 499:
                raise Exception(f"client side error, status code is {response.status}")
            if response.status >= 500 and response.status <= 599:
                raise Exception(f"server side error, status code is {response.status}")
            #Needs revision
            if response.headers['Content-Type'] == None:
                raise Exception("content-type header is not text/html")
            return await response.text()

    async def crawl_page(self, current_url: str):
        if self.should_stop == True:
            return
        #Check domain matches.
        c = urlsplit(current_url)
        if c.netloc != self.base_domain:
            return
        normalized_url = normalize_url(current_url)
        #Check if the url has been crawled already.
        check_exisitng = await self.add_page_visit(normalized_url)
        if not check_exisitng:
            return
        #Get html content of the url
        async with self.semaphore:
            html = await self.get_html(normalized_url)
        #Fill out the page_data dictionary.
        current_page_data = extract_page_data(html, normalized_url)

        #####DON'T UNDERSTAND#####
        async with self.lock:
        #####DON'T UNDERSTAND#####

            self.page_data[normalized_url] = current_page_data #Self.page data is a dict of all the current_page_data dicts.

        #Creating list of tasks (found urls) to crawl next.
        tasks = []
        for link in current_page_data["outgoing_links"]:
            task = asyncio.create_task(self.crawl_page(link))
            tasks.append(task)
            self.all_tasks.add(task)
        try:
            #Waiting for all tasks to be unpacked from the list and finished.
            await asyncio.gather(*tasks)
        finally:
            for task in tasks:
                #.discard won't error if the item isn't in the list.
                self.all_tasks.discard(task)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()

def normalize_url(url: str,)-> str:
    #This needs touching up
    url = urlsplit(url)
    path = url.path
    if path.endswith('/'):
        path = path[:-1]
    return url.scheme + "://" + url.netloc + path 

def get_heading_from_html(html: str)-> str:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.h1
    if h1 == None:
        return ""
    else:
        return h1.get_text(strip=True)

def get_first_paragraph_from_html(html: str)-> str:
    #Check inside <main> <p> </p> </main> first, then check <p> </p> if there is no main.
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
    print(f"Extracted page data for {base_url}:")
    d = {
        "url": base_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, base_url),
        "image_urls": get_images_from_html(html, base_url)
    }
    print(d)
    return d