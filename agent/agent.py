from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters
from google.adk.agents.llm_agent import LlmAgent

tools = [
    MCPToolset(
        connection_params = StdioConnectionParams(
            server_params = StdioServerParameters(
                command = "python",
                args = ["./api/mcp_server.py"]
            ),
            timeout = 30
        )
    )
]

root_agent = LlmAgent(
    name = "givergy_assistant",
    model = "gemini-2.5-flash-lite-preview-06-17",
    tools = tools,
    instruction = "You are determine which tool to call and extract parameters"
)