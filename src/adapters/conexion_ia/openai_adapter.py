from src.domain.ports.generador_respuesta import Generador
from openai import OpenAI


class OpenAIAdapter(Generador):
    def __init__(self):
        self.client = OpenAI()

    def generar_respuesta(self, mensajes: list) -> str:
        mensaje_openai = []
        for msg in mensajes:
            if msg.type == "human":
                role = "user"
            elif msg.type == "ai":
                role = "assistant"
            elif msg.type == "system":
                role = "system"
            else:
                role = "user"

            mensaje_openai.append({"role": role, "content": msg.content})

        ##Insertar el mensaje del rol del sistema al inicio de la lista de mensajes
        rol_system = {
            "role": "system",
            "content": "Eres un asistente de atención al cliente amable y conciso.",
        }
        mensaje_openai.insert(0, rol_system)

        respuesta = self.client.chat.completions.create(
            model="gpt-4o-mini", messages=mensaje_openai
        )
        return respuesta.choices[0].message.content


if __name__ == "__main__":
    from dotenv import load_dotenv
    from langchain_core.messages import HumanMessage

    load_dotenv()
    adapter = OpenAIAdapter()
    salida = adapter.generar_respuesta([HumanMessage(content="Hola, ¿cómo estás?")])
    print(salida)
