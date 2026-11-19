# Currency Converter and Exchange Rate Analysis
# Works in Google Colab or Jupyter Notebook.

import requests
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
from datetime import date
from sklearn.ensemble import IsolationForest

API_URL = 'https://api.frankfurter.dev/v1'
CURRENCIES = ['EUR', 'USD', 'INR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY']


def get_rates(from_currency, to_currency, start_date, end_date):
    if from_currency == to_currency:
        raise ValueError('Choose two different currencies.')
    if start_date is None or end_date is None or start_date > end_date:
        raise ValueError('Enter a valid date range.')
    if end_date > date.today():
        raise ValueError('End date cannot be in the future.')

    url = f'{API_URL}/{start_date}..{end_date}'
    response = requests.get(url, params={'base': from_currency, 'symbols': to_currency}, timeout=30)
    response.raise_for_status()
    data = response.json()
    if 'rates' not in data or not data['rates']:
        raise ValueError('No rates found for this period.')

    rows = [(day, values[to_currency]) for day, values in data['rates'].items() if to_currency in values]
    if not rows:
        raise ValueError('No rates returned for the selected currencies.')
    df = pd.DataFrame(rows, columns=['Date', 'Rate'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date').reset_index(drop=True)


def detect_anomalies(df, sensitivity=5):
    if len(df) < 20:
        raise ValueError('Select a longer period (at least 20 exchange-rate observations).')
    result = df.copy()
    result['Daily_Change_Pct'] = result['Rate'].pct_change().fillna(0) * 100
    result['Volatility_7'] = result['Daily_Change_Pct'].rolling(7, min_periods=2).std().fillna(0)
    features = result[['Daily_Change_Pct', 'Volatility_7']]
    model = IsolationForest(contamination=sensitivity / 100, random_state=42, n_estimators=100)
    result['Anomaly'] = model.fit_predict(features) == -1
    return result


def analyze(from_currency, to_currency, start_date, end_date, sensitivity):
    rates = get_rates(from_currency, to_currency, start_date, end_date)
    result = detect_anomalies(rates, sensitivity)
    anomalies = result[result['Anomaly']]

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(result['Date'], result['Rate'], label=f'{from_currency}/{to_currency} rate')
    ax.scatter(anomalies['Date'], anomalies['Rate'], c='red', s=32, label='Anomaly', zorder=3)
    ax.set(title=f'{from_currency}/{to_currency} Exchange Rates and Anomalies', xlabel='Date', ylabel=f'{to_currency} per 1 {from_currency}')
    ax.legend()
    ax.grid(alpha=0.25)
    fig.autofmt_xdate()
    plt.show()
    plt.close(fig)

    filename = f'exchange_rates_{from_currency}_{to_currency}.csv'
    result.to_csv(filename, index=False)
    print(f'Analyzed {len(result)} exchange-rate observations.')
    print(f'Anomalies flagged: {len(anomalies)} (sensitivity: {sensitivity}%)')
    print(f'Saved CSV: {filename}')
    display(anomalies[['Date', 'Rate', 'Daily_Change_Pct']].tail(15))
    return result


def convert_latest(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount, date.today().isoformat()
    response = requests.get(f'{API_URL}/latest', params={'base': from_currency, 'symbols': to_currency}, timeout=30)
    response.raise_for_status()
    data = response.json()
    return amount * float(data['rates'][to_currency]), data['date']


def launch():
    source = widgets.Dropdown(options=CURRENCIES, value='EUR', description='From:')
    target = widgets.Dropdown(options=CURRENCIES, value='USD', description='To:')
    start = widgets.DatePicker(description='Start:', value=date(2026, 1, 1))
    end = widgets.DatePicker(description='End:', value=min(date(2026, 11, 19), date.today()))
    sensitivity = widgets.IntSlider(value=5, min=1, max=15, step=1, description='Anomaly %:')
    amount = widgets.FloatText(value=100, description='Amount:')
    chart_button = widgets.Button(description='Show analysis', button_style='primary')
    convert_button = widgets.Button(description='Convert latest')
    output = widgets.Output()

    def on_chart(_):
        with output:
            clear_output(wait=True)
            try:
                analyze(source.value, target.value, start.value, end.value, sensitivity.value)
            except (ValueError, requests.RequestException, KeyError) as error:
                print('Could not complete analysis:', error)

    def on_convert(_):
        with output:
            clear_output(wait=True)
            try:
                converted, rate_date = convert_latest(amount.value, source.value, target.value)
                print(f'{amount.value:.2f} {source.value} = {converted:.2f} {target.value} (rate date: {rate_date})')
            except (ValueError, requests.RequestException, KeyError) as error:
                print('Could not convert currency:', error)

    chart_button.on_click(on_chart)
    convert_button.on_click(on_convert)
    display(widgets.VBox([
        widgets.HBox([source, target]),
        widgets.HBox([start, end]),
        sensitivity,
        chart_button,
        widgets.HBox([amount, convert_button]),
        output
    ]))


if __name__ == '__main__':
    launch()
