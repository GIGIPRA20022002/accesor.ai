import asyncio, sys
from dotenv import load_dotenv
load_dotenv()
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from servers.citas_server import consultar_citas, cancelar_cita

async def main():
    # 1. consultar para ver el id
    print(await consultar_citas(cliente="573218109192"))
    # 2. cancelar (pon el id que viste arriba, ej: 1)
    print(await cancelar_cita(cliente="573218109192", id=1))
    # 3. consultar de nuevo: la cita cancelada ya NO debe aparecer
    print(await consultar_citas(cliente="573218109192"))

asyncio.run(main())