from dotenv import load_dotenv
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import asyncio

load_dotenv()

async def get_agent():
    tools = [
        MCPToolset(
            connection_params = StdioServerParameters(
                command="python",
                args=["./apiCalls/mcp_server.py"]
            )
        )
    ]

    agent = LlmAgent(
        name = "givergy_assistant",
        model = "gemini-2.5-flash-lite-preview-06-17",
        tools = tools,
        instruction = "You are determine which tool to call and extract parameters"
    )

    return agent

async def main():
    agent= await get_agent()

    session_service = InMemorySessionService()

    session = await session_service.create_session(
        state = {},
        app_name = "mcp_givergy_app",
        user_id = "user_givergy"
    )

    print("Ctrl+C to exit")
    while True:
        try:
            query = input(">> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        content = types.Content(role= "user", parts= [types.Part(text=query)])

        runner = Runner(
            app_name= "mcp_givergy_app",
            agent= agent,
            session_service= session_service
        )

        response = runner.run_async(
            session_id= session.id,
            user_id= session.user_id,
            new_message= content
        )

        async for message in response:
            print(message)

if __name__ == "__main__":
    asyncio.run(main())