import asyncio
import re
from fastmcp import Client
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
import json
import httpx

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
MCP_URL = os.getenv('MCP_URL')
EVENT_ID = os.getenv('EVENT_ID')
GUEST_ID = os.getenv('GUEST_ID')

DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_payment_status",
            "description": "Check the status of a payment using its payment ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "payment_id": {
                        "type": "string",
                        "description": "The UUID of the payment to check"
                    }
                },
                "required": ["payment_id"]
            }
        }
    }
]

async def ai_parse_prompt(prompt: str) -> dict:
    """Use AI to determine which tool to call and extract parameters"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324",
        "messages": [{"role": "user", "content": prompt}],
        "tools": TOOLS,
        "tool_choice": "auto"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            message = data["choices"][0]["message"]
            if "tool_calls" not in message or not message["tool_calls"]:
                return None
                
            tool_call = message["tool_calls"][0]
            return {
                "name": tool_call["function"]["name"],
                "args": json.loads(tool_call["function"]["arguments"])
            }
            
    except Exception as e:
        print(f"❌ DeepSeek API error: {e}")
        return None

async def main():
    async with Client(MCP_URL) as client:
        await client.call_tool("login")
        print("Ctrl+C to exit")
        while True:
            try:
                user_input = input(">> ")
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                break

            tool_call = await ai_parse_prompt(user_input)

            if not tool_call:
                print("❌ Couldn't determine action from your query")
                continue

            if tool_call["name"] == "check_payment_status":
                result  = await client.call_tool(
                    "check_payment_status",
                    {
                        "event_id": EVENT_ID,
                        "guest_id": GUEST_ID,
                        "payment_id": tool_call["args"]["payment_id"]
                    }
                )
                print(result.data)
            else:
                print(f"❌ Unsupported action: {tool_call['name']}")

if __name__=="__main__":
    asyncio.run(main())