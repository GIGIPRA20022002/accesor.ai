import asyncio
from dotenv import load_dotenv
load_dotenv()
from servers.citas_server import agendar_cita
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    resultado = await agendar_cita(
        fecha_hora="2026-08-15T10:00:00",
        cliente="573218109192",
        servicio="corte de cabello",
        nota_adicional="prueba directa"
    )
    print(resultado)

asyncio.run(main())