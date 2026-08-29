from dataclasses import dataclass
from datetime import date

@dataclass
class Position:
    ticker: str
    quantite: float
    prix_achat: float
    date_achat: date
    id: int | None = None  # None tant que pas encore en base

    def __post_init__(self):
        # Validation à la création
        if self.quantite <= 0:
            raise ValueError("La quantité doit être positive")
        if self.prix_achat <= 0:
            raise ValueError("Le prix d'achat doit être positif")
        if not self.ticker:
            raise ValueError("Le ticker ne peut pas être vide")


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
        
        

