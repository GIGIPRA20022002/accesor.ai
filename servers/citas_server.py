from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import Optional
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
db = os.getenv("DATABASE_URL")

##Crear el servivor FastMCP
mcp = FastMCP("CitasServer")


##Declarar una tool
@mcp.tool()
async def agendar_cita(
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
        async with await psycopg.AsyncConnection.connect(db) as conn :
            async with conn.cursor() as cur : 
                await cur.execute(
                    "INSERT INTO citas( negocio_id,cliente_numero,fecha_hora,servicio,descripcion)Values(%s,%s,%s,%s,%s)",
                    ("negocio_demo",cliente,fecha_dt,servicio,nota_adicional)#TODO : negocio_id real cuando haya multi_negocio
                )
            await conn.commit()
        return (
            True,
            f"Cita agendada para {cliente} el {fecha_dt} (servicio={servicio}, nota={nota_adicional})",
        )
    except Exception as e:
        return False, f"Error al agendar cita: {e}"


if __name__ == "__main__":
    mcp.run()
