# ONS Vacancy Time Series Analysis

This project downloads, processes, and analyzes Office for National Statistics (ONS) vacancy time series data.  
It produces cleaned datasets, visualizations, and forecasts.

---
## Project Structure
```
boe_ons/
├── src/ # Scripts for downloading and cleaning data
│ ├── fetch_data.py
│ └── data_cleaning_structuring.py
│ └── main.py
│
├── analysis/ # Scripts for visualizing and forecasting
│ ├── plot_monthly_vacancies.py
│ └── forecasting_model.py
│
├── data/ # Stores downloaded and processed data
│
└── README.md
```

---

## Installation

### Using Poetry (recommended)

Poetry is a modern dependency manager for Python projects.  
If you don’t have Poetry installed, follow instructions:  
[Poetry installation guide](https://python-poetry.org/docs/#installation)

Once Poetry is installed:

```bash
# Clone this repository
git clone https://github.com/mohsinnadeems/boe_ons
cd boe_ons

# Install dependencies
poetry install

# Activate the environment
poetry shell

```

### Without Poetry
```bash
# Clone repository
git clone https://github.com/mohsinnadeems/boe_ons
cd boe_ons

# Install dependencies
pip install -r requirements.txt
 ```


## How to Run the Project

Once dependencies are installed, run the entire pipeline with a single command:
```bash
python src/main.py
```

This will:

#### 1- Fetch vacancy data directly from the ONS API (latest and historical vintages).

#### 2- Clean and consolidate the downloaded files into a structured dataset:
```
➤ data/cleaned_monthly_series.csv
```

#### 3- Generate visualizations showing monthly trends and revisions over time:
```
➤ plots/monthly_vacancies.png
```

#### 4- Build a forecasting model using Holt–Winters exponential smoothing and save outputs:
```
➤ plots/forecasting_plot.png
➤ data/forecasting.csv
```

#### After execution, you’ll find:

Cleaned datasets in the data/ folder

Generated plots in the plots/ folder

## Notes

#### The pipeline is modular: each step (fetch, clean, visualize, forecast) can be run independently if needed.

#### All scripts are documented with docstrings for readability and reproducibility.
