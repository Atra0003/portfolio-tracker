from datetime import date

import pytest

from src import database
from src.portfolio import Position


@pytest.fixture(autouse=True)
def temporary_database(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "data" / "portfolio.db")
    database.init_db()


def test_init_db_creates_parent_directory_and_empty_table():
    assert database.DB_PATH.exists()
    assert database.get_all_positions() == []


def test_add_and_get_position():
    database.add_position(Position(" aapl ", 2, 100, date(2025, 1, 1), "achat"))
    positions = database.get_all_positions()

    assert len(positions) == 1
    assert positions[0].ticker == "AAPL"
    assert positions[0].quantite == 2
    assert positions[0].date_achat == "2025-01-01"
    assert positions[0].id is not None


def test_update_position():
    database.add_position(Position("AAPL", 1, 100, date(2025, 1, 1), "achat"))
    position = database.get_all_positions()[0]
    position.quantite = 3
    position.prix_achat = 120
    database.update_position(position)

    updated = database.get_all_positions()[0]
    assert updated.quantite == 3
    assert updated.prix_achat == 120


def test_delete_position():
    database.add_position(Position("AAPL", 1, 100, date.today(), "achat"))
    position_id = database.get_all_positions()[0].id
    database.delete_position(position_id)
    assert database.get_all_positions() == []


def test_delete_all_positions():
    database.add_position(Position("AAPL", 1, 100, date.today(), "achat"))
    database.add_position(Position("MSFT", 2, 200, date.today(), "achat"))
    database.delete_all_position()
    assert database.get_all_positions() == []


def test_get_all_tickers_returns_unique_values_in_insertion_order():
    database.add_position(Position("AAPL", 1, 100, date.today(), "achat"))
    database.add_position(Position("AAPL", 2, 110, date.today(), "achat"))
    database.add_position(Position("MSFT", 1, 200, date.today(), "achat"))
    assert database.get_all_tickers() == ["AAPL", "MSFT"]

