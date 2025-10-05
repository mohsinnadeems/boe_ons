import matplotlib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

matplotlib.use("TkAgg")

BASE_DIR = Path.cwd()
data_path = BASE_DIR / "data" / "cleaned_monthly_series.csv"

df = pd.read_csv(data_path)
df["Vacancies"] = df["Vacancies"].astype(int)

df['Year'] = df['Period'].str.split().str[0].astype(int)
df['Month'] = df['Period'].str.split().str[1]

months_order = [
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
]

sns.set(style="whitegrid", palette="tab10", font_scale=1)

all_years = sorted(df['Year'].unique())
tick_years = all_years[::2]

fig, axes = plt.subplots(4, 3, figsize=(18, 12), sharey=True)
axes = axes.flatten()

for i, month in enumerate(months_order):
    ax = axes[i]
    month_df = df[df['Month'] == month]

    sns.lineplot(x='Year', y='Vacancies', data=month_df, ax=ax, marker="o", label=month)

    ax.set_title(month, fontsize=12, fontweight="bold")
    ax.set_xlabel("Year", fontsize=10)

    if i % 3 != 0:
        ax.set_ylabel("")
    else:
        ax.set_ylabel("Vacancies", fontsize=10)

    ax.set_xticks(tick_years)
    ax.set_xticklabels(tick_years, rotation=45)

    if i in [0, 1, 2]:
        if 2008 in month_df['Year'].values:
            dip_value = month_df.loc[month_df['Year'] == 2008, 'Vacancies'].values[0]
            ax.annotate(
                "Global Financial Crisis 2008",
                xy=(2008, dip_value),
                xytext=(2004, month_df['Vacancies'].max()),
                arrowprops=dict(facecolor='orange', shrink=0.05, linestyle='dashed'),
                fontsize=9, color='orange'
            )

    if i in [3, 4, 5]:
        if 2020 in month_df['Year'].values:
            dip_value = month_df.loc[month_df['Year'] == 2020, 'Vacancies'].values[0]
            ax.annotate(
                "COVID dip",
                xy=(2020, dip_value),
                xytext=(2016, month_df['Vacancies'].max()),
                arrowprops=dict(facecolor='red', shrink=0.05),
                fontsize=9, color='red'
            )

    if i in [6, 7, 8]:
        if 2021 in month_df['Year'].values:
            ax.annotate(
                "Recovery 2021",
                xy=(2021, month_df.loc[month_df['Year'] == 2021, 'Vacancies'].values[0]),
                xytext=(2018, month_df['Vacancies'].max()),
                arrowprops=dict(facecolor='green', shrink=0.05),
                fontsize=9, color='green'
            )

    if i in [9, 10, 11]:
        avg_value = month_df['Vacancies'].mean()
        last_year = month_df['Year'].max()
        last_value = month_df.loc[month_df['Year'] == last_year, 'Vacancies'].values[0]
        ax.annotate(
            "Back to average",
            xy=(last_year, last_value),
            xytext=(last_year - 3, avg_value + 10),
            arrowprops=dict(facecolor='blue', shrink=0.05),
            fontsize=9, color='blue'
        )

plt.tight_layout()
plt.suptitle("Vacancy Trends by Month Across Years", fontsize=16)
plt.show()
