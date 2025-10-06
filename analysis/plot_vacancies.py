"""
plot_vacancies.py

This script generates a multi-panel line plot showing trends in job vacancies
across different months and years from a cleaned monthly vacancy dataset.

The visualization includes annotations highlighting key historical events
such as the Global Financial Crisis (2008), the COVID-19 dip (2020),
and the subsequent recovery (2021).

Outputs:
    - Saves the generated plot as 'monthly_vacancies.png' in the 'plots' directory.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import List

try:
    BASE_DIR: Path = Path(__file__).parent.parent
except NameError:
    BASE_DIR: Path = Path.cwd()

data_path: Path = BASE_DIR / "data" / "cleaned_monthly_series.csv"
PLOTS_DIR: Path = BASE_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def load_data(path: Path) -> pd.DataFrame:
    """
    Load cleaned monthly vacancy data.

    Args:
        path (Path): Path to the cleaned CSV file.

    Returns:
        pd.DataFrame: Loaded data with vacancies converted to integers.
    """
    df = pd.read_csv(path)
    df["Vacancies"] = df["Vacancies"].astype(int)
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess dataset by splitting 'Period' column into year and month columns.

    Args:
        df (pd.DataFrame): Raw vacancy data.

    Returns:
        pd.DataFrame: Processed data with 'Year' and 'Month' columns.
    """
    df["Year"] = df["Period"].str.split().str[0].astype(int)
    df["Month"] = df["Period"].str.split().str[1]
    return df


def create_monthly_vacancy_plot(
    df: pd.DataFrame, months_order: List[str], output_path: Path
) -> None:
    """
    Generate a line plot showing vacancy trends by month.

    Args:
        df (pd.DataFrame): Preprocessed vacancy data.
        months_order (List[str]): Ordered list of month abbreviations for plotting.
        output_path (Path): Path to save the generated plot.

    Returns:
        None
    """
    sns.set(style="whitegrid", palette="tab10", font_scale=1)

    all_years: List[int] = sorted(df["Year"].unique())
    tick_years: List[int] = all_years[::2]  # every 2 years

    fig, axes = plt.subplots(4, 3, figsize=(18, 12), sharey=True)
    axes = axes.flatten()

    for i, month in enumerate(months_order):
        ax = axes[i]
        month_df = df[df["Month"] == month]

        sns.lineplot(
            x="Year", y="Vacancies", data=month_df, ax=ax, marker="o", label=month
        )

        ax.set_title(month, fontsize=12, fontweight="bold")
        ax.set_xlabel("Year", fontsize=10)

        ax.set_xticks(tick_years)
        ax.set_xticklabels(tick_years, rotation=45)

        if i in [0, 1, 2]:
            if 2008 in month_df["Year"].values:
                dip_value = month_df.loc[month_df["Year"] == 2008, "Vacancies"].values[
                    0
                ]
                ax.annotate(
                    "Global Financial Crisis 2008",
                    xy=(2008, dip_value),
                    xytext=(2004, month_df["Vacancies"].max()),
                    arrowprops=dict(
                        facecolor="orange", shrink=0.05, linestyle="dashed"
                    ),
                    fontsize=9,
                    color="orange",
                )

        if i in [3, 4, 5]:
            if 2020 in month_df["Year"].values:
                dip_value = month_df.loc[month_df["Year"] == 2020, "Vacancies"].values[
                    0
                ]
                ax.annotate(
                    "COVID dip",
                    xy=(2020, dip_value),
                    xytext=(2016, month_df["Vacancies"].max()),
                    arrowprops=dict(facecolor="red", shrink=0.05),
                    fontsize=9,
                    color="red",
                )

        if i in [6, 7, 8]:
            if 2021 in month_df["Year"].values:
                ax.annotate(
                    "Recovery 2021",
                    xy=(
                        2021,
                        month_df.loc[month_df["Year"] == 2021, "Vacancies"].values[0],
                    ),
                    xytext=(2018, month_df["Vacancies"].max()),
                    arrowprops=dict(facecolor="green", shrink=0.05),
                    fontsize=9,
                    color="green",
                )

        if i in [9, 10, 11]:
            avg_value = month_df["Vacancies"].mean()
            last_year = month_df["Year"].max()
            last_value = month_df.loc[
                month_df["Year"] == last_year, "Vacancies"
            ].values[0]
            ax.annotate(
                "Back to average",
                xy=(last_year, last_value),
                xytext=(last_year - 3, avg_value + 10),
                arrowprops=dict(facecolor="blue", shrink=0.05),
                fontsize=9,
                color="blue",
            )

    plt.tight_layout()
    plt.suptitle("Vacancy Trends by Month Across Years", fontsize=16, y=1.02)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    """
    Main function to load, preprocess data and create vacancy trends plot.
    """
    df = load_data(data_path)
    df = preprocess_data(df)

    months_order: List[str] = [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
    ]

    output_path = PLOTS_DIR / "monthly_vacancies.png"
    create_monthly_vacancy_plot(df, months_order, output_path)


if __name__ == "__main__":
    main()
