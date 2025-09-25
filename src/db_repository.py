from mysql.connector import Error
from src.model.models import Model
from src.db import Db


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
    
def fetchQuery(self,query):
    try:
        connection = Db.connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        raise e
