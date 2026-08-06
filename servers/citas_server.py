from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import Optional
import os
import psycopg
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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
        fecha_dt = fecha_dt.replace(tzinfo=ZoneInfo("America/Bogota"))
        async with await psycopg.AsyncConnection.connect(db) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO citas( negocio_id,cliente_numero,fecha_hora,servicio,descripcion)Values(%s,%s,%s,%s,%s)",
                    (
                        "negocio_demo",
                        cliente,
                        fecha_dt,
                        servicio,
                        nota_adicional,
                    ),  # TODO : negocio_id real cuando haya multi_negocio
                )
            await conn.commit()
        return (
            True,
            f"Cita agendada para {cliente} el {fecha_dt} (servicio={servicio}, nota={nota_adicional})",
        )
    except Exception as e:
        return False, f"Error al agendar cita: {e}"


@mcp.tool()
async def consultar_citas(cliente: str) -> tuple[bool, str]:
    """Consulta las citas activas (pendientes o confirmadas) de un cliente.
    Usar cuando el cliente pregunte por sus citas, por ejemplo:
    "¿cuándo es mi cita?", "¿tengo alguna cita agendada?".

    Args:
        cliente: identificador del cliente (número de WhatsApp)
    """

    try:
        async with await psycopg.AsyncConnection.connect(db) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT id, fecha_hora, servicio, estado "
                    "FROM citas WHERE cliente_numero = %s "
                    "AND estado IN ('pendiente','confirmada') ORDER BY fecha_hora",
                    (cliente,),
                )
                filas = await cur.fetchall()
                if not filas:
                    return True, "No se encontraron citas"
                texto = "Tus citas\n"
                for id_cita, fecha_hora, servicio, estado in filas:
                    texto += f"- (#{id_cita}) {fecha_hora} - {servicio} ({estado})\n"
                return True, texto

    except Exception as e:
        return False, f"error al consultar citas {e}"


@mcp.tool()
async def cancelar_cita(cliente: str, id: int) -> tuple[bool, str]:
    """Cancelar una cita de un cliente.
    Usar cuando el cliente pida cancelar citas, por ejemplo:
    "cancela mi cita por favor".

    Args:
        cliente: identificador del cliente (número de WhatsApp)
        id: identificador de la cita
    """

    try:
        async with await psycopg.AsyncConnection.connect(db) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "UPDATE citas SET estado = 'cancelada',actualizado_en = NOW() WHERE id = %s AND cliente_numero = %s",
                    (id, cliente),
                )
                if cur.rowcount == 0:
                    return False, "No se encontró esa cita (o no es tuya)"

            # Solo si sí se actualizó algo, haces commit
            await conn.commit()
            return True, f"Cita {id} cancelada exitosamente"

    except Exception as e:
        return False, f"Error al cancelar cita: {e}"


@mcp.tool()
async def consultar_disponibilidad(fecha: str) -> tuple[bool, str]:
    """Consulta los horarios disponibles de un día.
    Usar cuando el cliente pregunte por disponibilidad, por ejemplo:
    "¿tienen cupo mañana?", "¿qué horarios hay libres el viernes?".

    Args:
        fecha: día a consultar en formato ISO, ej: '2026-08-16'
    """
    slots = range(9, 18)
    inicio = datetime.fromisoformat(fecha)
    fin = inicio + timedelta(days=1)

    try:
        async with await psycopg.AsyncConnection.connect(db) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT  EXTRACT(HOUR FROM fecha_hora AT TIME ZONE 'America/Bogota') as hora "
                    "FROM citas "
                    "WHERE fecha_hora >= %s AND fecha_hora < %s "
                    "AND estado IN ('confirmada','pendiente') "
                    "AND negocio_id = 'negocio_demo'",
                    (inicio, fin),
                )
                filas = await cur.fetchall()
                horas_ocupadas = {int(fila[0]) for fila in filas}
                disponibles = []
                for hora in slots:
                    if hora not in horas_ocupadas:
                        disponibles.append(hora)
                if not disponibles:
                    return True, "No hay horarios disponibles"
                resultado = ", ".join(str(hora) for hora in disponibles)
                return True, f"Horarios disponibles : {resultado} "
    except Exception as e:
        return False, f"Error consultando disponibilidad {e}"


if __name__ == "__main__":
    mcp.run()
