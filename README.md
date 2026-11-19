# Currency Converter and Exchange Rate Analysis

I started this as a Python mini-project for currency conversion and checking past exchange rates. This version also plots the rates and highlights dates where the movement looks unusual.

## What it does

- Converts amounts using the latest available exchange rate
- Shows historical rates for a chosen currency pair and date range
- Plots the exchange rate over time
- Marks unusual observations using Isolation Forest
- Saves the analysed data to a CSV file

The anomaly check uses daily percentage change and a 7-day rolling measure of volatility. The red points aren't price predictions; they're just observations flagged by the model.

## Running it

1. Open `Currency_Exchange_Interactive.ipynb` in Google Colab.
2. Click **Runtime → Run all**.
3. Choose the currencies, dates and anomaly percentage.
4. Click **Show analysis** to generate the chart. You can also use **Convert latest** for a quick currency conversion.

I used Python, Pandas, Matplotlib, scikit-learn, ipywidgets and requests.

Exchange-rate data comes from [Frankfurter](https://frankfurter.dev/). You need an internet connection, but no API key.
