from typing import Iterable, Optional
from .movie import Movie
from .films.app.db import MySQLConnection
from .db import Db

class MovieRepository:
    """
    Encapsulates operations on the 'peliculas' table.
    """
    def __init__(self, db: MySQLConnection) -> None:
        self._db = Db.connect()

    def insert(self, title: str, director: Optional[str], actors: Optional[str], synopsis: Optional[str]) -> Movie:
        sql = """
            INSERT INTO user_films (title, director, actors, synopsis)
            VALUES (%s, %s, %s, %s)
        """
        conn = self._db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (title, director, actors, synopsis))
                conn.commit()
                new_id = cur.lastrowid
            return Movie(id=new_id, title=title, director=director, actors=actors, synopsis=synopsis)
        finally:
            conn.close()

    def list_all(self) -> Iterable[Movie]:
        sql = "SELECT id, title, director, actors, synopsis FROM peliculas ORDER BY id DESC"
        conn = self._db.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                return [
                    Movie(id=r[0], title=r[1], director=r[2], actors=r[3], synopsis=r[4])
                    for r in rows
                ]
        finally:
            conn.close()
