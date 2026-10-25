# Intro:
    This is a basic web crawler that creates a dictionary where each url crawled is a key and each value is a nested dictionary of strings and lists, containing the following information; "url", "heading", "first_paragraph", "outgoing_links", and "image_urls".
    
    There are issues with using this on some websites, anything with half decent security will return http status codes 403 or 429 for "forbidden" and "too many requests", I will not be adding workarounds for these as the point of this project was to practice/learn specific things that I feel I have now done. This is meant to be a basic test web crawler for learning the fundamentals of how they work, not a sophisticated one to be seriously used.

# Dependencies:
    # Python version:
    3.12

    # Packages:
    1) BeautifulSoup4 4.13.4
    2) aiohttp 3.12.12
    3) requests 2.32.4

# Instructions:
    1) Clone the repo
    git clone https://github.com/opendrill/python_web_crawler.git
    
    2) Cd into the project directory
    cd ./python_web_crawler
    
    3) Create a virtual environment
    python3 -m venv .venv
    
    4) Activate the virtual environment
    On Linux: source .venv/bin/activate
    On Windows: .venv\Scripts\activate #Haven't tried on Windows.

    5) Download requirements from requirements.txt
    pip install -r requirements.txt

    6) Run the web crawler!
    python3 main.py max_concurrency max_pages

# Command examples:
    1) python3 main.py https://example-url.com 5 100
    2) python3 main.py https://example-url.com 5 unlimited
    3) python3 main.py https://example-url.com unlimited 100
    4) python3 main.py https://example-url.com unlimited unlimited

# Important notes:
    1) max_concurrency and max_pages must both be integers (whole numbers).
    2) max_concurrency and max_pages can both be set to 'unlimited', just type that out in place of an integer, any other non-integer value will be rejected.
    3) max_concurrency sets how many http requests can be in progress at once.
    4) max_pages sets how many pages can be crawled/scraped.