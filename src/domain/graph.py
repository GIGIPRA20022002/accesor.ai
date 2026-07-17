from src.domain.ports.generador_respuesta import Generador
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages : Annotated[list,add_messages]


def crear_nodo(generador: Generador):
    def generar_respuesta(state: State):
        mensaje = state["messages"]
        texto = generador.generar_respuesta(mensaje)
        return {"messages": [texto]}

    return generar_respuesta


def crear_grafo(generador: Generador):
    builder = StateGraph(State)
    builder.add_node("generar_respuesta", crear_nodo(generador))
    builder.add_edge(START, "generar_respuesta")
    builder.add_edge("generar_respuesta", END)
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)
