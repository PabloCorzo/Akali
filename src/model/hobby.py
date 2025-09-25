from .model import Model


class Hobby(Model):

    def __init__(self,user_id,name:str,satisfaction_level:int,hability,time:float,id = None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.satisfaction_level = satisfaction_level
        self.hability = hability
        self.time = time

    def to_tuple(self) -> tuple:
        return self.user_id, self.name, self.satisfaction_level, self.hability, self.time


    def _to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "satisfaction_level": self.satisfaction_level,
            "hability": self.hability,
            "time": self.time,
        }
