from src.domain.ports.generador_respuesta import Generador
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    input_usuario: str
    respuesta: str


def crear_nodo(generador: Generador):
    def generar_respuesta(state: State):
        mensaje = state["input_usuario"]
        texto = generador.generar_respuesta(mensaje)
        return {"respuesta": texto}

    return generar_respuesta


def crear_grafo(generador: Generador):
    builder = StateGraph(State)
    builder.add_node("generar_respuesta", crear_nodo(generador))
    builder.add_edge(START, "generar_respuesta")
    builder.add_edge("generar_respuesta", END)
    return builder.compile()
