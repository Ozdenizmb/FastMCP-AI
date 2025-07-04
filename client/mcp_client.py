import asyncio
import re
from fastmcp import Client

MCP_URL = "http://localhost:8000/mcp/"
EVENT_ID = "35a77b4b-063f-11f0-91f9-62452ee26198"
GUEST_ID = "764e819d-0642-11f0-91f9-62452ee26198"

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

            m = re.search(r'payment\s+([0-9a-f\-]+)', user_input)
            if not m:
                print("❌ I don't understand. Can you repeat it?")
                continue

            payment_id = m.group(1)

            tool_call = await client.call_tool(
                "check_payment_status",
                {
                    "event_id": EVENT_ID,
                    "guest_id": GUEST_ID,
                    "payment_id": payment_id
                }
            )

            print(tool_call.data)

if __name__=="__main__":
    asyncio.run(main())