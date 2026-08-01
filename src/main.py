from dotenv import load_dotenv
import sys, asyncio

load_dotenv()
from src.adapters.wpp.receptor_adapter import app

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())