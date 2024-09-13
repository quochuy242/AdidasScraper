import asyncio
from typing import Dict, List

import httpx
from pydantic import BaseModel
from rich import print
from selectolax.parser import HTMLParser
from tqdm import tqdm, trange
from urllib.parse import urljoin

# Base url, add number of page to get the url of each page
URL = "https://www.adidas.com.vn"


# Class to store product information
class Product(BaseModel):
    name: str = ""
    category: str = ""
    price: int = 0
    url: str = ""
    image_url: Dict[str, str] = {}
    size: List[str] = []


def get_num_pages(html: HTMLParser) -> int:
    """
    Get the number of pages from the html content
    """
    try:
        num_pages = html.css_first(
            "span[data-auto-id=pagination-pages-container]"
        ).text()
        num_pages = num_pages.replace("of ", "")
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


async def get_product_url(html: HTMLParser, base_url: str) -> List[str]:
    """
    Get the url of each product from the html content
    """
    try:
        product_urls = html.css(
            "div[data-auto-id=glass-product-card] a.glass-product-card__assets-link"
        )
        return [
            urljoin(base_url, product_url.attributes["href"])
            for product_url in product_urls
        ]
    except AttributeError:
        return []


async def get_product_details(html: HTMLParser, url: str) -> Product:
    """
    Get the details of a product from the html content
    """

    def get_image_url(html: HTMLParser) -> Dict[str, str]:
        try:
            nodes = html.css("div.color-chooser-grid___1ZBx_ a span img")
            return {
                node.attributes["alt"]
                .text()
                .replace("Colour ", "", count=1): node.attributes["src"].text()
                for node in nodes
            }
        except Exception as e:
            raise e

    def get_price(html: HTMLParser) -> int:
        try:
            price = html.css_first("div.gl-price-item notranslate").text()
        except Exception as e:
            raise e
        return int(price.replace(",", "").replace("₫", "").strip())

    def get_size(html: HTMLParser) -> List[str]:
        nodes = html.css_first("div[data-auto-id=size-selector]")
        return [node.text() for node in nodes.css("button")]

    try:
        name = (
            html.css_first("h1[data-auto-id=product-title]").attributes["span"].text()
        )
        category = (
            html.css_first("div[data-auto-id=product-category]")
            .attributes["span"]
            .text()
        )
        return Product(
            name=name,
            category=category,
            price=get_price(html),
            url=url,
            image_url=get_image_url(html),
            size=get_size(html),
        )
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return Product()


async def main() -> None:
    async with httpx.AsyncClient() as client:
        for gender in ["/en/men-shoes", "/en/woman-shoes"]:
            # Read the 1st page
            url: str = URL + gender
            html = await get_html_content(url, client)

            # Get the number of pages
            if html is not None:
                num_pages = get_num_pages(html)
                print(f"Number of pages: {num_pages}")

            # Get all of product urls from all pages
            url = url + "?start="
            product_urls = []
            for page in trange(0, num_pages + 1, desc="Page"):
                html = await get_html_content(url + str(page * 48), client)
                product_urls.extend(
                    await get_product_url(html, base_url="https://www.adidas.com.vn")
                )
                await asyncio.sleep(0.1)
            print(product_urls[:5])
            print(f"Number of products: {len(product_urls)}")

            # # Get all of product details from all product urls
            # products = []
            # for url in product_urls:  # tqdm(product_urls, desc="Product"):
            #     url = "https://www.adidas.com.vn" + url
            #     print(url)
            # #     html = await get_html_content(url, client)
            # #     products.append(await get_product_details(html, url))
            # #     await asyncio.sleep(0.1)
            # # print(f"Loading successful {len(products)} products")


if __name__ == "__main__":
    asyncio.run(main())
