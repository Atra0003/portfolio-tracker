from datetime import date

import pandas as pd

from src.charts import plot_allocation_pie, plot_portfolio_evolution, plot_vs_benchmark


def test_plot_portfolio_evolution():
    history = {date(2025, 1, 1): 100, date(2025, 1, 2): 120}
    figure = plot_portfolio_evolution(history)

    assert list(figure.data[0].x) == list(history.keys())
    assert list(figure.data[0].y) == [100, 120]
    assert figure.layout.title.text == "Évolution des valeurs par date"
    assert figure.layout.xaxis.tickformat == "%d/%m/%Y"


def test_plot_allocation_pie():
    figure = plot_allocation_pie({"AAPL": 60, "MSFT": 40})
    assert list(figure.data[0].labels) == ["AAPL", "MSFT"]
    assert list(figure.data[0].values) == [60, 40]


def test_plot_vs_benchmark():
    index = pd.to_datetime(["2025-01-01", "2025-01-02"])
    portfolio = pd.Series([100, 110], index=index)
    benchmark = pd.Series([100, 105], index=index)
    figure = plot_vs_benchmark(portfolio, benchmark)

    assert len(figure.data) == 2
    assert figure.data[0].name == "portfolio"
    assert figure.data[1].name == "benchmark"
    assert list(figure.data[0].y) == [100, 110]
    assert list(figure.data[1].y) == [100, 105]

