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
