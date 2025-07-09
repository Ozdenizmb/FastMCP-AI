import httpx, os
from dotenv import load_dotenv

http_client = httpx.Client()

load_dotenv()

_login_data = {"csrf_token": None, "cookies": None}

def _do_login() -> dict:
    if _login_data["csrf_token"] and _login_data["cookies"]:
        return
    
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    url = "http://localhost:8080/v1/localhost/auth/login"
    payload = {"username": username, "password": password, "version": 0}
    resp = http_client.post(url, json=payload, headers={"X-CSRF-Token": "FETCH"})
    resp.raise_for_status()

    csrf_token = resp.headers.get("X-CSRF-Token")
    cookies = resp.headers.get("Set-Cookie")

    if not csrf_token or not cookies:
        raise RuntimeError("Login headers missing!")
    
    _login_data["csrf_token"] = csrf_token
    _login_data["cookies"] = cookies

def get_auth_headers():

    _do_login()

    return {
        "X-CSRF-Token": _login_data["csrf_token"],
        "Cookie": _login_data["cookies"],
    }