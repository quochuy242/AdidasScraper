import csv
import json
import os
import time
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urljoin

from curl_cffi import requests
from pydantic_csv import BasemodelCSVWriter
from rich import print

from item import Item


def get_json(api: str) -> Dict:
    try:
        resp = requests.get(api, impersonate="chrome")
        text = json.loads(resp.text)
        return text
    except Exception as e:
        print(f"[red]Error while requesting {api}: {e}")
        raise e


def get_api(country: str = "en", start_num: int = 0, search_item: str = "shoes") -> str:
    return f"https://www.adidas.com.vn/api/plp/content-engine?sitePath={country}&query={search_item}&start={start_num}"


def get_detail_api(product_id: str) -> str:
    return f"https://www.adidas.com.vn/api/search/product/{product_id}?sitePath=en"


def get_total_item(text: Dict) -> int:
    return text["raw"]["itemList"]["count"]


def get_info(text: Dict) -> None:
    print(f"Result of searching: {text['title']}")
    print(f"Total of items: {text['raw']['count']}")
    print(
        f'Scrape from {int(text['raw']['startIndex'])} item to {int(text['raw']['startIndex']) + 48} item'
    )
    return None


def get_items(text: Dict, detail: bool) -> List[Item]:
    def get_detail(link: str) -> Tuple[str, str]:
        if detail:
            detail_json = get_json(api=link)
            try:
                color = detail_json["color"]
                image = detail_json["image"]["src"]
            except Exception as e:
                print(f"[red]Error while getting detail of {link}: {e}")
                return None, None
        else:
            color = image = None
        return color, image

    items = []
    for item in text["raw"]["itemList"]["items"]:
        product_id = item["productId"]
        title = item["displayName"]
        subtitle = item["subTitle"]
        division = item["division"]
        price = int(item["price"])
        link = urljoin("https://www.adidas.com.vn", item["link"])

        if item["colorVariations"]:
            for color_id in item["colorVariations"]:
                new_link = urljoin(
                    "https://www.adidas.com.vn", link.replace(product_id, color_id)
                )
                color, image = get_detail(link=get_detail_api(color_id))
                items.append(
                    Item(
                        id=color_id,
                        title=title,
                        subtitle=subtitle,
                        division=division,
                        price=price,
                        link=new_link,
                        color=color,
                        image=image,
                    )
                )
        color, image = get_detail(link=get_detail_api(product_id))
        items.append(
            Item(
                id=product_id,
                title=title,
                subtitle=subtitle,
                division=division,
                price=price,
                link=link,
                color=color,
                image=image,
            )
        )

    return items


def save_to_csv(items: Iterable[Item], file_name: str = "./output/adidas.csv") -> None:
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, mode="a", newline="", encoding="utf-8") as fp:
        writer = BasemodelCSVWriter(fp, data=items, model=Item)
        writer.write()
    return
