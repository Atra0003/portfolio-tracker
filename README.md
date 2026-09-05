# Portfolio Tracker

Application web réalisée avec Streamlit pour enregistrer des opérations d'achat et de vente, suivre la valeur d'un portefeuille et comparer ses performances à l'indice S&P 500.

Les cours et historiques de marché sont récupérés depuis Yahoo Finance avec `yfinance`. Les positions sont conservées localement dans une base de données SQLite.

## Fonctionnalités

- ajout d'opérations d'achat et de vente ;
- récupération des cours actuels ;
- tableau détaillé des positions et des gains ou pertes ;
- graphique d'évolution du portefeuille ;
- répartition du portefeuille par actif ;
- comparaison en base 100 avec le S&P 500 (`^GSPC`) ;
- sélection de la période d'affichage ;
- stockage local avec SQLite.

## Prérequis

- Python 3.10 ou une version plus récente ;
- `pip` ;
- une connexion Internet pour récupérer les données de marché.

Vérifier la version de Python :

```bash
python3 --version
```

Sous Windows, la commande peut être :

```powershell
py --version
```

## Installation

### Linux et macOS

Cloner le dépôt puis entrer dans son dossier :

```bash
git clone <URL_DU_DEPOT>
cd portfolio-tracker
```

Créer et activer un environnement virtuel :

```bash
python3 -m venv venv
source venv/bin/activate
```

Installer les dépendances :

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows avec PowerShell

```powershell
git clone <URL_DU_DEPOT>
cd portfolio-tracker
py -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell bloque l'activation de l'environnement virtuel, autoriser temporairement les scripts pour la session courante :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

## Lancement de l'application

Avec l'environnement virtuel activé :

```bash
streamlit run app.py
```

Streamlit affiche ensuite l'adresse locale de l'application, généralement :

```text
http://localhost:8501
```

Il est également possible de lancer directement l'exécutable de l'environnement virtuel sous Linux ou macOS :

```bash
venv/bin/streamlit run app.py
```

## Utilisation

1. Choisir la période des graphiques.
2. Saisir un ticker Yahoo Finance, par exemple `AAPL`, `MSFT` ou `TSLA`.
3. Indiquer la quantité, le prix et la date de l'opération.
4. Sélectionner `achat` ou `vente`.
5. Cliquer sur **Envoyer**.

Les tickers sont automatiquement nettoyés et convertis en majuscules. Un ticker doit être reconnu par Yahoo Finance pour que ses données puissent être affichées.

## Base de données

La base SQLite est créée automatiquement au premier lancement dans :

```text
data/portfolio.db
```

Aucune configuration de serveur de base de données n'est nécessaire.

## Tests

Exécuter tous les tests :

```bash
python -m pytest -q
```

Afficher le détail de chaque test :

```bash
python -m pytest -v
```

Les appels à Yahoo Finance sont simulés pendant les tests. La suite de tests n'utilise donc pas Internet et ne modifie pas la base de données réelle.

## Structure du projet

```text
portfolio-tracker/
├── app.py                 # Interface Streamlit
├── requirements.txt      # Dépendances Python
├── data/
│   └── portfolio.db      # Base SQLite créée automatiquement
├── src/
│   ├── charts.py         # Création des graphiques Plotly
│   ├── database.py       # Accès à SQLite
│   ├── market_data.py    # Accès aux données Yahoo Finance
│   └── portfolio.py      # Modèles et calculs du portefeuille
└── tests/                # Tests automatisés
```

## Résolution des problèmes courants

### `ModuleNotFoundError`

Vérifier que l'environnement virtuel est activé, puis réinstaller les dépendances :

```bash
python -m pip install -r requirements.txt
```

### Aucun cours disponible pour un ticker

- vérifier l'orthographe du ticker ;
- vérifier que le ticker existe sur Yahoo Finance ;
- vérifier la connexion Internet ;
- réessayer quelques instants plus tard si Yahoo Finance est temporairement indisponible.

### Le port 8501 est déjà utilisé

Lancer l'application sur un autre port :

```bash
streamlit run app.py --server.port 8502
```
