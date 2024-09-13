from rich import print
import httpx
import asyncio
from selectolax.parser import HTMLParser
from typing import List
from tqdm import tqdm, trange

# Base url, add number of page to get the url of each page
URL = "https://www.adidas.com.vn/en/men-shoes?start="


def get_num_pages(html: HTMLParser) -> int:
    """
    Get the number of pages from the html content
    """
    try:
        num_pages = html.css_first(
            "span[data-auto-id=pagination-pages-container]"
        ).text()
        num_pages = num_pages.split("of")[-1].strip()
        return int(num_pages)
    except AttributeError:
        return 1


async def get_html_content(url: str, client: httpx.AsyncClient) -> HTMLParser | None:
    try:
        response = await client.get(
            url,
            timeout=200,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"
            },
        )
        response.raise_for_status()
        return HTMLParser(response.text)
    except httpx.HTTPStatusError as e:
        print(f"Error while requesting {e.request.url!r}.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


async def get_product_url(html: HTMLParser) -> List[str]:
    """
    Get the url of each product from the html content
    """
    try:
        product_urls = html.css(
            "div[data-auto-id=glass-product-card] a.glass-product-card__assets-link"
        )
        return [product_url.attributes["href"] for product_url in product_urls]
    except AttributeError:
        return []


async def main() -> None:
    async with httpx.AsyncClient() as client:
        # Read the 1st page
        html = await get_html_content(URL, client)

        # Get the number of pages
        if html is not None:
            num_pages = get_num_pages(html)
            print(f"Number of pages: {num_pages}")

        # Get all of product urls from all pages
        product_urls = []
        for page in trange(0, num_pages + 1, desc="Page"):
            html = await get_html_content(URL + str(page * 48), client)
            product_urls.extend(await get_product_url(html))
            await asyncio.sleep(0.5)
        print(product_urls)
        print(f"Number of products: {len(product_urls)}")


if __name__ == "__main__":
    asyncio.run(main())
