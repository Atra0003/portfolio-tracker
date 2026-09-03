from datetime import datetime
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def plot_portfolio_evolution(historique):
    "Permet d'avoir un raphique montrant l'évolution de la valeur totale de mon portefeuille dans le temps"
    dates = list(historique.keys())
    valeurs = np.array(list(historique.values()))

    fig = px.line(
        x=dates,
        y=valeurs,
        labels={"x": "Date", "y": "Valeur"},
        title="Évolution des valeurs par date",
    )
    fig.update_xaxes(
        tickformat="%d/%m/%Y",  # Format Jour/Mois/Année
        tickangle=45,  # Inclinaison à 45 degrés
    )
    return fig

def plot_allocation_pie(allocations):
    labels = list(allocations.keys())
    valeurs = list(allocations.values())

    fig = px.pie(values=valeurs, names=labels, color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

def  plot_vs_benchmark(portfolio_history, benchmark_history): 
    dates_P = portfolio_history.index
    valeurs_P = portfolio_history.values

    dates_B = benchmark_history.index
    valeurs_B = benchmark_history.values

    fig = go.Figure(
        data=[go.Scatter(x=dates_P, y=valeurs_P, mode='lines+markers', line=dict(color="blue"), name="portfolio"), go.Scatter(x=dates_B, y=valeurs_B, mode='lines+markers', line=dict(color="red"), name="benchmark")], 
        layout=go.Layout(title="plot_vs_benchmark"),
    )
    return fig
    #fig.show()