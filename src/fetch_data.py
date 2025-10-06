"""
fetch_data.py

This script automates downloading a set of vintage CSV files containing
vacancy time series data from the UK Office for National Statistics (ONS).

It detects the latest available vintage, then downloads a subset of recent
vintages plus the latest file.

Usage:
    python fetch_data.py
"""

import requests
import os
import time
from tqdm import tqdm

BASE_URL = "https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/ap2y/lms"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/116.0.0.0 Safari/537.36"
}

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SAFE_MIN_VINTAGE = 117


def find_latest_vintage(start: int = 200) -> int:
    """
     Detect the latest vintage version of the ONS vacancy dataset.

     Args:
         start (int): The highest vintage version number to check (default: 200).

     Returns:
         int: The latest vintage version found, with a minimum floor of SAFE_MIN_VINTAGE (v117).
     """
    print("Detecting latest vintage...")
    detected = None

    for v in reversed(range(1, start + 1)):
        url = f"{BASE_URL}/previous/v{v}"
        try:
            r = requests.get(url, headers=HEADERS, stream=True, timeout=10)
            if r.status_code == 200:
                detected = v
                break
        except requests.RequestException:
            pass
        time.sleep(0.2)

    if detected is None or detected < SAFE_MIN_VINTAGE:
        print(f"Detected v{detected}, but using safe floor v{SAFE_MIN_VINTAGE}")
        return SAFE_MIN_VINTAGE

    print(f"Latest vintage found: v{detected}")
    return detected


def download_csv(url: str, filename: str) -> None:
    """
      Download a CSV file from a URL and save it locally.

      Args:
          url (str): The URL to download the CSV from.
          filename (str): The local file path where the CSV will be saved.
      """
    if os.path.exists(filename):
        print(f"Already exists: {filename}")
        return

    retries = 3
    for i in range(retries):
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
            return
        else:
            print(f"Failed: {url} (status {r.status_code}), retry {i + 1}/{retries}")
            time.sleep(2**i)
    print(f"Giving up on {url}")


def main():
    """
    Main function of the script.

    Steps:
        1. Create the data directory if it doesn't exist.
        2. Find the latest available vintage of ONS vacancy data.
        3. Download the latest vintage and the preceding 24 vintages.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        latest_v = find_latest_vintage(start=200)
    except Exception as e:
        print(f"Error finding latest vintage: {e}")
        return

    start_version = max(1, latest_v - 24)
    end_version = latest_v

    print(f"Downloading vintages v{start_version} → v{end_version}")

    for v in tqdm(range(start_version, end_version + 1), desc="Downloading vintages"):
        url = f"{BASE_URL}/previous/v{v}"
        filename = os.path.join(DATA_DIR, f"v{v}.csv")
        download_csv(url, filename)
        time.sleep(0.5)

    latest_filename = os.path.join(DATA_DIR, "latest.csv")
    download_csv(BASE_URL, latest_filename)


if __name__ == "__main__":
    main()
