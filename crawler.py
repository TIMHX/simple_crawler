import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import yaml
import logging


class SimpleCrawler:
    def __init__(
        self, _
    ):  # initial_start_urls is no longer needed as start_urls are loaded from config
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
        self.start_urls = config.get("START_URLS", ["https://www.huntshowdown.com/"])
        self.domain_whitelist = {urlparse(url).netloc for url in self.start_urls}
        self.path_prefixes = {urlparse(url).path for url in self.start_urls}

        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels
        if (
            not self.logger.handlers
        ):  # Prevent adding handlers multiple times if script is re-run
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _download_image(self, image_url):
        parsed_url = urlparse(image_url)
        image_name = os.path.basename(parsed_url.path)

        if image_name in self.downloaded_image_names:
            self.logger.warning(f"Skipping duplicate image: {image_name}")
            return

        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            image_path = os.path.join(self.output_folder_name, image_name)

            with open(image_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            self.logger.info(f"Downloaded: {image_name}")
            self.downloaded_image_names.add(image_name)
            self.downloaded_count += 1
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading {image_url}: {e}")
        except Exception as e:
            self.logger.error(f"Error saving {image_url} to folder: {e}")

    def _get_all_links(self, url, soup):
        links = set()
        for a_tag in soup.findAll("a", href=True):
            href = a_tag.attrs.get("href")
            if href:
                full_url = urljoin(url, href)
                # Check if the link's netloc matches any of the whitelisted domains
                # And if the full_url starts with any of the start_urls
                parsed_full_url = urlparse(full_url)
                if parsed_full_url.netloc in self.domain_whitelist and any(
                    parsed_full_url.path.startswith(prefix)
                    for prefix in self.path_prefixes
                ):
                    links.add(full_url)
        return links

    def _get_all_images(self, url, soup):
        images = set()

        # # Extract images from <img> tags
        # for img_tag in soup.findAll("img", src=True):
        #     src = img_tag.attrs.get("src")
        #     if src and src.lower().endswith(self.image_extensions):
        #         full_url = urljoin(url, src)
        #         if not any(
        #             keyword.lower() in full_url.lower()
        #             for keyword in self.image_blacklist
        #         ):
        #             images.add(full_url)

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
                    self.logger.debug(f"Found image URL: {full_url}")
        return images

    def download_specific_images(self, image_urls):
        self.logger.info("Attempting to download specific images:")
        for image_url in image_urls:
            self._download_image(image_url)

    def crawl(self):
        queue = list(self.start_urls)
        while queue:
            url = queue.pop(0)
            if url in self.visited_urls:
                continue
            self.visited_urls.add(url)
            self.logger.info(f"Crawling: {url}")

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
                        self.logger.warning(
                            f"Download limit of {self.download_limit} reached. Stopping image downloads."
                        )
                        return
                    self._download_image(image_url)

                # Crawl subpages
                links = self._get_all_links(url, soup)
                for link in links:
                    if link not in self.visited_urls:
                        queue.append(link)

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error crawling {url}: {e}")


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    start_urls_from_config = config.get("START_URLS", ["https://www.huntshowdown.com/"])

    crawler = SimpleCrawler(start_urls_from_config)
    crawler.crawl()

    crawler.logger.info(f"All images saved to {crawler.output_folder_name}")
