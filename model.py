import datetime
from pathlib import Path

import joblib
import pandas as pd
import yfinance as yf
from fbprophet import Prophet
import matplotlib

matplotlib.use('agg')

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()

def train(ticker):
    data = yf.download(ticker, "2020-01-01", TODAY.strftime("%Y-%m-%d"))
    data.head()
    data["Adj Close"].plot(title=f"{ticker} Stock Adjusted Closing Price")

    df_forecast = data.copy()
    df_forecast.reset_index(inplace=True)
    df_forecast["ds"] = df_forecast["Date"]
    df_forecast["y"] = df_forecast["Adj Close"]
    df_forecast = df_forecast[["ds", "y"]]
    df_forecast

    model = Prophet()
    model.fit(df_forecast)

    joblib.dump(model, Path(BASE_DIR).joinpath(f"trained_models/{ticker}.joblib"))


def predict(ticker, days=7):
    model_file = Path(BASE_DIR).joinpath(f"trained_models/{ticker}.joblib")
    if not model_file.exists():
        train(ticker)

    model = joblib.load(model_file)

    future = TODAY + datetime.timedelta(days=days)

    dates = pd.date_range(start="2020-01-01", end=future.strftime("%m/%d/%Y"),)
    df = pd.DataFrame({"ds": dates})

    forecast = model.predict(df)

    model.plot(forecast).savefig(f"predict_plots/{ticker}_plot.png")
    model.plot_components(forecast).savefig(f"predict_plots{ticker}_plot_components.png")

    return forecast.tail(days).to_dict("records")


def convert(prediction_list):
    output = {}
    for data in prediction_list:
        date = data["ds"].strftime("%m/%d/%Y")
        output[date] = data["trend"]
    return output