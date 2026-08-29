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


def add_position(p : Position):
    connexion = sqlite3.connect('data/portfolio.db')
    cursor = connexion.cursor()

    ticker = p.ticker
    quantite = p.quantite
    prix_achat = p.prix_achat
    date_achat = p.date_achat

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
    connexion.close()
    return list_position


def get_all_prices():
    connexion = sqlite3.connect('data/portfolio.db')
    cursor = connexion.cursor()
    request = '''SELECT prix_achat FROM portfolio'''
    cursor.execute(request)
    prices = cursor.fetchall()
    list_price = []
    for p in prices:
        list_price.append(p)
    connexion.close()
    return list_price


def delete_position(id : int):
    connexion = sqlite3.connect('data/portfolio.db')
    cursor = connexion.cursor()
    request = '''DELETE FROM portfolio WHERE id = ?'''
    cursor.execute(request, (id,))
    connexion.commit()
    connexion.close()


def delete_all_position():
    connexion = sqlite3.connect('data/portfolio.db')
    cursor = connexion.cursor()
    request = '''DELETE FROM portfolio'''
    cursor.execute(request)
    connexion.commit()
    connexion.close()


def update_position(p : Position):
    connexion = sqlite3.connect('data/portfolio.db')
    cursor = connexion.cursor()
    ticker = p.ticker
    quantite = p.quantite
    prix_achat = p.prix_achat
    date_achat = p.date_achat
    id = p.id
    request = '''UPDATE portfolio SET ticker = ?, quantite = ?, prix_achat = ?, date_achat = ? WHERE id = ?'''
    cursor.execute(request, (ticker, quantite, prix_achat, date_achat, id))
    connexion.commit()
    connexion.close()
