from abc import ABC, abstractmethod


class EnviadorMensajes(ABC):
    @abstractmethod
    async def enviar_mensaje(self, destinatario: str, texto: str) -> tuple[bool, str]:
        pass
