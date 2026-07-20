from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import Optional

##Crear el servivor FastMCP
mcp = FastMCP("CitasServer")


##Declarar una tool
@mcp.tool()
def agendar_cita(
    fecha_hora: str,
    cliente: str,
    servicio: Optional[str] = None,
    nota_adicional: Optional[str] = None,
) -> tuple[bool, str]:
    """
    Agenda una cita para un cliente del negocio.
    Usar cuando el cliente haya confirmado fecha y hora.

    Args:
        fecha_hora: fecha y hora en formato ISO 8601, ej: '2026-07-20T15:00:00'
        cliente: identificador del cliente (número de WhatsApp)
        servicio: servicio solicitado (opcional)
        nota_adicional: nota adicional sobre la cita (opcional)
    """

    try:
        fecha_dt = datetime.fromisoformat(fecha_hora)
        return (
            True,
            f"Cita agendada para {cliente} el {fecha_dt} (servicio={servicio}, nota={nota_adicional})",
        )
    except Exception as e:
        return False, f"Error al agendar cita: {e}"


if __name__ == "__main__":
    mcp.run()
