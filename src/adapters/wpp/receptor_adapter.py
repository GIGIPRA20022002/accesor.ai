from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from src.domain.graph import crear_grafo
from src.adapters.wpp.enviador_adapter import WppEnviadorAdapter
from src.use_cases.procesar_mensaje_entrante import ProcesarMensajeEntrante

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    grafo = await crear_grafo()
    enviador = WppEnviadorAdapter()
    app.state.caso_uso = ProcesarMensajeEntrante(grafo, enviador)
    yield


app = FastAPI(lifespan=lifespan)


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
async def recibir_mensaje(request: Request):
    data = await request.json()
    caso_uso = request.app.state.caso_uso
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
        numero = mensaje.get("from")
        # delegar al caso de uso
        await caso_uso.ejecutar(body, numero)
        return {"status": "ok"}

    if "statuses" in value:
        status = value["statuses"][0].get("status")
        return {"status": status}

    return {"info": "evento no reconocido"}
