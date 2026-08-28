from src.portfolio import Position
import sqlite3


def init_db():
    connexion = sqlite3.connect('data/portfolio.db')
    cursor = connexion.cursor()

    table = '''CREATE TABLE IF NOT EXISTS portfolio
                (ticker TEXT, quantite REAL, prix_achat REAL, date_achat TEXT, ID INTEGER PRIMARY KEY)
                '''
    cursor.execute(table)
    #cursor.execute("INSERT INTO portfolio (ticker, quantite, prix_achat, date_achat) VALUES ('AAA', 10, 100, '2026-06-04')")
    connexion.commit()
    #cursor.execute("SELECT * FROM portfolio")
    #result = cursor.fetchall()
    #print(result)

    connexion.close()


def add_position(position):
    connexion = sqlite3.connect('data/portfolio.db')
    cursor = connexion.cursor()

    ticker = position.ticker
    quantite = position.quantite
    prix_achat = position.prix_achat
    date_achat = position.date_achat

    request = '''INSERT INTO portfolio (ticker, quantite, prix_achat, date_achat) VALUES (?, ?, ?, ?)'''
    cursor.execute(request, (ticker, quantite, prix_achat, date_achat))
    connexion.commit()
    #cursor.execute("SELECT * FROM portfolio")
    #result = cursor.fetchall()
    #print(result)
    connexion.close()

def get_all_positions():
    connexion = sqlite3.connect('data/portfolio.db')
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM portfolio")
    result = cursor.fetchall()
    list_position = []
    for position in result:
        ticker, quantite, prix_achat, date_achat, id = position
        p = Position(ticker, quantite, prix_achat, date_achat, id)
        list_position.append(p)
    return list_position
