from abc import ABC, abstractmethod


class Generador(ABC):
    @abstractmethod
    def generar_respuesta(self, mensajes: list) -> str:
        pass
