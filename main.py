from crawl import *
from json_report import write_json_report
import sys
#sys creates a list of arguments, the script itself is always [0], first argument is [1], and so on.

#I would like to come back to this and refine how users add arguments by putting proper parameters in place at some point.

#Validating input for arguments 2 or 3.
def arg_int_check(arg, arg_num):
    if arg == "unlimited":
        return float("inf")
    else:
        try:
            if int(arg) < 1:
                print(f"argument {arg_num} must be greater than or equal to 1")
                sys.exit(1)
            else:
                return int(arg)
        except ValueError:
            print(f"argument {arg_num} must be a whole number or 'unlimited'")
            sys.exit(1)

async def main():
    #Check number of args is correct.
    if len(sys.argv) < 4:
        print("too few arguments provided, refer to the README.md")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided, refer to the README.md")
        sys.exit(1)
    #Check arg 1 is a url
    parsed = urlparse(sys.argv[1])
    if parsed.scheme != "https" or not parsed.netloc:
        print("argument 1 must be a https URL")
        sys.exit(1)

    #Validate arg inputs for 2 and 3
    max_concurrency = arg_int_check(sys.argv[2], 2)
    max_pages = arg_int_check(sys.argv[3], 3)
    report_name = 'report.json'

    print("starting crawl of:", sys.argv[1])
    
    page_data = await crawl_site_async(sys.argv[1], max_concurrency, max_pages)
    
    print(f"finished crawl of: {sys.argv[1]}")
    
    write_json_report(page_data, report_name)
    
    print(f"report generated: {report_name}")

if __name__ == "__main__":
    asyncio.run(main())