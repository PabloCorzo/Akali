from mysql.connector import Error
from src.model.models import Model
from src.db import Db


# def insert(model: Model, tb: str):
#     try:
#         connection = Db.connect()
#         cursor = connection.cursor()
#         sql_query = f"""
#                     INSERT INTO {tb} (name, user_id, satisfaction_level, hability, time)
#                     VALUES (%s, %s, %s, %s, %s)
#                 """
#         cursor.execute(sql_query, model.to_tuple())
#         connection.commit()
#         cursor.close()
#         connection.close()
#     except Error as e:
#         raise e


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
    Consulta y devuelve todas las filas de una tbala' de la base de datos akali.
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

def createUser(username : str, password :str, mail : str):
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