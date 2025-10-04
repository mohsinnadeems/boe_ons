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


def find_latest_vintage(start=200):
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


def download_csv(url, filename):
    if os.path.exists(filename):
        print(f"Already exists: {filename}")
        return

    retries = 3
    for i in range(retries):
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"Downloaded: {filename}")
            return
        else:
            print(f"Failed: {url} (status {r.status_code}), retry {i + 1}/{retries}")
            time.sleep(2 ** i)
    print(f"Giving up on {url}")


def main():
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
