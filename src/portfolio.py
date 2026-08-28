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

    def get_ticker(self):
        return self.ticker

    def get_quantite(self):
        return self.quantite

    def get_prix_achat(self):
        return self.date_achat

    def get_date_achat(self):
        return self.date_achat