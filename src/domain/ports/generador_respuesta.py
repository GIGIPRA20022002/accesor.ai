from abc import ABC, abstractmethod


class Generador(ABC):
    @abstractmethod
    def generar_respuesta(self, mensaje: str) -> str:
        pass
