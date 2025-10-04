import pandas as pd
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "cleaned_monthly_series.csv"


def extract_release_date(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.lower().startswith('"release date"'):
                return line.split(",")[1].strip().strip('"')
    return None


def parse_csv(file_path):
    release_date = extract_release_date(file_path)
    df = pd.read_csv(file_path, skiprows=7, header=None, names=["Period", "Vacancies"])
    df["Vacancies"] = pd.to_numeric(df["Vacancies"], errors="coerce")
    df["ReleaseDate"] = pd.to_datetime(release_date, dayfirst=True, errors="coerce")

    monthly_mask = df["Period"].str.match(r"\d{4} [A-Z]{3}")
    return df[monthly_mask]


def main():
    vintages = sorted(DATA_DIR.glob("*.csv"))
    all_data = []

    print(f"Processing {len(vintages)} vintage files...")
    for vintage_file in tqdm(vintages):
        try:
            df = parse_csv(vintage_file)
            if not df.empty:
                df["VintageFile"] = vintage_file.name
                all_data.append(df)
        except Exception as e:
            print(f"Error processing {vintage_file}: {e}")

    if all_data:
        cleaned_df = pd.concat(all_data, ignore_index=True)
        cleaned_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Cleaned monthly data saved to {OUTPUT_FILE}")
    else:
        print("No data processed.")


if __name__ == "__main__":
    main()
