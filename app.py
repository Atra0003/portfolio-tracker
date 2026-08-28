from src.market_data import get_current_price, get_price_history
from src.portfolio import Position
from src.database import init_db, add_position, get_all_positions, delete_position, delete_all_position, update_position


def main():
    ticker = "NQ=F"
    #get_current_price(ticker)
    #print(get_price_history(ticker, '1mo'))

    p1 = Position("aaa", 10.0, 100.5, "2000-06-16")
    p2 = Position("bbb", 10.0, 100.5, "2000-06-16")
    p3 = Position("ccc", 10.0, 100.5, "2000-06-16")
    p4 = Position("ddd", 10.0, 100.5, "2000-06-16", 2)
    init_db()
    delete_all_position()

    add_position(p1)
    add_position(p2)
    add_position(p3)
    delete_position(1)
    update_position(p4)

    result =  get_all_positions()

    for i in result:
        print(i)
    print()





if __name__ == "__main__":
    main()