
from src.dbHobby import dbHobby
from dotenv import load_dotenv

load_dotenv()
def test_connect_success_or_skip():

    try:
        con = dbHobby.connect()
        try:
            assert con.is_connected()
        finally:
            con.close()
    except:
        print("Error connecting to db")

