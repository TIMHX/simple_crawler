import yaml
from crawler import SimpleCrawler

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    start_urls = config.get("START_URLS", ["https://www.huntshowdown.com/"])

    crawler = SimpleCrawler(start_urls)
    crawler.crawl()

    print(f"All images saved to {crawler.output_folder_name}")
