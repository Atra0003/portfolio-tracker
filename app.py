from src.market_data import get_current_price, get_price_history
from src.portfolio import Position, calculate_position_value, calculate_gain_loss, calculate_portfolio_summary, calculate_allocation
from src.portfolio import calculate_quantite, build_portfolio_history
from src.database import init_db, add_position, get_all_positions, delete_position, delete_all_position, update_position
from src.database import get_all_prices, get_all_ticker
from datetime import date
from src.charts import plot_portfolio_evolution, plot_allocation_pie

def main():
    positions = get_all_positions()
    t = get_all_ticker()
    dico = {}
    for i in t:
        dico[i] = get_current_price(i)
    result = calculate_allocation(positions, dico)
    plot_allocation_pie(result)

    
if __name__ == "__main__":
    main()