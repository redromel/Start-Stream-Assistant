from urllib.parse import parse_qs, urlparse
from nicegui import ui, Client

@ui.page('/redirect_page', dark=True)
async def redirect_page(client: Client):
    await client.connected()
    ui.label("test")
    ui.button("test 2")
    url = await ui.run_javascript('window.location.href')
    try:
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['code'][0]
        print(code)
    except Exception as e:
        print(e)