import pandas as pd
import pytest

from src import market_data


class FakeTicker:
    def __init__(self, ticker, dataframe):
        self.ticker = ticker
        self.dataframe = dataframe
        self.period = None

    def history(self, period):
        self.period = period
        return self.dataframe


def call_without_streamlit_cache(function, *args):
    wrapped = getattr(function, "__wrapped__", function)
    return wrapped(*args)


def test_get_current_price_returns_latest_close(monkeypatch):
    frame = pd.DataFrame({"Close": [100.0, 105.5]})
    fake = FakeTicker("AAPL", frame)
    monkeypatch.setattr(market_data.yf, "Ticker", lambda ticker: fake)

    result = call_without_streamlit_cache(market_data.get_current_price, "AAPL")

    assert result == 105.5
    assert fake.period == "1d"


@pytest.mark.parametrize("frame", [pd.DataFrame(), pd.DataFrame({"Open": [10]})])
def test_get_current_price_rejects_missing_data(monkeypatch, frame):
    monkeypatch.setattr(market_data.yf, "Ticker", lambda ticker: FakeTicker(ticker, frame))
    with pytest.raises(ValueError, match="Aucun cours disponible pour BAD"):
        call_without_streamlit_cache(market_data.get_current_price, "BAD")


def test_get_price_history_returns_close_series(monkeypatch):
    frame = pd.DataFrame({"Open": [90, 95], "Close": [100, 110]})
    fake = FakeTicker("AAPL", frame)
    monkeypatch.setattr(market_data.yf, "Ticker", lambda ticker: fake)

    result = call_without_streamlit_cache(market_data.get_price_history, "AAPL", "1mo")

    assert result.tolist() == [100, 110]
    assert fake.period == "1mo"


@pytest.mark.parametrize("frame", [pd.DataFrame(), pd.DataFrame({"Open": [10]})])
def test_get_price_history_rejects_missing_data(monkeypatch, frame):
    monkeypatch.setattr(market_data.yf, "Ticker", lambda ticker: FakeTicker(ticker, frame))
    with pytest.raises(ValueError, match="Aucun historique disponible pour BAD"):
        call_without_streamlit_cache(market_data.get_price_history, "BAD", "1mo")

