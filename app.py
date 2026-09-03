from src.market_data import get_current_price, get_price_history
from src.portfolio import Position, calculate_position_value, calculate_gain_loss, calculate_portfolio_summary, calculate_allocation
from src.portfolio import calculate_quantite, build_portfolio_history, prepare_benchmark_comparison
from src.database import init_db, add_position, get_all_positions, delete_position, delete_all_position, update_position
from src.database import get_all_prices, get_all_ticker
from datetime import date
from src.charts import plot_portfolio_evolution, plot_allocation_pie, plot_vs_benchmark
import pandas as pd

def main():
    positions = get_all_positions()
    t = get_all_ticker()
    periode = "1mo"
    benchmark_ticker = "^GSPC"
    dico, benchmark = prepare_benchmark_comparison(positions, t, periode, benchmark_ticker)
    plot_vs_benchmark(dico, benchmark)

    
if __name__ == "__main__":
    main()