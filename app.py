from src.market_data import get_current_price, get_price_history
from src.portfolio import Position
from src.database import init_db


def main():
    ticker = "NQ=F"
    get_current_price(ticker)
    #print(get_price_history(ticker, '1mo'))

    Portfolio = Position("aaa", 10.0, 100.5, "2000-06-16")
    init_db()




if __name__ == "__main__":
    main()