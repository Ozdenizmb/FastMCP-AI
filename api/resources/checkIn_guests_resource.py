import httpx, os
from dotenv import load_dotenv
from mcp_instance import mcp
from utils.auth import get_auth_headers

load_dotenv()

BASE_PATH = os.getenv('BASE_PATH')
EVENT_ID = os.getenv('EVENT_ID')
GUEST_ID = os.getenv('GUEST_ID')

@mcp.tool()
def check_payment_status(payment_id: str) -> dict:
    """Check the current payment status."""
    url = (
        f"{BASE_PATH}/checkin/v1/events/"
        f"{EVENT_ID}/guests/{GUEST_ID}/payments/{payment_id}"
    )
    headers = get_auth_headers()

    try:
        resp = httpx.get(url, headers=headers, timeout=10.0)
        resp.raise_for_status()
        return {"API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"Error: ": f"{e}"}