from src.market_data import get_current_price, get_price_history
from src.portfolio import Position, calculate_position_value, calculate_gain_loss, calculate_portfolio_summary, calculate_allocation
from src.portfolio import calculate_quantite
from src.database import init_db, add_position, get_all_positions, delete_position, delete_all_position, update_position
from src.database import get_all_prices, get_all_ticker
from datetime import date
from src.charts import plot_portfolio_evolution

def main():
    positions = get_all_positions()
    print()
    #print(positions)
    d = date(2025, 9, 5)
    t = 'AAPL'
    print(calculate_quantite(positions, t, d))


    
if __name__ == "__main__":
    main()