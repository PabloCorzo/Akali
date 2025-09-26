import os
import mysql.connector
from mysql.connector import Error
from src.model.models import Model

# Carga sencilla de variables: permite definir DB_* en el entorno del sistema
# o, si prefieres archivo, usa python-dotenv (opcional). Para mantener el
# repositorio simple, no auto-cargamos archivos aquí.

class Db:

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
                host=os.getenv("DB_HOST", "%"),
                port=int(os.getenv("DB_PORT", "3306")),
                user=os.getenv("DB_USER", "akali"),
                password=os.getenv("DB_PASSWORD", "desarrollo123"),
                database=os.getenv("DB_NAME", "akali_usuarios"),
            )
            return connection
        except Error as e:
            # Re-lanzamos para que los tests puedan capturarlo si falla la conexión
            raise e

    def insert(self, model: Model, db: str):
        try:
            connection = Db.connect()
            cursor = connection.cursor()
            sql_query = f"""
                        INSERT INTO {db}.hobby (name, user_id, satisfaction_level, hability, time)
                        VALUES (%s, %s, %s, %s, %s)
                    """
            cursor.execute(sql_query, model.to_tuple())
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            raise e


    def delete(self, id: int, db: str):
        try:
            connection = Db.connect()
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {db} WHERE id = %s", (id,))
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            raise e


    def selectAll(self) -> list:
        """
        Consulta y devuelve todas las filas de la tabla 'hobby' de la base de datos akali_hobby.
        Retorna una lista de diccionarios con las columnas como claves.
        """
        try:
            connection = Db.connect()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM hobby")
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Error as e:
            raise e

    def fetchQuery(self,query: str, type: str = "one"):
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





