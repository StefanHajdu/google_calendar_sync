import requests
from requests.exceptions import HTTPError
import time

from parse_html import parse_html_response

from config import urls, YEAR


def get_html_content(url, idx):
    response = None
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Response status for url: {url}: {response.status_code}")
    except HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as err:
        print(f"Error: {err}")

    return parse_html_response(response.text, **{"month": idx, "year": YEAR})


start = time.time()

for idx, url in enumerate(urls):
    print(f"{get_html_content(url, idx+1)}\n")
    break

end = time.time()
print(f"executed in: {end - start}")
