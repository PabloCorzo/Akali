import os
import mysql.connector
from mysql.connector import Error

from src.model.hobby import Hobby


# Carga sencilla de variables: permite definir DB_* en el entorno del sistema
# o, si prefieres archivo, usa python-dotenv (opcional). Para mantener el
# repositorio simple, no auto-cargamos archivos aquí.

class dbHobby:

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
                database=os.getenv("DB_NAME", "akali_hobby"),
            )
            return connection
        except Error as e:
            # Re-lanzamos para que los tests puedan capturarlo si falla la conexión
            raise e

    def insert(self, hobby: Hobby):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                        Insert into akali_hobby ((name, user_id, satisfaction_level, hability, time)
                               VALUES (%s, %s, %s, %s, %s)
                           """,
                           hobby.to_tuple())
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            raise e

    def selectAll(self)-> list:
        """
        Consulta y devuelve todas las filas de la tabla 'hobby' de la base de datos akali_hobby.
        Retorna una lista de diccionarios con las columnas como claves.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM hobby")
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Error as e:
            raise e


