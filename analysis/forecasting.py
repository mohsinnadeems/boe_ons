"""
forecasting.py

This script applies the Holt-Winters Exponential Smoothing method
to forecast monthly vacancies for the next 2 years based on historical data.

Outputs:
    - Saves forecast plot to 'plots/forecasting_plot.png'
    - Saves forecast data to 'data/forecasting.csv'
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from typing import Tuple


def get_base_dirs() -> Tuple[Path, Path, Path]:
    """
    Determine base, data, and plots directories.

    Returns:
        Tuple[Path, Path, Path]: (BASE_DIR, data_path, PLOTS_DIR)
    """
    try:
        BASE_DIR = Path(__file__).parent.parent
    except NameError:
        BASE_DIR = Path.cwd()

    data_path = BASE_DIR / "data"
    PLOTS_DIR = BASE_DIR / "plots"
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    return BASE_DIR, data_path, PLOTS_DIR


def load_vacancy_data(path: Path) -> pd.Series:
    """
    Load cleaned vacancy data and return a time series.

    Args:
        path (Path): Path to the cleaned CSV file.

    Returns:
        pd.Series: Vacancy time series indexed by Period.
    """
    df = pd.read_csv(path / "cleaned_monthly_series.csv")
    df["Period"] = pd.to_datetime(df["Period"], format="%Y %b")
    df.set_index("Period", inplace=True)

    return df["Vacancies"].astype(float).resample("M").mean()


def fit_holt_winters(
    train: pd.Series, seasonal_periods: int = 12
) -> ExponentialSmoothing:
    """
    Fit Holt-Winters Exponential Smoothing model.

    Args:
        train (pd.Series): Time series training data.
        seasonal_periods (int): Seasonal cycle length.

    Returns:
        ExponentialSmoothing: Fitted model.
    """
    model = ExponentialSmoothing(
        train, seasonal="additive", seasonal_periods=seasonal_periods, trend="add"
    )
    return model.fit()


def forecast_future(fit, steps: int) -> pd.Series:
    """
    Forecast future values from a fitted model.

    Args:
        fit: Fitted Holt-Winters model.
        steps (int): Number of steps to forecast.

    Returns:
        pd.Series: Forecasted values.
    """
    forecast = fit.forecast(steps=steps)
    return forecast.round().astype(int)


def plot_forecast(
    train: pd.Series,
    forecast: pd.Series,
    forecast_index: pd.DatetimeIndex,
    output_path: Path,
) -> None:
    """
    Plot historical data and forecast.

    Args:
        train (pd.Series): Historical vacancy data.
        forecast (pd.Series): Forecasted vacancies.
        forecast_index (pd.DatetimeIndex): Index for forecasted values.
        output_path (Path): Path to save the plot.

    Returns:
        None
    """
    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train, label="Historical Data", color="blue")
    plt.plot(
        forecast_index,
        forecast,
        label="Forecast (2 Years Ahead)",
        color="red",
        linestyle="--",
    )
    plt.title("Holt-Winters Forecast of Monthly Vacancies")
    plt.xlabel("Date")
    plt.ylabel("Vacancies (thousands)")
    plt.legend()
    plt.grid()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()


def save_forecast(
    forecast_index: pd.DatetimeIndex, forecast: pd.Series, path: Path
) -> None:
    """
    Save forecasted values to CSV.

    Args:
        forecast_index (pd.DatetimeIndex): Forecast index.
        forecast (pd.Series): Forecast values.
        path (Path): Output CSV path.

    Returns:
        None
    """
    forecast_df = pd.DataFrame(
        {"Period": forecast_index, "Predicted Vacancies": forecast}
    )
    forecast_df.to_csv(path, index=False)


def main() -> None:
    """
    Main function to load data, fit model, forecast vacancies, plot and save results.
    """
    BASE_DIR, data_path, PLOTS_DIR = get_base_dirs()
    vacancies = load_vacancy_data(data_path)

    train = vacancies
    fit = fit_holt_winters(train)

    forecast_steps = 24
    forecast = forecast_future(fit, forecast_steps)

    forecast_index = pd.date_range(
        start=train.index[-1] + pd.DateOffset(months=1),
        periods=forecast_steps,
        freq="M",
    )

    plot_forecast(train, forecast, forecast_index, PLOTS_DIR / "forecasting_plot.png")
    save_forecast(forecast_index, forecast, data_path / "forecasting.csv")


if __name__ == "__main__":
    main()
