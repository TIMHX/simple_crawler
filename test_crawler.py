from crawler import SimpleCrawler

if __name__ == "__main__":
    start_url = "https://www.huntshowdown.com/news/behind-the-storm-technical-design-of-thundershower-in-hunt-showdown"
    crawler = SimpleCrawler(start_url)
    crawler.crawl(start_url)

    print(f"All images saved to {crawler.output_folder_name}")
