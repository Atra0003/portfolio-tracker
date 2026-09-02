from datetime import datetime
import numpy as np

import numpy as np
import plotly.express as px


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
    fig.show() 
    #return fig