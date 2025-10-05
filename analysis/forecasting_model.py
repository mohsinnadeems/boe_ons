import matplotlib

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

matplotlib.use("TkAgg")

df = pd.read_csv("data/cleaned_monthly_series.csv")
df["Period"] = pd.to_datetime(df["Period"], format="%Y %b")
df.set_index("Period", inplace=True)

vacancies = df["Vacancies"].astype(float).resample("M").mean()

train = vacancies

model = ExponentialSmoothing(
    train, seasonal="additive", seasonal_periods=12, trend="add"
)
fit = model.fit()

forecast_steps = 24
forecast = fit.forecast(steps=forecast_steps)
forecast = forecast.round().astype(int)

forecast_index = pd.date_range(
    start=train.index[-1] + pd.DateOffset(months=1), periods=forecast_steps, freq="M"
)

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
# plt.grid()
# plt.ion()  # interactive mode

plt.show()

forecast_df = pd.DataFrame({"Period": forecast_index, "Forecast": forecast})
print(forecast_df)
