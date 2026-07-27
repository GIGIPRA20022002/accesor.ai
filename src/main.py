from dotenv import load_dotenv
from src.domain.graph import crear_grafo
from src.adapters.conexion_ia.openai_adapter import OpenAIAdapter
from src.use_cases.procesar_mensaje_entrante import ProcesarMensajeEntrante
from src.adapters.wpp.enviador_adapter import WppEnviadorAdapter
from src.adapters.wpp.receptor_adapter import app, get_procesador

load_dotenv()

adaptador = OpenAIAdapter()
grafo = crear_grafo(adaptador)
enviador = WppEnviadorAdapter()
caso_uso = ProcesarMensajeEntrante(grafo, enviador)
app.dependency_overrides[get_procesador] = lambda: caso_uso
