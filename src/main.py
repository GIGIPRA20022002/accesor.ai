from dotenv import load_dotenv
from src.domain.graph import crear_grafo
from src.adapters.conexion_ia.openai_adapter import OpenAIAdapter
from langchain_core.messages import HumanMessage

load_dotenv()

if __name__ == "__main__":
    thread_id = "juan1"

    adaptador = OpenAIAdapter()
    grafo = crear_grafo(adaptador)

    ##Primer Invoke##
    grafo.invoke(
        {
            "messages": [
                HumanMessage(content="hola ,como estas ,quiero agendar una cita")
            ]
        },
        {"configurable": {"thread_id": thread_id}},
    )

    ##Segundo Invoke
    respuesta = grafo.invoke(
        {"messages": [HumanMessage(content="Que te acabo de pedir ")]},
        {"configurable": {"thread_id": thread_id}},
    )

    # Acceder al contenido del último mensaje
    ultimo = respuesta["messages"][-1]
    print(ultimo.content)
