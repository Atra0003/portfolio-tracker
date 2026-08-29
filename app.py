from src.market_data import get_current_price, get_price_history
from src.portfolio import Position, calculate_position_value, calculate_gain_loss, calculate_portfolio_summary
from src.database import init_db, add_position, get_all_positions, delete_position, delete_all_position, update_position
from src.database import get_all_prices
from datetime import date

def main():
    """
    delete_all_position()
    positions_test = [
        ("AAPL", 10, 180.50, date(2025, 1, 15)),
        ("AAPL", 5, 210.00, date(2025, 6, 10)),
        ("AAPL", 8, 195.75, date(2025, 9, 2)),
        ("MSFT", 6, 390.00, date(2025, 2, 20)),
        ("MSFT", 4, 415.30, date(2025, 7, 5)),
        ("MSFT", 10, 400.00, date(2025, 11, 1)),
        ("GOOGL", 12, 145.00, date(2025, 1, 8)),
        ("GOOGL", 7, 170.25, date(2025, 5, 18)),
        ("GOOGL", 5, 155.60, date(2025, 8, 30)),
        ("TSLA", 3, 220.00, date(2025, 3, 12)),
        ("TSLA", 6, 280.50, date(2025, 6, 25)),
        ("TSLA", 2, 340.00, date(2025, 10, 14)),
        ("AMZN", 9, 155.00, date(2025, 2, 1)),
        ("AMZN", 4, 175.40, date(2025, 7, 19)),
        ("AMZN", 11, 165.90, date(2025, 12, 3)),
    ]

    for ticker, quantite, prix_achat, date_achat in positions_test:
        p = Position(ticker=ticker, quantite=quantite, prix_achat=prix_achat, date_achat=date_achat)
        add_position(p)

    print(f"{len(positions_test)} positions insérées avec succès.")


    for p in (get_all_positions()):
        print(p)
    
    list_price = []
    for p in get_all_positions():
        price = get_current_price(p.ticker)
        list_price.append(calculate_position_value(p, price))
    print(list_price)
    
    p1 = Position("AAPL", 10, 180.50, date(2025, 1, 15))
    add_position(p1)
    price = get_current_price(p1.ticker)
    result = calculate_gain_loss(p1, price)
    print(result)
    """

    #result = calculate_portfolio_summary(get_all_positions(), get_all_prices())
    #print(result)

    prices = {}
    for p in get_all_positions():
        price = get_current_price(p.ticker)
        if p.ticker not in prices:
            prices[p.ticker] = price
        

    print(calculate_portfolio_summary(get_all_positions(), prices))




if __name__ == "__main__":
    main()