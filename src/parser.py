import hashlib


class Parser:

    def __init__(self):
        pass
    
    def hashPassword(self,password : str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    parser = Parser()
    print(parser.hashPassword(input("Introduce password:\n")))
