from src.market_data import get_current_price
from src.portfolio import Position, calculate_allocation, build_portfolio_history, build_positions_table, prepare_benchmark_comparison
from src.database import init_db, add_position, get_all_positions, get_all_tickers
from src.charts import plot_portfolio_evolution, plot_allocation_pie, plot_vs_benchmark
import pandas as pd
import streamlit as st

def main():
    st.set_page_config(
        page_title="Mon portfolio",
        layout="wide"
    )
    init_db()
    p = render_period_filter()
    render_form()
    render_table()
    render_charts(p)


def render_form(): 
    with st.form("add position"):
        ticker = st.text_input("Enttrer le ticker : ")
        quantite = st.number_input("Entrer une quantité")
        prix_achat = st.number_input("Entrer le prix d'achat/vente de l'actif : ")
        date_achat = st.date_input("Entrer la date achat/vente de l'actif : ")
        type_position = st.selectbox("Sélectionner le type de position : ", ("achat", "vente"))

        soumis = st.form_submit_button("Envoyer")
        if soumis:
            try:
                p = Position(ticker, quantite, prix_achat, date_achat, type_position)
                add_position(p)
                st.success("Position ajoutée")
            except (ValueError, OSError) as error:
                st.error(str(error))


def load_current_prices(tickers):
    return {ticker: get_current_price(ticker) for ticker in tickers}

def render_table():
    positions = get_all_positions()
    if not positions:
        st.info("Ajoutez une position pour afficher le portefeuille.")
        return
    try:
        prices = load_current_prices({p.ticker for p in positions})
    except (ValueError, KeyError, IndexError) as error:
        st.error(f"Impossible de récupérer les cours actuels : {error}")
        return
    data = build_positions_table(positions, prices)
    df = pd.DataFrame(data)

    st.dataframe(
        df,
        hide_index=True,
    )

def render_charts(periode):
    positions = get_all_positions()
    tickers = get_all_tickers()
    if not positions:
        return
    period = periode
    try:
        prices = load_current_prices(tickers)
        history = build_portfolio_history(positions, tickers, period)
        st.plotly_chart(plot_portfolio_evolution(history), use_container_width=True)
        allocations = calculate_allocation(positions, prices)
        if allocations:
            st.plotly_chart(plot_allocation_pie(allocations), use_container_width=True)
        portfolio_comparison, benchmark_comparison = prepare_benchmark_comparison(
            positions,
            tickers,
            period,
            "^GSPC",
        )
        if not portfolio_comparison.empty and not benchmark_comparison.empty:
            figure = plot_vs_benchmark(
                portfolio_comparison,
                benchmark_comparison,
            )
            st.plotly_chart(figure, use_container_width=True)
        else:
            st.warning(
                "Données insuffisantes pour comparer le portefeuille au benchmark."
            )
    except (ValueError, KeyError, IndexError) as error:
        st.error(f"Impossible de construire les graphiques : {error}")


def render_period_filter(): 
    option = st.selectbox(
        "Choisir une période (1 mois, 6 mois, 1 an, tout)",
        ("1mo", "6mo", "1y", "max")
    )
    return option




    
if __name__ == "__main__":
    main()
