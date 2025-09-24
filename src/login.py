import hashlib


class Login:

    def __init__(self):
        pass
    
    def hashPassword(self,password : str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    connector = Login()
    print(connector.hashPassword(input("Introduce password:\n")))
