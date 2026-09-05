import yfinance as yf
import streamlit as st


@st.cache_data(ttl=600)
def get_current_price(ticker):
    "Récupérer le prix actuel d'une action à partir de son ticker"
    data = yf.Ticker(ticker)
    todays_data = data.history(period="1d")
    actual_value = todays_data["Close"].iloc[-1]
    return actual_value



@st.cache_data(ttl=600)
def get_price_history(ticker, p):
    "Récupérer l'historique de prix d'une action sur une période donnée"
    data = yf.Ticker(ticker)
    DataFrame = data.history(period=p)
    data_close_info = DataFrame["Close"]
    return data_close_info


if __name__ == "__main__":
    ticker = "NQ=F"
    get_current_price(ticker)
    print(get_price_history(ticker, '1mo'))