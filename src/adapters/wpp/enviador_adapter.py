from src.domain.ports.enviador_mensajes import EnviadorMensajes
import os
import httpx
from dotenv import load_dotenv
import asyncio


class WppEnviadorAdapter(EnviadorMensajes):
    def __init__(self):
        self.wpp_token = os.getenv("WHATSAPP_TOKEN")
        self.telefono_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.url = f"https://graph.facebook.com/v22.0/{self.telefono_id}/messages"

    async def enviar_mensaje(self, destinatario: str, texto: str) -> tuple[bool, str]:
        headers = {
            "Authorization": f"Bearer {self.wpp_token}",
            "Content-Type": "application/json",
        }
        data = {
            "messaging_product": "whatsapp",
            "to": destinatario,
            "type": "text",
            "text": {"body": texto},
        }
        try:
            async with httpx.AsyncClient() as client:
                respuesta = await client.post(self.url, headers=headers, json=data)
                ##print (respuesta.json())
                if respuesta.status_code == 200:
                    body = respuesta.json()
                    mensaje_id = body["messages"][0]["id"]
                    return True, mensaje_id
                else:
                    body = respuesta.json()
                    error_msg = None
                    if isinstance(body, dict) and "error" in body:
                        error_msg = body["error"].get("message")
                    return False, error_msg
        except Exception as e:
            return False, str(e)


if __name__ == "__main__":
    load_dotenv()
    adaptador = WppEnviadorAdapter()
    resultado = asyncio.run(
        adaptador.enviar_mensaje("573218109192", "hola desde mi bot")
    )
    print("Resultado", resultado)
