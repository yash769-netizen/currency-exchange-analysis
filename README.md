# Currency Converter and Exchange Rate Analysis

A Python project for converting currencies and exploring historical exchange rates.

## Features
- Currency conversion using the latest available reference exchange rate
- Currency pair and date-range selection with interactive controls
- Historical exchange-rate graph
- Isolation Forest model to flag unusual daily movements
- Export analysis results to CSV

## Run in Google Colab
1. Open `Currency_Exchange_Interactive.ipynb` in Google Colab.
2. Select **Runtime → Run all**.
3. Choose the currency pair, dates and anomaly percentage.
4. Press **Show analysis** to see the graph or **Convert latest** for conversion.

The analysis uses reference rates from [Frankfurter](https://frankfurter.dev/) and requires internet access. Anomaly flags indicate unusual observations, not predictions or trading advice.

## Tools
Python, Pandas, Matplotlib, scikit-learn, ipywidgets, requests.

No API key is required.
