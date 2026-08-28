from src.market_data import get_current_price, get_price_history


def main():
    ticker = "NQ=F"
    get_current_price(ticker)
    print(get_price_history(ticker, '1mo'))



if __name__ == "__main__":
    main()