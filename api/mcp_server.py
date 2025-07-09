from dotenv import load_dotenv
from mcp_instance import mcp

load_dotenv()

import resources.checkIn_guests_resource
import resources.events_resource

if __name__ == "__main__":
    mcp.run(
        transport="stdio"
    )