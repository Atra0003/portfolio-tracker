from dataclasses import dataclass
from datetime import date, datetime
from src.market_data import get_price_history
#from src.database import get_all_positions
import pandas as pd 

@dataclass
class Position:
    ticker: str
    quantite: float
    prix_achat: float
    date_achat: date
    type_position : str
    id: int | None = None  # None tant que pas encore en base

    def __post_init__(self):
        # Validation à la création
        if self.quantite <= 0:
            raise ValueError("La quantité doit être positive")
        if self.prix_achat <= 0:
            raise ValueError("Le prix d'achat doit être positif")
        if not self.ticker:
            raise ValueError("Le ticker ne peut pas être vide")
        if self.type_position != "achat" and self.type_position != "vente":
            raise ValueError("La type position ne peut être que achat ou vente")


def calculate_position_value(position, current_price):
    return position.quantite * current_price

def calculate_gain_loss(position, current_price) : 
    cout_total = position.quantite * position.prix_achat
    current_value = calculate_position_value(position, current_price)
    gain_perte = current_value - cout_total
    percent = gain_perte / cout_total
    return (gain_perte, percent) 

def calculate_portfolio_summary(positions : list[Position], prices):
    current_value = 0
    gain_perte = 0
    cout_total = 0
    for p in positions:
        current_price = prices[p.ticker]
        current_value += calculate_position_value(p, current_price)
        gain_perte += calculate_gain_loss(p, current_price)[0]
        cout_total += p.quantite * p.prix_achat
    gain_perte_pct = gain_perte / cout_total

    return {"current_value" : float(current_value), "gain_perte": float(gain_perte), "gain_perte_pct" : float(gain_perte_pct)}



def calculate_allocation(positions, prices):
    # prices := dictionnaire {ticker: prix_actuel},
    if len(positions) == 0:
        return {}
    valeurs_par_ticker = {}
    total_value = 0
    portfolio_summary = calculate_portfolio_summary(positions, prices)
    total_value = portfolio_summary["current_value"]
    for p in positions:
        current_price = prices[p.ticker]
        current_value = calculate_position_value(p, current_price)
        if p.ticker not in valeurs_par_ticker:
            valeurs_par_ticker[p.ticker] = current_value
        else: 
            valeurs_par_ticker[p.ticker] += current_value
        
    allocations = {}
    for ticker, value in valeurs_par_ticker.items():
        allocations[ticker] = (value/total_value)*100
    return allocations

def calculate_quantite(positions, ticker, date):
    """
    calcule la quantité d'un actif (ticker) dans tout les positions jusqu'a une date donnée
    """
    quantite = 0
    for p in positions:
        d = datetime.strptime(p.date_achat, "%Y-%m-%d").date()
        if d <= date and p.ticker == ticker:
            if p.type_position == "achat":
                quantite += p.quantite
            else: 
                quantite -= p.quantite
    return quantite

def build_portfolio_history(positions, tickers, periode):
    """
    concevoir l'historique du portfolio sur une période
    retourne un dictionnaire[date] = quantité total
    """
    df = []
    for t in tickers: 
        p_r = get_price_history(t, periode)
        p_r = p_r.rename(t)
        df.append(p_r)
    df = pd.concat(df, axis=1)
    result = {}
    for index, row in df.iterrows():
        #arriver a avoir la quantité en fonction du ticker et la dateclear
        v = 0
        for t in row.items():
            q = calculate_quantite(positions, t[0], index.date()) # calculer la quantité
            v += q * t[1] # calcule la valeur total du portfolio
        result[index.date()] = v
    return result


def prepare_benchmark_comparison(positions, tickers, periode, benchmark_ticker):
    #Péparation du dictionnaire en une serie pour appliquer la base 100
    dico = pd.Series(build_portfolio_history(positions, tickers, periode))
    dico = (dico / dico.iloc[0]) * 100

    #Application de la base 100 sur le data frame
    benchmark = get_price_history(benchmark_ticker, periode)
    benchmark = (benchmark / benchmark.iloc[0]) * 100 

    return [dico , benchmark]


        
        

