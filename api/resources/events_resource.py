import httpx, os
from dotenv import load_dotenv
from mcp_instance import mcp
from utils.auth import get_auth_headers

load_dotenv()

BASE_PATH = os.getenv('BASE_PATH')
DOMAIN = os.getenv('DOMAIN')
EVENT_ID = os.getenv('EVENT_ID')
GUEST_ID = os.getenv('GUEST_ID')

@mcp.tool()
def getByIdJSON() -> dict:
    """It fetches the event information."""
    url = (
        f"{BASE_PATH}/v1/{DOMAIN}/events/"
        f"{EVENT_ID}?view=FULL"
    )
    headers = get_auth_headers()

    try:
        resp = httpx.get(url, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return {"API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"Error: ": f"{e}"}
    
@mcp.tool()
def updateJSON(changes: dict) -> dict:
    """
    Update specific fields of an event.

    This tool fetches the existing event data, applies the provided changes, and sends the updated event back to the backend.
    Only the fields provided in the 'changes' dictionary will be updated.
    
    Example input:
    {
        "name": "New Event Name",
        "startDate": "2025-07-10T18:00:00Z"
    }
    """

    url_get = (
        f"{BASE_PATH}/v1/{DOMAIN}/events/"
        f"{EVENT_ID}?view=FULL"
    )
    url_post = (
        f"{BASE_PATH}/v1/{DOMAIN}/events/"
        f"{EVENT_ID}"
    )
    headers = get_auth_headers()

    try:
        resp = httpx.get(url_get, headers=headers, timeout=30.0)
        resp.raise_for_status()
        current_event_data = resp.json()

        updated_data = current_event_data.copy()
        updated_data.update(changes)

        resp = httpx.post(url_post, json=updated_data, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return {"API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"Error: ": f"{e}"}

@mcp.tool()    
def getBySubUrlJSON(sub_url: str) -> dict:
    """
    Check if a subUrl maps to a valid event.

    Parameters:
    - sub_url: The subdomain path to check (e.g. "myevent2025")

    Returns:
    - {"exists": True} if the subUrl maps to an event.
    - {"Error": "..."} if not found or an error occurred.
    """

    url_get = (
        f"{BASE_PATH}/v1/{DOMAIN}/events/"
        f"sites?subUrl={sub_url.strip()}"
    )
    headers = get_auth_headers()

    try:
        resp = httpx.get(url_get, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return {"API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"Error: ": f"{e}"}

@mcp.tool()    
def createiPadApiKey() -> dict:
    """
    Create a new iPad API key for the current event.

    This tool triggers the backend to generate an iPad API key for the event
    and returns the updated event information.
    """

    url_post = (
        f"{BASE_PATH}/v1/{DOMAIN}/events/"
        f"{EVENT_ID}/ipad-api-key"
    )
    headers = get_auth_headers()

    try:
        resp = httpx.post(url_post, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return {"API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"Error: ": f"{e}"}

@mcp.tool()  
def applyReceiptDefaults() -> dict:
    """
    Apply default receipt settings to the current event.

    This tool triggers the backend to update the event's receipt-related settings
    to system defaults.
    """

    url_post = (
        f"{BASE_PATH}/v1/{DOMAIN}/events/"
        f"{EVENT_ID}/apply-receipt-defaults"
    )
    headers = get_auth_headers()

    try:
        resp = httpx.post(url_post, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return {"API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"Error: ": f"{e}"}

@mcp.tool()   
def obfuscateEvent(dry_run: bool = True) -> dict:
    """
    Obfuscate (anonymize) guest data in an event.

    This tool sends a request to obfuscate guest data for the event.
    If 'dry_run' is True (default), the operation will simulate the changes without applying them.

    Parameters:
    - dry_run: Boolean flag indicating whether to simulate (True) or apply (False) the obfuscation.
    """

    url_post = (
        f"{BASE_PATH}/v1/{DOMAIN}/events/"
        f"{EVENT_ID}/obfuscate?dryRun={'true' if dry_run else 'false'}"
    )
    headers = get_auth_headers()
    
    try:
        resp = httpx.post(url_post, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return {"API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"Error: ": f"{e}"}

@mcp.tool()
def actionsJSON(actions: list[dict]) -> dict:
    """
    Trigger control actions on an event (e.g. close silent auction, close live auction, close buy now, close lots, close raffles, close ticket, close pledges, close all, update dates).

    Input should be a list of action objects. Each action object must have a "type" key,
    and may optionally include a "values" dictionary depending on the action type.

    Example input:
    [
        {"type": "CLOSE_SILENT_AUCTION"},
        {"type": "UPDATE_DATES", "values": {"startTime": "2025-07-10T18:00:00Z", "endTime": "2025-07-10T22:00:00Z"}}
    ]
    """

    url_post = (
        f"{BASE_PATH}/v1/{DOMAIN}/events/"
        f"{EVENT_ID}/actions"
    )
    headers = get_auth_headers()

    try:
        resp = httpx.post(url_post, json=actions, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return {"API Response: ": f"{resp.json()}"}
    except Exception as e:
        return {"Error: ": f"{e}"}