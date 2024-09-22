# Adidas Product Scraper

This web scraper extracts product information from the official Adidas website using their API. The scraped data is saved in a CSV file for easy analysis and access.

## Usage

### 1. Clone the repo

```bash
git clone https://github.com/quochuy242/AdidasScraper.git
cd AdidasScraper
```

### 2. Install the requirements

```bash
pip3 install -r requirements.txt
```

### 3. Run the scraper

Command-line Arguments

- `--country` (str): The alpha-2 code of the country. Defaults to "en".
- `-t, --total-item` (bool): Whether to scrape all found items. This is required.
- `-n, --num-item` (int): The number of items you want to scrape. Defaults to 1000.
- `-s, --search` (str): The search term used to find products on the Adidas homepage. Defaults to "shoes".
- `-d, --detail` (bool): Whether to scrape the detailed information for each item. Defaults to `False`.
- `-i, --info-api` (bool): If set to `True`, prints the information about the API used. Defaults to `False`.
- `-c, --csv` (str): The path where the CSV file will be saved. Defaults to `./output/adidas.csv`.

Example Commands

1. Scrape all available items with the default search term ("shoes") and save to the default CSV location:
   ```bash
   python scraper.py --total-item True
   ```

2. Scrape 500 items from the U.S. Adidas website, looking for "jackets", and save the data to a specific CSV file:
   ```bash
   python scraper.py --country "us" --num-item 500 --search "jackets" --csv "./output/jackets.csv"
   ```

3. Scrape all shoes with detailed information:
   ```bash
   python scraper.py --total-item True --detail True
   ```

4. Get information about the API without scraping:
   ```bash
   python scraper.py --info-api True
   ```

## Output

The CSV file contains the following fields:
- Product Name
- Price
- Product ID
- Category
- Availability
- Other relevant product information

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you find a bug or have a feature request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
