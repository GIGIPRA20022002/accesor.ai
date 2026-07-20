from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class AgendadorCitas(ABC):
    @abstractmethod
    def agendar_cita(
        self,
        fecha_hora: datetime,
        cliente: str,
        servicio: Optional[str] = None,
        nota_adicional: Optional[str] = None,
    ) -> tuple[bool, str]:
        pass
