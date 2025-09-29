from ..src.model.hobby import Hobby
# Verificar inicialización del objeto y sus métodos

def test__to_dict():
    h = Hobby(user_id=1, name="pintar", satisfaction_level=8, hability="intermedio", time=2.5, id=42)
    d = h._to_dict()
    assert d == {
        "id": 42,
        "user_id": 1,
        "name": "pintar",
        "satisfaction_level": 8,
        "hability": "intermedio",
        "time": 2.5,
    }


def test_creation_hobby_and_to_tuple():
    h = Hobby(user_id=7, name="leer", satisfaction_level=10, hability="alto", time=1.25)
    assert h.id is None
    assert h.user_id == 7
    assert h.name == "leer"
    assert h.satisfaction_level == 10
    assert h.hability == "alto"
    assert h.time == 1.25


    assert h.to_tuple() == (7, "leer", 10, "alto", 1.25)
