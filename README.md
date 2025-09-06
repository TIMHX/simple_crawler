# Simple Web Crawler

This project provides a simple web crawler to download PNG and JPG image files from a specified base URL and its subpages.

## Setup

1.  **Install `uv`**: If you don't have `uv` installed, you can install it using pip:
    ```bash
    pip install uv
    ```

2.  **Install Dependencies**: Ensure you have a `pyproject.toml` file in the root directory of the project. Navigate to the project's root directory in your terminal and run:
    ```bash
    uv sync
    ```
    This will create a virtual environment and install the necessary packages, including `requests`, `beautifulsoup4`, and `PyYAML`.

## Usage

To run the crawler, execute the `crawler.py` script:

```bash
uv run python crawler.py
```

The crawler will start from the `start_url` defined in [`crawler.py`](crawler.py) and recursively download image files based on the configured extensions. All downloaded images will be saved into a folder specified in [`config.yaml`](config.yaml).

## Configuration

All crawler settings are managed in `config.yaml`.

```yaml
# config.yaml
DOWNLOAD_LIMIT: 20 # Optional: Limits the number of images to download. Remove or set to null for no limit.
IMAGE_EXTENSIONS: [".png", ".jpg", ".jpeg"] # Required: List of image file extensions to download.
IMAGE_BLACKLIST: # Optional: List of keywords. Image URLs containing any of these keywords will be skipped.
  - "socials"
  - "usk"
  - "xbox1"
  - "pegi"
  - "award"
  - "steam"
  - "ps5"
  - "ct_store_logo"
  - "hunt_1896_logo"
  - "esrb_mature17"
  - "Base Game"
  - "GFDLC"
OUTPUT_FOLDER_NAME: "downloaded_images" # Required: The folder where downloaded images will be saved.
```

## Methodology

The `Simple Web Crawler` operates by performing the following steps:

1.  **Initialization**: The crawler starts with a given `start_url` and initializes a queue for URLs to visit, a set for visited URLs, and a counter for downloaded images.
2.  **Fetching and Parsing**: It fetches the content of each URL using `requests` and parses the HTML using `BeautifulSoup4` to extract all `<a>` (anchor) and `<img>` (image) tags.
3.  **URL Filtering**:
    *   **Image URLs**: It identifies image URLs based on configured `IMAGE_EXTENSIONS`. These URLs are then checked against the `IMAGE_BLACKLIST` to skip unwanted images. Valid image URLs are downloaded and saved to the `OUTPUT_FOLDER_NAME`.
    *   **Page URLs**: It identifies new page URLs (links) within the same domain as the `start_url`. These URLs are added to the queue for further crawling if they haven't been visited yet.
4.  **Download Limit**: The crawler respects an optional `DOWNLOAD_LIMIT`, stopping once the specified number of images has been downloaded.
5.  **Recursion**: The process continues recursively, exploring new links until the queue is empty, the download limit is reached, or no new valid URLs are found.


## Use Cases

This simple web crawler can be used for various purposes, such as:

*   **Archiving Website Content**: Regularly download images from a website to create a local archive for offline viewing or historical record-keeping.
*   **Content Analysis**: Collect image assets for further analysis, such as identifying branding elements, popular themes, or content trends.
*   **Asset Migration**: Gather all images from an old website before migrating to a new platform, ensuring no assets are lost.
*   **Educational Purposes**: Learn about web crawling, HTML parsing, and basic data extraction by modifying and experimenting with the crawler's logic.

### Example: Crawling Hunt Showdown Website

**Use at your own risk.**

**❌  Don't abuse it**

As an example, the crawler is configured to start from `https://www.huntshowdown.com/`. This allows you to:

*   **Collect Game Art**: Download various in-game screenshots, concept art, and promotional images directly from the official website.
*   **Monitor Updates**: Periodically run the crawler to see new images added to the site, potentially indicating new game content or events.
*   **Fan Content Creation**: Gather assets for creating fan-made content, wallpapers, or community discussions, while respecting copyright and terms of service.

Downloaded files demo:
<img width="1641" height="879" alt="图片" src="https://github.com/user-attachments/assets/e7a930ca-1350-4234-8490-605cdafa64a6" />
<img width="1611" height="819" alt="图片" src="https://github.com/user-attachments/assets/262fcadc-f13e-479b-bc1c-3aab78e416c9" />
