from unittest.mock import Mock
import pytest

from src import db_repository as repo


def make_mocks():
    # Create mock connection and cursor with the methods used
    cursor = Mock()
    connection = Mock()
    connection.cursor.return_value = cursor
    return connection, cursor


def dict_cursor(connection, cursor):
    # Ensure connection.cursor(dictionary=True) returns our cursor
    def _cursor(dictionary=False):
        return cursor
    connection.cursor.side_effect = _cursor


def test_selectAll_executes_and_returns_rows(monkeypatch):
    connection, cursor = make_mocks()
    dict_cursor(connection, cursor)
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    rows = [{"id": 1, "title": "A"}, {"id": 2, "title": "B"}]
    cursor.fetchall.return_value = rows

    result = repo.selectAll("akali.movies")

    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][0].strip() == "SELECT * FROM akali.movies"
    assert result == rows
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_delete_executes_and_commits(monkeypatch):
    connection, cursor = make_mocks()
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    repo.delete(42, tb="akali_hobby.hobby")

    cursor.execute.assert_called_once()
    sql, params = cursor.execute.call_args[0]
    assert sql == "DELETE FROM akali_hobby.hobby WHERE id = %s"
    assert params == (42,)
    connection.commit.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_fetchQuery_one_and_all(monkeypatch):
    connection, cursor = make_mocks()
    dict_cursor(connection, cursor)
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    # one
    cursor.fetchone.return_value = {"id": 1}
    res_one = repo.fetchQuery("SELECT 1", type="one")
    assert res_one == {"id": 1}
    # all
    cursor.fetchall.return_value = [{"id": 1}, {"id": 2}]
    res_all = repo.fetchQuery("SELECT * FROM akali.movies", type="all")
    assert res_all == [{"id": 1}, {"id": 2}]

    assert cursor.execute.call_count == 2
    cursor.close.assert_called()
    connection.close.assert_called()


def test_get_movie_by_id_builds_query_and_params(monkeypatch):
    connection, cursor = make_mocks()
    dict_cursor(connection, cursor)
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    row = {"id": 7, "title": "Seven"}
    cursor.fetchone.return_value = row

    res = repo.get_movie_by_id(7, db="akali")

    sql, params = cursor.execute.call_args[0]
    assert "FROM akali.movies" in sql
    assert "WHERE id = %s" in sql
    assert params == (7,)
    assert res == row


def test_filter_movies_builds_sql_params_and_order(monkeypatch):
    connection, cursor = make_mocks()
    dict_cursor(connection, cursor)
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    cursor.fetchall.return_value = []

    filters = {
        "title": "Star",
        "year_min": 2000,
        "year_max": 2010,
        "genre": ["Sci-Fi", "Action"],
        "rating_min": 7.5,
        "language": "EN",
    }

    repo.filter_movies(filters, db="akali", limit=10, offset=5, sort_by="year", sort_dir="desc")

    sql, params = cursor.execute.call_args[0]
    # No join expected (no actor)
    assert "LEFT JOIN" not in sql
    assert "FROM akali.movies m" in sql
    # ORDER BY
    assert "ORDER BY m.year DESC" in sql
    # LIMIT/OFFSET placeholders are added
    assert "LIMIT %s OFFSET %s" in sql

    # Params order must match filters then pagination
    expected_params = ["%Star%", 2000, 2010, "Sci-Fi", "Action", 7.5, "EN", 10, 5]
    assert params == expected_params


def test_filter_movies_with_actor_adds_join_and_param(monkeypatch):
    connection, cursor = make_mocks()
    dict_cursor(connection, cursor)
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    cursor.fetchall.return_value = []

    filters = {"actor": "Ford"}

    repo.filter_movies(filters, db="akali", limit=20, offset=0)

    sql, params = cursor.execute.call_args[0]
    assert "LEFT JOIN akali.movies_cast mc ON mc.movie_id = m.id" in sql
    assert "LEFT JOIN akali.persons p ON p.id = mc.person_id" in sql
    assert params[0] == "%Ford%"
    assert params[-2:] == [20, 0]


def test_search_movies_text_builds_like_and_pagination(monkeypatch):
    connection, cursor = make_mocks()
    dict_cursor(connection, cursor)
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    cursor.fetchall.return_value = []

    res = repo.search_movies_text("Nolan", db="akali", limit=3, offset=6)

    sql, params = cursor.execute.call_args[0]
    assert "FROM akali.movies" in sql
    assert "WHERE title LIKE %s OR director LIKE %s" in sql
    assert "ORDER BY year DESC" in sql
    assert "LIMIT %s OFFSET %s" in sql
    assert params == ("%Nolan%", "%Nolan%", 3, 6)
    assert res == []
