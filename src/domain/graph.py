
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage


async def crear_grafo(checkpointer):
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
    
    agent = create_agent(modelo, tools, checkpointer=checkpointer)
    return agent



