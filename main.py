from crawl import *
import sys
#sys creates a list of arguments, the script itself is always [0], first argument is [1], and so on.

def main():
    print("Hello from web-crawler!")
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        #need to validate input later
        print("starting crawl of:", sys.argv[1])
        url = normalize_url(sys.argv[1])
        print(get_html(url))

if __name__ == "__main__":
    main()
