from src.use_cases.procesar_mensaje_entrante import ProcesarMensajeEntrante
from fastapi import FastAPI, Query, HTTPException, Request, Depends
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()


def get_procesador():
    raise RuntimeError("Debe ser sobrescrito en main.py")


@app.get("/conector")
async def verificar_token(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
):
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    if hub_verify_token != verify_token:
        raise HTTPException(status_code=403, detail="Token Invalido")
    return PlainTextResponse(hub_challenge)


@app.post("/conector")
async def recibir_mensaje(
    request: Request, caso_uso: ProcesarMensajeEntrante = Depends(get_procesador)
):
    data = await request.json()
    ##print("Datos recibidos:", data)
    # Aca se decide que hacer con el mensaje entrante, se delega al caso de uso
    entry = data.get("entry", [])
    if not entry:
        return {"info": "sin entry"}

    changes = entry[0].get("changes", [])
    if not changes:
        return {"info": "sin changes"}

    value = changes[0].get("value", {})

    if "messages" in value:
        mensaje = value["messages"][0]
        body = mensaje.get("text", {}).get("body")
        enviador = mensaje.get("from")
        # delegar al caso de uso
        await caso_uso.ejecutar(body, enviador)
        return {"status": "ok"}

    if "statuses" in value:
        status = value["statuses"][0].get("status")
        return {"status": status}

    return {"info": "evento no reconocido"}
