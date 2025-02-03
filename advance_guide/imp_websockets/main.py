from typing import Annotated

from fastapi import FastAPI, WebSocket, Request, Cookie, Query, Depends, WebSocketException, status
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="advance_guide/imp_websockets/templates")


@app.get("/{_type}", response_class=HTMLResponse)
async def get(request: Request, _type):
    if _type == "token":
        return templates.TemplateResponse(request=request, name="websocket_token.html")
    elif _type == "clients":
        return templates.TemplateResponse(request=request, name="websocket_client.html")
    else:
        return templates.TemplateResponse(request=request, name="websocket_html.html")


async def get_cookie_or_token(
        websocket: WebSocket,
        session: Annotated[str | None, Cookie()] = None,
        token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("items/{item_id}/ws")
async def websocket_token(
        *,
        websocket: WebSocket,
        item_id: str,
        q: int | None = None,
        cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query Parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for Item ID: {item_id}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
