from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage


async def crear_grafo():
    modelo = ChatOpenAI(model="gpt-4o-mini")
    client = MultiServerMCPClient(
        {
            "citas": {
                "command": "python",
                "args": ["servers/citas_server.py"],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    checkpointer = MemorySaver()
    agent = create_agent(modelo, tools, checkpointer=checkpointer)
    return agent


async def probar():
    grafo = await crear_grafo()
    respuesta = await grafo.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="agéndame una cita para mañana 10am, soy el cliente 573218109192, servicio corte de cabello"
                )
            ]
        },
        {"configurable": {"thread_id": "prueba1"}},
    )
    print(respuesta["messages"][-1].content)
