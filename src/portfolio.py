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
