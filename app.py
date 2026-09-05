from src.market_data import get_current_price, get_price_history
from src.portfolio import Position, calculate_position_value, calculate_gain_loss, calculate_portfolio_summary, calculate_allocation
from src.portfolio import calculate_quantite, build_portfolio_history, prepare_benchmark_comparison, build_positions_table
from src.database import init_db, add_position, get_all_positions, delete_position, delete_all_position, update_position
from src.database import get_all_prices, get_all_ticker
from datetime import date
from src.charts import plot_portfolio_evolution, plot_allocation_pie, plot_vs_benchmark
import pandas as pd
import streamlit as st

def main():
    st.set_page_config(
        page_title="Mon portfolio",
        layout="wide"
    )
    init_db()
    render_form()
    render_table()


def render_form(): 
    with st.form("add position"):
        ticker = st.text_input("Enttrer le ticker : ")
        quantite = st.number_input("Entrer une quantité")
        prix_achat = st.number_input("Entrer le prix d'achat/vente de l'actif : ")
        date_achat = st.date_input("Entrer la date achat/vente de l'actif : ")
        type_position = st.selectbox("Sélectionner le type de position : ", ("achat", "vente"))

        soumis = st.form_submit_button("Envoyer")
        if soumis:
            date_achat = date_achat.strftime('%Y-%m-%d')
            p = Position(ticker, quantite, prix_achat, date_achat, type_position)
            try:
                add_position(p)
                st.success("success")
            except ValueError:
                st.error("erreur lors de l'ajout")

def render_table():
    positions = get_all_positions()
    prices = get_all_prices()
    data = build_positions_table(positions, prices)
    df = pd.DataFrame(data)

    st.dataframe(
        df,
        hide_index=True,
    )




    
if __name__ == "__main__":
    main()