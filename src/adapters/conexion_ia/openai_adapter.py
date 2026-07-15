from src.domain.ports.generador_respuesta import Generador
from openai import OpenAI


class OpenAIAdapter(Generador):
    def __init__(self):
        self.client = OpenAI()

    def generar_respuesta(self, mensaje: str) -> str:
        respuesta = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente de atención al cliente amable y conciso.",
                },
                {"role": "user", "content": mensaje},
            ],
        )
        return respuesta.choices[0].message.content


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    adapter = OpenAIAdapter()
    salida = adapter.generar_respuesta("Hola, ¿cómo estás?")
    print(salida)
