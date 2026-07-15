from dotenv import load_dotenv
from src.domain.graph import crear_grafo
from src.adapters.conexion_ia.openai_adapter import OpenAIAdapter

load_dotenv()

if __name__ == "__main__":
    adaptador = OpenAIAdapter()
    grafo = crear_grafo(adaptador)
    result = grafo.invoke({"input_usuario": "Hola como estas ?"})
    print(result)
