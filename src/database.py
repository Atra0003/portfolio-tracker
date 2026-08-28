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