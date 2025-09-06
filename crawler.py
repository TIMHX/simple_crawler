import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import yaml


class SimpleCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.downloaded_image_names = (
            set()
        )  # New set to store names of downloaded images
        self.downloaded_count = 0

        # Load config
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        self.output_folder_name = config.get("OUTPUT_FOLDER_NAME", "downloaded_images")
        os.makedirs(self.output_folder_name, exist_ok=True)

        self.download_limit = config.get(
            "DOWNLOAD_LIMIT"
        )  # Default to None (no limit) if not in config
        self.image_extensions = tuple(config.get("IMAGE_EXTENSIONS"))
        self.image_blacklist = config.get("IMAGE_BLACKLIST", [])

    def _download_image(self, image_url):
        parsed_url = urlparse(image_url)
        image_name = os.path.basename(parsed_url.path)

        if image_name in self.downloaded_image_names:
            print(f"Skipping duplicate image: {image_name}")
            return

        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            image_path = os.path.join(self.output_folder_name, image_name)

            with open(image_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded: {image_name}")
            self.downloaded_image_names.add(image_name)
            self.downloaded_count += 1
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {image_url}: {e}")
        except Exception as e:
            print(f"Error saving {image_url} to folder: {e}")

    def _get_all_links(self, url, soup):
        links = set()
        for a_tag in soup.findAll("a", href=True):
            href = a_tag.attrs.get("href")
            if href:
                full_url = urljoin(url, href)
                if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                    links.add(full_url)
        return links

    def _get_all_images(self, url, soup):
        images = set()

        # Extract images from <img> tags
        for img_tag in soup.findAll("img", src=True):
            src = img_tag.attrs.get("src")
            if src and src.lower().endswith(self.image_extensions):
                full_url = urljoin(url, src)
                if not any(
                    keyword.lower() in full_url.lower()
                    for keyword in self.image_blacklist
                ):
                    images.add(full_url)

        # Extract images from <meta property="og:image"> tags
        for meta_tag in soup.findAll("meta", property=lambda x: x and "og:image" in x):
            content = meta_tag.attrs.get("content")
            if content and content.lower().endswith(self.image_extensions):
                full_url = urljoin(url, content)
                if not any(
                    keyword.lower() in full_url.lower()
                    for keyword in self.image_blacklist
                ):
                    images.add(full_url)
        return images

    def download_specific_images(self, image_urls):
        print("\nAttempting to download specific images:")
        for image_url in image_urls:
            self._download_image(image_url)

    def crawl(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        print(f"Crawling: {url}")

        try:
            response = requests.get(
                url, allow_redirects=True, timeout=10
            )  # Added timeout and explicit allow_redirects
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Download images
            images = self._get_all_images(url, soup)
            for image_url in images:
                if (
                    self.download_limit is not None
                    and self.downloaded_count >= self.download_limit
                ):
                    print(
                        f"Download limit of {self.download_limit} reached. Stopping image downloads."
                    )
                    return
                self._download_image(image_url)

            # Crawl subpages
            links = self._get_all_links(url, soup)
            for link in links:
                self.crawl(link)

        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}")


if __name__ == "__main__":
    start_url = "https://www.huntshowdown.com/"
    crawler = SimpleCrawler(start_url)
    # crawler.crawl(start_url) # This will be called from a separate test script

    print(f"All images saved to {crawler.output_folder_name}")
