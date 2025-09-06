import yaml
from crawler import SimpleCrawler

if __name__ == "__main__":
    # Create a temporary config.yaml for testing
    test_config_content = """
DOWNLOAD_LIMIT: 20
"""
    with open("config.yaml", "w") as f:
        f.write(test_config_content)

    start_url = "https://www.huntshowdown.com/news/behind-the-storm-technical-design-of-thundershower-in-hunt-showdown"
    crawler = SimpleCrawler(start_url)
    crawler.crawl(start_url)

    print(f"All images saved to {crawler.output_folder_name}")

    # Clean up the temporary config.yaml (optional, but good practice)
    # import os
    # os.remove("config.yaml")
