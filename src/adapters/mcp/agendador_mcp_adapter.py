from datetime import datetime
from typing import Optional
from src.domain.ports.agendador_citas import AgendadorCitas
import asyncio

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession


class AgendadorCitasMCPAdapter(AgendadorCitas):
    def agendar_cita(
        self,
        fecha_hora: datetime,
        cliente: str,
        servicio: Optional[str] = None,
        nota_adicional: Optional[str] = None,
    ) -> tuple[bool, str]:
        return asyncio.run(
            self.llamar_servidor(fecha_hora, cliente, servicio, nota_adicional)
        )

    async def llamar_servidor(
        self,
        fecha_hora: datetime,
        cliente: str,
        servicio: Optional[str] = None,
        nota_adicional: Optional[str] = None,
    ) -> tuple[bool, str]:
        ## 1. Parámetros para lanzar tu servidor MCP
        params = StdioServerParameters(
            command="python", args=["servers/citas_server.py"]
        )

        ## 2.Conectar el cliente stdio
        async with stdio_client(params) as (read, write):
            ## 3.Crear sesion
            async with ClientSession(read, write) as session:
                ## 4.Handshake inicial
                await session.initialize()
                ## 5.Llamar a la tool expuesta
                result = await session.call_tool(
                    "agendar_cita",
                    {
                        "fecha_hora": fecha_hora.isoformat(),
                        "cliente": cliente,
                        "servicio": servicio,
                        "nota_adicional": nota_adicional,
                    },
                )

                ##6.Retornar resultado
                datos_estructurados = result.structuredContent

                booleano_real = datos_estructurados['result'][0]
                string_limpio  = datos_estructurados['result'][1]
                return (booleano_real,string_limpio)

if __name__ == "__main__":
    adaptador = AgendadorCitasMCPAdapter()
    fecha = datetime(2026, 7, 20, 15, 0)
    cliente = "Juan Perez"
    servicio = "Corte de cabello"
    nota = "Por favor, que sea rápido."

    mensaje = adaptador.agendar_cita(fecha, cliente, servicio, nota)
    print("resultado:", mensaje)