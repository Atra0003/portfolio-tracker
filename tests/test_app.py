from contextlib import nullcontext
from datetime import date
from unittest.mock import Mock

import pandas as pd

import app
from src.portfolio import Position


def test_load_current_prices(monkeypatch):
    monkeypatch.setattr(app, "get_current_price", lambda ticker: {"AAPL": 100, "MSFT": 200}[ticker])
    assert app.load_current_prices(["AAPL", "MSFT"]) == {"AAPL": 100, "MSFT": 200}


def test_render_period_filter(monkeypatch):
    monkeypatch.setattr(app.st, "selectbox", lambda *args, **kwargs: "6mo")
    assert app.render_period_filter() == "6mo"


def test_main_calls_each_section(monkeypatch):
    calls = []
    monkeypatch.setattr(app.st, "set_page_config", lambda **kwargs: calls.append("config"))
    monkeypatch.setattr(app, "init_db", lambda: calls.append("database"))
    monkeypatch.setattr(app, "render_period_filter", lambda: "1y")
    monkeypatch.setattr(app, "render_form", lambda: calls.append("form"))
    monkeypatch.setattr(app, "render_table", lambda: calls.append("table"))
    monkeypatch.setattr(app, "render_charts", lambda period: calls.append(("charts", period)))

    app.main()

    assert calls == ["config", "database", "form", "table", ("charts", "1y")]


def configure_form(monkeypatch, submitted=True, quantity=1):
    monkeypatch.setattr(app.st, "form", lambda *args, **kwargs: nullcontext())
    monkeypatch.setattr(app.st, "text_input", lambda *args, **kwargs: "AAPL")
    number_values = iter([quantity, 100])
    monkeypatch.setattr(app.st, "number_input", lambda *args, **kwargs: next(number_values))
    monkeypatch.setattr(app.st, "date_input", lambda *args, **kwargs: date(2025, 1, 1))
    monkeypatch.setattr(app.st, "selectbox", lambda *args, **kwargs: "achat")
    monkeypatch.setattr(app.st, "form_submit_button", lambda *args, **kwargs: submitted)


def test_render_form_adds_valid_position(monkeypatch):
    configure_form(monkeypatch)
    add = Mock()
    success = Mock()
    monkeypatch.setattr(app, "add_position", add)
    monkeypatch.setattr(app.st, "success", success)

    app.render_form()

    added = add.call_args.args[0]
    assert added.ticker == "AAPL"
    success.assert_called_once_with("Position ajoutée")


def test_render_form_does_nothing_when_not_submitted(monkeypatch):
    configure_form(monkeypatch, submitted=False)
    add = Mock()
    monkeypatch.setattr(app, "add_position", add)
    app.render_form()
    add.assert_not_called()


def test_render_form_displays_validation_error(monkeypatch):
    configure_form(monkeypatch, quantity=0)
    error = Mock()
    monkeypatch.setattr(app.st, "error", error)
    monkeypatch.setattr(app, "add_position", Mock())
    app.render_form()
    error.assert_called_once()
    assert "quantité" in error.call_args.args[0]


def test_render_table_handles_empty_portfolio(monkeypatch):
    info = Mock()
    monkeypatch.setattr(app, "get_all_positions", lambda: [])
    monkeypatch.setattr(app.st, "info", info)
    app.render_table()
    info.assert_called_once()


def test_render_table_displays_dataframe(monkeypatch):
    position = Position("AAPL", 1, 100, date.today(), "achat")
    dataframe = Mock()
    monkeypatch.setattr(app, "get_all_positions", lambda: [position])
    monkeypatch.setattr(app, "load_current_prices", lambda tickers: {"AAPL": 110})
    monkeypatch.setattr(app.st, "dataframe", dataframe)
    app.render_table()
    displayed = dataframe.call_args.args[0]
    assert displayed.loc[0, "prix_actuel"] == 110


def test_render_table_displays_market_error(monkeypatch):
    position = Position("BAD", 1, 100, date.today(), "achat")
    error = Mock()
    monkeypatch.setattr(app, "get_all_positions", lambda: [position])
    monkeypatch.setattr(app, "load_current_prices", Mock(side_effect=ValueError("indisponible")))
    monkeypatch.setattr(app.st, "error", error)
    app.render_table()
    assert "indisponible" in error.call_args.args[0]


def test_render_charts_handles_empty_portfolio(monkeypatch):
    chart = Mock()
    monkeypatch.setattr(app, "get_all_positions", lambda: [])
    monkeypatch.setattr(app, "get_all_tickers", lambda: [])
    monkeypatch.setattr(app.st, "plotly_chart", chart)
    app.render_charts("1mo")
    chart.assert_not_called()


def test_render_charts_displays_all_three_charts(monkeypatch):
    position = Position("AAPL", 1, 100, date.today(), "achat")
    comparison = pd.Series([100, 105])
    chart = Mock()
    monkeypatch.setattr(app, "get_all_positions", lambda: [position])
    monkeypatch.setattr(app, "get_all_tickers", lambda: ["AAPL"])
    monkeypatch.setattr(app, "load_current_prices", lambda tickers: {"AAPL": 110})
    monkeypatch.setattr(app, "build_portfolio_history", lambda *args: {date.today(): 110})
    monkeypatch.setattr(app, "prepare_benchmark_comparison", lambda *args: (comparison, comparison))
    monkeypatch.setattr(app.st, "plotly_chart", chart)
    app.render_charts("1mo")
    assert chart.call_count == 3


def test_render_charts_warns_when_comparison_is_empty(monkeypatch):
    position = Position("AAPL", 1, 100, date.today(), "achat")
    warning = Mock()
    monkeypatch.setattr(app, "get_all_positions", lambda: [position])
    monkeypatch.setattr(app, "get_all_tickers", lambda: ["AAPL"])
    monkeypatch.setattr(app, "load_current_prices", lambda tickers: {"AAPL": 110})
    monkeypatch.setattr(app, "build_portfolio_history", lambda *args: {date.today(): 110})
    monkeypatch.setattr(
        app,
        "prepare_benchmark_comparison",
        lambda *args: (pd.Series(dtype=float), pd.Series(dtype=float)),
    )
    monkeypatch.setattr(app.st, "plotly_chart", Mock())
    monkeypatch.setattr(app.st, "warning", warning)
    app.render_charts("1mo")
    warning.assert_called_once()


def test_render_charts_displays_calculation_error(monkeypatch):
    position = Position("AAPL", 1, 100, date.today(), "achat")
    error = Mock()
    monkeypatch.setattr(app, "get_all_positions", lambda: [position])
    monkeypatch.setattr(app, "get_all_tickers", lambda: ["AAPL"])
    monkeypatch.setattr(app, "load_current_prices", Mock(side_effect=KeyError("AAPL")))
    monkeypatch.setattr(app.st, "error", error)
    app.render_charts("1mo")
    assert "AAPL" in error.call_args.args[0]

