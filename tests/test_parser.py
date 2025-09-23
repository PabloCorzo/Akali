from src.parser import Parser

def test_encryption():
    s = "test1"
    encrypted_value = "1b4f0e9851971998e732078544c96b36c3d01cedf7caa332359d6f1d83567014"
    parser = Parser()
    encrypted_value_2 = parser.hashPassword(s)

def test_encryption2():
    s = "test2"
    encrypted_value = "60303ae22b998861bce3b28f33eec1be758a213c86c93c076dbe9f558c11c752"
    parser = Parser()
    encrypted_value_2 = parser.hashPassword(s)
    assert encrypted_value == encrypted_value_2
test_encryption()
test_encryption2()