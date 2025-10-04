from unittest.mock import Mock
import pytest
from src import db_repository as repo

# -----------------
# Utilidad de mocks
# -----------------
def make_mocks():
    cursor = Mock()
    connection = Mock()
    connection.cursor.return_value = cursor
    return connection, cursor


# ---------------------------------------
# filter_movies: título + rango + orden/lim
# ---------------------------------------
def test_filter_movies_title_year_range_sort_limit(monkeypatch):
    connection, cursor = make_mocks()
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    # Respuesta simulada
    rows = [
        {"id": 1, "title": "Matrix Reloaded", "year": 2003, "genre": "Sci-Fi", "director": "Wachowski", "rating": 7.2, "language": "en", "created_at": "2024-01-01 00:00:00"}
    ]
    cursor.fetchall.return_value = rows

    result = repo.filter_movies(
        filters={"title": "Matrix", "year_min": 2000, "year_max": 2020},
        db="akali_movies",
        sort_by="rating",
        sort_dir="desc",
        limit=10,
        offset=20,
    )

    # Verifica ejecución con placeholders y orden seguro
    assert cursor.execute.call_count == 1
    sql, params = cursor.execute.call_args[0]
    s = " ".join(sql.split()).lower()
    assert "from akali_movies.movies m" in s
    assert "where" in s
    assert "m.title like %s" in s
    assert "m.year >=" in s and "m.year <=" in s
    assert "order by m.rating desc" in s
    assert "limit %s offset %s" in s

    # params: title like, year_min, year_max, limit, offset
    assert params[:-2] == ["%Matrix%", 2000, 2020]
    assert params[-2:] == [10, 20]
    assert result == rows


# -----------------------------------------------------
# filter_movies: género múltiple + director (sin actor)
# -----------------------------------------------------
def test_filter_movies_genre_list_and_director(monkeypatch):
    connection, cursor = make_mocks()
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    cursor.fetchall.return_value = []

    result = repo.filter_movies(
        filters={"genre": ["Action", "Sci-Fi"], "director": "Nolan"},
        db="akali_movies",
        sort_by="year",
        sort_dir="desc",
        limit=5,
        offset=0,
    )

    assert cursor.execute.call_count == 1
    sql, params = cursor.execute.call_args[0]
    s = " ".join(sql.split()).lower()
    # Sin joins de actor
    assert "left join akali_movies.movies_cast" not in s
    assert "left join akali_movies.persons" not in s
    # IN con 2 placeholders y director LIKE
    assert "m.genre in (%s, %s)" in s
    assert "m.director like %s" in s
    assert params[:3] == ["Action", "Sci-Fi", "%Nolan%"]
    assert params[-2:] == [5, 0]
    assert result == []


# ------------------------------------------
# filter_movies: actor activa los LEFT JOINs
# ------------------------------------------
def test_filter_movies_with_actor_adds_joins(monkeypatch):
    connection, cursor = make_mocks()
    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    cursor.fetchall.return_value = [{"id": 10, "title": "Speed", "year": 1994, "genre": "Action", "director": "De Bont", "rating": 7.3, "language": "en", "created_at": "2024-01-01"}]

    result = repo.filter_movies(
        filters={"actor": "Keanu"},
        db="akali_movies",
        limit=3,
        offset=0,
    )

    assert cursor.execute.call_count == 1
    sql, params = cursor.execute.call_args[0]
    s = " ".join(sql.split()).lower()
    assert "left join akali_movies.movies_cast mc on mc.movie_id = m.id" in s
    assert "left join akali_movies.persons p on p.id = mc.person_id" in s
    assert "(p.name like %s)" in s
    assert params[:1] == ["%Keanu%"]
    assert params[-2:] == [3, 0]
    assert isinstance(result, list) and len(result) == 1


# ------------------------
# get_movie_by_id sencillo
# ------------------------
def test_get_movie_by_id(monkeypatch):
    connection, cursor = make_mocks()
    # Para cursor(dictionary=True)
    def cursor_with_dict(dictionary=False):
        return cursor
    connection.cursor.side_effect = cursor_with_dict

    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    row = {"id": 7, "title": "Interstellar", "year": 2014, "genre": "Sci-Fi", "director": "Christopher Nolan", "rating": 8.6, "language": "en", "created_at": "2024-01-01"}
    cursor.fetchone.return_value = row

    result = repo.get_movie_by_id(7, db="akali_movies")

    cursor.execute.assert_called_once()
    sql, params = cursor.execute.call_args[0]
    assert sql.strip().lower().startswith("select id, title")
    assert "from akali_movies.movies" in sql.lower()
    assert params == (7,)
    assert result == row


# -------------------------
# search_movies_text rápido
# -------------------------
def test_search_movies_text(monkeypatch):
    connection, cursor = make_mocks()
    def cursor_with_dict(dictionary=False):
        return cursor
    connection.cursor.side_effect = cursor_with_dict

    monkeypatch.setattr(repo, "Db", type("_D", (), {"connect": staticmethod(lambda: connection)}))

    rows = [{"id": 1, "title": "E.T.", "year": 1982, "genre": "Family", "director": "Steven Spielberg", "rating": 7.8, "language": "en", "created_at": "2024-01-01"}]
    cursor.fetchall.return_value = rows

    result = repo.search_movies_text("Spielberg", db="akali_movies", limit=2, offset=4)

    assert cursor.execute.call_count == 1
    sql, params = cursor.execute.call_args[0]
    s = " ".join(sql.split()).lower()
    assert "where title like %s or director like %s" in s
    assert "order by year desc" in s
    assert "limit %s offset %s" in s
    assert params == ("%Spielberg%", "%Spielberg%", 2, 4)
    assert result == rows