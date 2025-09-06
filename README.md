# Simple Web Crawler

This project provides a simple web crawler to download PNG and JPG image files from a specified base URL and its subpages.

## Setup

1.  **Install `uv`**: If you don't have `uv` installed, you can install it using pip:
    ```bash
    pip install uv
    ```

2.  **Create `pyproject.toml`**: Ensure you have a `pyproject.toml` file in the root directory of the project with the following content:
    ```toml
    [project]
    name = "simple-crawler"
    version = "0.1.0"
    dependencies = [
        "requests",
        "beautifulsoup4",
        "PyYAML",
    ]
    ```

3.  **Install Dependencies**: Navigate to the project's root directory in your terminal and run:
    ```bash
    uv sync
    ```
    This will create a virtual environment and install the necessary packages, including `PyYAML`.

## Usage

To run the crawler, execute the `crawler.py` script:

```bash
uv run python crawler.py
```

The crawler will start from `https://www.huntshowdown.com/` and recursively download image files based on the configured extensions. All downloaded images will be saved into a folder specified in `config.yaml`.

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

## Usage

To run the crawler, execute the `crawler.py` script:

```bash
uv run python crawler.py
```

The `start_url` is still defined in `crawler.py` for now.
```python
if __name__ == "__main__":
    start_url = "https://www.huntshowdown.com/" # Change this to your desired starting URL
    crawler = SimpleCrawler(start_url)
    crawler.crawl(start_url)
```