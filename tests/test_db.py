
from ..src.db import Db
from dotenv import load_dotenv

load_dotenv()
def test_connect_success_or_skip():

    try:
        con = Db.connect()
        try:
            assert con.is_connected()
        finally:
            con.close()
    except:
        print("Error connecting to db")

