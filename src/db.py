import os
import mysql.connector
from mysql.connector import Error

from src.model.hobby import Hobby
from src.model.model import Model


# Carga sencilla de variables: permite definir DB_* en el entorno del sistema
# o, si prefieres archivo, usa python-dotenv (opcional). Para mantener el
# repositorio simple, no auto-cargamos archivos aquí.

class db:

    @staticmethod
    def connect():
        """
        Local por el momento
        Devuelve una conexión a MySQL usando variables de entorno si están presentes.
        Archivo .env propio
        Variables soportadas (con valores por defecto):
          - DB_HOST (localhost)
          - DB_PORT (3306)
          - DB_USER (akali)
          - DB_PASSWORD (cadena vacía)
          - DB_NAME (akali_hobby)
        """
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "3306")),
                user=os.getenv("DB_USER", "akali"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "akali"),
            )
            return connection
        except Error as e:
            # Re-lanzamos para que los tests puedan capturarlo si falla la conexión
            raise e





