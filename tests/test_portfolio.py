from datetime import date

import pandas as pd
import pytest

from src.portfolio import (
    Position,
    build_portfolio_history,
    build_positions_table,
    calculate_allocation,
    calculate_gain_loss,
    calculate_portfolio_summary,
    calculate_position_value,
    calculate_quantite,
    prepare_benchmark_comparison,
)


@pytest.fixture
def positions():
    return [
        Position(" aapl ", 2, 100, "2025-01-01", "achat"),
        Position("MSFT", 1, 200, date(2025, 1, 2), "achat"),
        Position("AAPL", 0.5, 120, "2025-01-03", "vente"),
    ]


def test_position_normalizes_ticker():
    position = Position(" aapl ", 1, 10, date.today(), "achat")
    assert position.ticker == "AAPL"


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"quantite": 0}, "quantité"),
        ({"prix_achat": 0}, "prix d'achat"),
        ({"ticker": "  "}, "ticker"),
        ({"type_position": "inconnu"}, "type position"),
    ],
)
def test_position_rejects_invalid_values(kwargs, message):
    values = {
        "ticker": "AAPL",
        "quantite": 1,
        "prix_achat": 10,
        "date_achat": date.today(),
        "type_position": "achat",
    }
    values.update(kwargs)
    with pytest.raises(ValueError, match=message):
        Position(**values)


def test_position_value_and_gain_loss():
    position = Position("AAPL", 2, 100, date.today(), "achat")
    assert calculate_position_value(position, 125) == 250
    assert calculate_gain_loss(position, 125) == (50, 0.25)


def test_portfolio_summary_handles_empty_portfolio():
    assert calculate_portfolio_summary([], {}) == {
        "current_value": 0.0,
        "gain_perte": 0.0,
        "gain_perte_pct": 0.0,
    }


def test_portfolio_summary_accounts_for_sales(positions):
    result = calculate_portfolio_summary(positions, {"AAPL": 110, "MSFT": 220})
    assert result == {
        "current_value": 385.0,
        "gain_perte": 45.0,
        "gain_perte_pct": 45 / 340,
    }


def test_portfolio_summary_handles_zero_net_cost():
    positions = [
        Position("AAPL", 1, 100, date.today(), "achat"),
        Position("AAPL", 1, 100, date.today(), "vente"),
    ]
    assert calculate_portfolio_summary(positions, {"AAPL": 110})["gain_perte_pct"] == 0


def test_allocation_groups_tickers_and_accounts_for_sales(positions):
    result = calculate_allocation(positions, {"AAPL": 110, "MSFT": 220})
    assert result["AAPL"] == pytest.approx(165 / 385 * 100)
    assert result["MSFT"] == pytest.approx(220 / 385 * 100)
    assert sum(result.values()) == pytest.approx(100)


def test_allocation_handles_empty_and_closed_positions():
    assert calculate_allocation([], {}) == {}
    closed = [
        Position("AAPL", 1, 100, date.today(), "achat"),
        Position("AAPL", 1, 110, date.today(), "vente"),
    ]
    assert calculate_allocation(closed, {"AAPL": 120}) == {}


def test_calculate_quantite_filters_by_ticker_date_and_type(positions):
    assert calculate_quantite(positions, "AAPL", date(2024, 12, 31)) == 0
    assert calculate_quantite(positions, "AAPL", date(2025, 1, 1)) == 2
    assert calculate_quantite(positions, "AAPL", date(2025, 1, 3)) == 1.5
    assert calculate_quantite(positions, "MSFT", date(2025, 1, 3)) == 1


def test_build_portfolio_history(monkeypatch, positions):
    index = pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"])
    histories = {
        "AAPL": pd.Series([100, 105, 110], index=index),
        "MSFT": pd.Series([200, 210, 220], index=index),
    }
    monkeypatch.setattr("src.portfolio.get_price_history", lambda ticker, period: histories[ticker])

    result = build_portfolio_history(positions, ["AAPL", "MSFT"], "1mo")

    assert result == {
        date(2025, 1, 1): 200,
        date(2025, 1, 2): 420,
        date(2025, 1, 3): 385,
    }


@pytest.mark.parametrize(("positions", "tickers"), [([], ["AAPL"]), ([object()], [])])
def test_build_portfolio_history_handles_missing_input(positions, tickers):
    assert build_portfolio_history(positions, tickers, "1mo") == {}


def test_prepare_benchmark_comparison_normalizes_to_base_100(monkeypatch, positions):
    history = {date(2025, 1, 1): 200, date(2025, 1, 2): 220}
    benchmark = pd.Series([400, 420], index=pd.to_datetime(["2025-01-01", "2025-01-02"]))
    monkeypatch.setattr("src.portfolio.build_portfolio_history", lambda *args: history)
    monkeypatch.setattr("src.portfolio.get_price_history", lambda *args: benchmark)

    portfolio_result, benchmark_result = prepare_benchmark_comparison(
        positions, ["AAPL"], "1mo", "^GSPC"
    )

    assert portfolio_result.tolist() == pytest.approx([100, 110])
    assert benchmark_result.tolist() == pytest.approx([100, 105])


@pytest.mark.parametrize("history", [{}, {date(2025, 1, 1): 0}])
def test_prepare_benchmark_comparison_handles_unusable_portfolio(monkeypatch, history):
    monkeypatch.setattr("src.portfolio.build_portfolio_history", lambda *args: history)
    portfolio_result, benchmark_result = prepare_benchmark_comparison([], [], "1mo", "^GSPC")
    assert portfolio_result.empty or portfolio_result.iloc[0] == 0
    assert benchmark_result.empty


def test_build_positions_table(positions):
    result = build_positions_table(positions, {"AAPL": 110, "MSFT": 220})
    assert result == {
        "tickers": ["AAPL", "MSFT", "AAPL"],
        "quantite": [2, 1, 0.5],
        "prix d'achat": [100, 200, 120],
        "prix_actuel": [110, 220, 110],
        "valeurs": [220, 220, 55],
        "gain_montant": [20, 20, -5],
        "gain_pourcentage": [0.1, 0.1, -5 / 60],
    }
