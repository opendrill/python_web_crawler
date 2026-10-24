import json

def write_json_report(page_data: dict[dict[str, list[str]]], filename: str):
    #Sort keys by url.
    pages = sorted(page_data.values(), key=lambda p: p["url"])
    #Encoding helps translate special characters. Indent makes the file human readable.
    with open(filename, 'w', encoding="utf-8") as report:
        json.dump(pages, report, indent=2)
