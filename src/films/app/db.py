import os
from mysql.connector import pooling
from dotenv import load_dotenv

class MySQLConnection:

    _pool: pooling.MySQLConnectionPool | None = None

    def __init__(self) -> None:
        load_dotenv()

        config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "films"),
            "charset": "utf8mb4",
            "use_unicode": True,
        }

        if MySQLConnection._pool is None:
            MySQLConnection._pool = pooling.MySQLConnectionPool(
                pool_name="films_pool",
                pool_size=5,
                **config
            )

    def get_connection(self):
        if MySQLConnection._pool is None:
            raise RuntimeError("Connection pool not initialized")
        return MySQLConnection._pool.get_connection()
