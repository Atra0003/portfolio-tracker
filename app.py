from src.market_data import get_current_price, get_price_history
from src.portfolio import Position
from src.database import init_db, add_position, get_all_positions


def main():
    ticker = "NQ=F"
    get_current_price(ticker)
    #print(get_price_history(ticker, '1mo'))

    portfolio = Position("bbb", 10.0, 100.5, "2000-06-16")
    init_db()
    #add_position(portfolio)
    result =  get_all_positions()
    for i in result:
        print(i)




if __name__ == "__main__":
    main()