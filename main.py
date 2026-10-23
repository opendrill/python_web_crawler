from crawl import *
import sys
#sys creates a list of arguments, the script itself is always [0], first argument is [1], and so on.

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        #need to validate input later
        print("starting crawl of:", sys.argv[1])
        page_data = await crawl_site_async(sys.argv[1])

        #crawled_pages_data = crawl_page(sys.argv[1], None, None)
        #print(crawled_pages_data) #Dictionary of each page crawled and data.
        #print("Pages crawled:", len(crawled_pages_data)) #Number of pages crawled.

if __name__ == "__main__":
    asyncio.run(main())
