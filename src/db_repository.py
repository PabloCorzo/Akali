from mysql.connector import Error
from src.model.models import Model
from src.db import Db

from typing import Any, Dict, List, Tuple, Optional



def delete(id: int, tb: str):
    try:
        connection = Db.connect()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {tb} WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()

    except Error as e:
        raise e


def selectAll(tb) -> list:
    """
    Consulta y devuelve todas las filas de una tabla de la base de datos akali.
    Retorna una lista de diccionarios con las columnas como claves.
    """
    try:
        connection = Db.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {tb}")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        raise e


def fetchQuery(query: str, type: str = "one"):
    try:
        connection = Db.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        if type == 'one':
            rows = cursor.fetchone()
        elif type == 'all':
            rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        raise e


def createUser(username: str, password: str, mail: str):
    query = f'INSERT INTO users VALUES({username},{mail},{password}")'
    try:
        connection = Db.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        raise e


def _build_movie_filters(filters: Dict[str, Any]) -> Tuple[str, List[Any], bool]:
    """
    Construye WHERE + params para filtrar películas.
    Devuelve (clause_where, params, requiere_join_actor).
    """
    where = []
    params: List[Any] = []
    join_actor = False

    if (title := filters.get("title")):
        where.append("m.title LIKE %s")
        params.append(f"%{title}%")

    year = filters.get("year")
    year_min = filters.get("year_min")
    year_max = filters.get("year_max")
    if year is not None:
        where.append("m.year = %s")
        params.append(year)
    else:
        if year_min is not None:
            where.append("m.year >= %s")
            params.append(year_min)
        if year_max is not None:
            where.append("m.year <= %s")
            params.append(year_max)

    genre = filters.get("genre")
    if genre:
        if isinstance(genre, (list, tuple, set)):
            placeholders = ", ".join(["%s"] * len(genre))
            where.append(f"m.genre IN ({placeholders})")
            params.extend(list(genre))
        else:
            where.append("m.genre = %s")
            params.append(genre)

    if (director := filters.get("director")):
        where.append("m.director LIKE %s")
        params.append(f"%{director}%")

    if (actor := filters.get("actor")):
        join_actor = True
        where.append("(p.name LIKE %s)")
        params.append(f"%{actor}%")

    if (rmin := filters.get("rating_min")) is not None:
        where.append("m.rating >= %s")
        params.append(rmin)
    if (rmax := filters.get("rating_max")) is not None:
        where.append("m.rating <= %s")
        params.append(rmax)

    if (lang := filters.get("language")):
        where.append("m.language = %s")
        params.append(lang)

    clause = ("WHERE " + " AND ".join(where)) if where else ""
    return clause, params, join_actor


def _safe_order_by(sort_by: Optional[str], sort_dir: Optional[str]) -> str:
    """
    ORDER BY seguro. Campos permitidos: title, year, rating, created_at.
    """
    allowed = {
        "title": "m.title",
        "year": "m.year",
        "rating": "m.rating",
        "created_at": "m.created_at",
    }
    col = allowed.get((sort_by or "").lower())
    if not col:
        return ""
    direction = "DESC" if (sort_dir or "").lower() == "desc" else "ASC"
    return f" ORDER BY {col} {direction} "


def filter_movies(
        filters: Dict[str, Any],
        db: str = "akali",  # <-- cambiado
        limit: int = 50,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_dir: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Devuelve películas como lista de dicts desde {db}.movies.
    """
    try:
        connection = Db.connect()
        cursor = connection.cursor(dictionary=True)

        where, params, join_actor = _build_movie_filters(filters)

        join_sql = (
            f"LEFT JOIN {db}.movies_cast mc ON mc.movie_id = m.id "
            f"LEFT JOIN {db}.persons p ON p.id = mc.person_id "
            if join_actor else ""
        )

        base_sql = f"""
            SELECT
                m.id, m.title, m.year, m.genre, m.director, m.rating, m.language, m.created_at
            FROM {db}.movies m
            {join_sql}
        """

        order_by = _safe_order_by(sort_by, sort_dir)
        limit_clause = " LIMIT %s OFFSET %s "

        sql = (base_sql + " " + where + " " + order_by + limit_clause).strip()
        params = params + [int(limit), int(offset)]

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        raise e
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            connection.close()
        except Exception:
            pass


def get_movie_by_id(movie_id: int, db: str = "akali") -> Optional[Dict[str, Any]]:
    """Devuelve una película por id o None."""
    try:
        connection = Db.connect()
        cursor = connection.cursor(dictionary=True)
        sql = f"""
            SELECT id, title, year, genre, director, rating, language, created_at
            FROM {db}.movies
            WHERE id = %s
        """
        cursor.execute(sql, (movie_id,))
        row = cursor.fetchone()
        return row
    except Error as e:
        raise e
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            connection.close()
        except Exception:
            pass


def search_movies_text(
        text: str,
        db: str = "akali",
        limit: int = 50,
        offset: int = 0,
) -> List[Dict[str, Any]]:
    """Búsqueda rápida por título o director (LIKE)."""
    try:
        connection = Db.connect()
        cursor = connection.cursor(dictionary=True)
        like = f"%{text}%"
        sql = f"""
            SELECT id, title, year, genre, director, rating, language, created_at
            FROM {db}.movies
            WHERE title LIKE %s OR director LIKE %s
            ORDER BY year DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (like, like, int(limit), int(offset)))
        rows = cursor.fetchall()
        return rows
    except Error as e:
        raise e
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            connection.close()
        except Exception:
            pass
