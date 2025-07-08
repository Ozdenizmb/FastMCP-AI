from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.agents.llm_agent import LlmAgent

tools = [
    MCPToolset(
        connection_params = StdioServerParameters(
            command="python",
            args=["./apiCalls/mcp_server.py"]
        )
    )
]

root_agent = LlmAgent(
    name = "givergy_assistant",
    model = "gemini-2.5-flash-lite-preview-06-17",
    tools = tools,
    instruction = "You are determine which tool to call and extract parameters"
)