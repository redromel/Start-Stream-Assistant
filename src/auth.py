import base64
import os
import requests
from oauthlib.oauth2 import WebApplicationClient

from constants import CLIENT_ID

scopes = "tournament.reporter user.identity"
auth_url = "https://start.gg/oauth/authorize"


client = WebApplicationClient(CLIENT_ID)


def generate_state():

    random_bytes = os.urandom(32)
    state = base64.urlsafe_b64encode(random_bytes).decode("utf-8")
    return state.rstrip("=")


url = client.prepare_request_uri(
    auth_url,
    redirect_uri="https://tolocalhost.com/redirect_page",
    scope = ['tournament.reporter','user.identity'],
    state = generate_state()
)
print(url)

data = client.prepare_refresh_body()
