from abc import ABC, abstractmethod




class Model(ABC):
    """
    Interfaz para los modelos de creado de hobby y peliculas
    """

    @abstractmethod
    def to_tuple(self):
        #convierte un modelo a una tupla
        pass