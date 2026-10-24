Making a web crawler in Python to practice http requests and using asyncio.

Python version: 3.12

Package dependencies:
1) BeautifulSoup4 4.13.4
2) aiohttp 3.12.12

# Instructions:
    # Clone the repo
    git clone main https://github.com/opendrill/python_web_crawler.git

    # Cd into the project directory
    cd ./python_web_crawler

    # Download requirements from requirements.txt
    pip install -r requirements.txt

    # Run the web crawler!
    python3 main.py max_concurrency max_pages

# Command examples:
1) python3 main.py 5 100
2) python3 main.py 5 unlimited
3) python3 main.py unlimited 100
4) python3 main.py unlimited unlimited

# Important notes:
1) max_concurrency and max_pages must both be integers (whole numbers).
2) max_concurrency and max_pages can both be set to 'unlimited', just type that out in place of an integer, any other non-integer value will be rejected.
3) max_concurrency sets how many http requests can be in progress at once.
4) max_pages sets how many pages can be crawled/scraped.