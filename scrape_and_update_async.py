import time
import asyncio
import aiohttp

from parse_html import parse_html_response
from google_calendar_apis import insert_calendar_events
from config import urls, YEAR


async def get_html_content_async(url, session):
    try:
        response = await session.get(url, raise_for_status=True)
        print(f"Response status for url: {url}: {response.status}")
    except aiohttp.ClientConnectorError as http_err:
        print(f"[Err] HTTP error: {http_err}")
    except Exception as err:
        print(f"[Err] Other connection error: {err}")

    return await response.text()


async def process_data(url, session, idx):
    try:
        html = await get_html_content_async(url, session)
        return parse_html_response(html, **{"month": idx, "year": YEAR})
    except Exception as err:
        print(f"[Err] Error: {err}")


async def main():
    start = time.time()

    session = aiohttp.ClientSession()
    calendar_events = await asyncio.gather(
        *[process_data(url, session, idx + 1) for idx, url in enumerate(urls)]
    )
    await session.close()

    end = time.time()
    print(f"executed in: {end - start}")

    print("Calendar events gathered, pushing to Google API:")
    insert_calendar_events(sum(calendar_events, []))


asyncio.run(main())
