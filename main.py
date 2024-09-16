import argparse
from typing import Dict

import scrape


def check_number_item(num_item: int, total_item: int) -> int:
    return total_item if num_item > total_item else num_item


def main() -> None:
    parser = argparse.ArgumentParser(description="The main file of repo")
    parser.add_argument(
        "--country", type=str, default="en", help="The alpha-2 code of the country"
    )
    parser.add_argument(
        "-t", "--total-item", type=bool, required=True, help="Scraping all found items"
    )
    parser.add_argument(
        "-n",
        "--num-item",
        type=int,
        help="The number of items wanting to scrape",
        default=1000,
    )
    parser.add_argument(
        "-s",
        "--search",
        type=str,
        default="shoes",
        help="used to find products on the Adidas homepage ",
    )
    parser.add_argument(
        "-d",
        "--detail",
        type=bool,
        default=False,
        help="The bool type, used to get the detail of the items",
    )
    parser.add_argument(
        "-i",
        "--info-api",
        type=bool,
        default=False,
        help="Get the information of the json api",
    )
    parser.add_argument(
        "-c",
        "--csv",
        type=str,
        default="./output/adidas.csv",
        help="CSV output directory ",
    )
    args = parser.parse_args()

    country = args.country
    total_item = args.total_item
    num_item = args.num_item
    search = args.search
    detail = args.detail
    info_api = args.info_api
    csv_path = args.csv

    json_data: Dict = scrape.get_json(
        api=scrape.get_api(country=country, start_num=0, search_item=search)
    )

    scrape_size = int(json_data["raw"]["itemList"]["viewSize"])

    if info_api:
        scrape.get_info(text=json_data)

    count_item: int = scrape.get_total_item(text=json_data)
    num_item = (
        check_number_item(num_item=num_item, total_item=count_item)
        if not total_item
        else count_item
    )

    for ith in range(0, num_item, scrape_size):
        ith_json_data: Dict = scrape.get_json(
            api=scrape.get_api(country=country, start_num=ith, search_item=search)
        )
        items = scrape.get_items(text=ith_json_data, detail=detail)
        scrape.save_to_csv(items=items, file_name=csv_path)


if __name__ == "__main__":
    main()
