from fastmcp import FastMCP
import httpx
from dotenv import load_dotenv
import os

mcp = FastMCP("GivergyCheckinBridge")

http_client = httpx.Client()

load_dotenv()
EVENT_ID = os.getenv('EVENT_ID')
GUEST_ID = os.getenv('GUEST_ID')

login_data = {"csrf_token": None, "cookies": None}

def _do_login() -> dict:
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    url = "http://localhost:8080/v1/localhost/auth/login"
    payload = {"username": username, "password": password, "version": 0}
    resp = http_client.post(url, json=payload, headers={"X-CSRF-Token": "FETCH"})
    resp.raise_for_status()

    csrf_token = resp.headers.get("X-CSRF-Token")
    cookies = resp.headers.get("Set-Cookie")

    if not csrf_token:
        raise RuntimeError("X-CSRF-Token header not found!")
    
    if not cookies:
        raise RuntimeError("Cookies header not found!")
    
    login_data["csrf_token"] = csrf_token
    login_data["cookies"] = cookies

    return login_data

@mcp.tool()
def check_payment_status(payment_id: str) -> dict:
    """Check the current payment status."""
    url = (
        f"http://localhost:8080/checkin/v1/events/"
        f"{EVENT_ID}/guests/{GUEST_ID}/payments/{payment_id}"
    )
    headers = {
        "X-CSRF-Token": login_data["csrf_token"],
        "Cookie": login_data["cookies"]
    }

    try:
        resp = httpx.get(url, headers=headers, timeout=10.0)
        resp.raise_for_status()
        return {"✅ API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"❌ Error: ": f"{e}"}

if __name__ == "__main__":
    _do_login()
    mcp.run(
        transport="stdio"
    )