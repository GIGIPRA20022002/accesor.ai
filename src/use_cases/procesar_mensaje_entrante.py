from langchain_core.messages import HumanMessage
from src.domain.ports.enviador_mensajes import EnviadorMensajes


class ProcesarMensajeEntrante:
    def __init__(self, grafo, enviador: EnviadorMensajes):
        self.grafo = grafo
        self.enviador = enviador

    async def ejecutar(self, texto: str, numero: str) -> tuple[bool, str]:
        
        respuesta = await self.grafo.ainvoke(
            {"messages": [HumanMessage(content=texto)]},
            {"configurable": {"thread_id": numero}},
        )

        ultimo = respuesta["messages"][-1]
        
        resultado = await self.enviador.enviar_mensaje(numero, ultimo.content)
        return resultado
