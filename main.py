import asyncio
import json
from typing import List

import httpx
from rich import print

from scrape import URL, fetch_product_details, fetch_product_urls
from product import Product


def save_to_json(products: List[Product], filename: str) -> None:
    """
    Save the list of products to a json file
    """
    with open(filename, "w") as f:
        json.dump([product.to_dict() for product in products], f, indent=4)


async def main() -> None:
    async with httpx.AsyncClient() as client:
        for gender in ["/en/men-shoes", "/en/woman-shoes"]:
            gender_url: str = URL + gender
            print(f"Scraping {gender_url}")

            product_urls: List[str] = await fetch_product_urls(client, gender_url)
            print("Example 5 first product: ", product_urls[:5])
            print(f"Number of products: {len(product_urls)}")

            products: List[Product] = await fetch_product_details(client, product_urls)
            print(f"Loading successful {len(products)} products")

            # Save all product to json file
            save_to_json(products, f"./json/shoes_{gender.split('/')[-1]}.json")


if __name__ == "__main__":
    asyncio.run(main())
