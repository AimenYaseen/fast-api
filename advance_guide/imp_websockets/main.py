from typing import Annotated

from fastapi import FastAPI, WebSocket, Request, Cookie, Query, Depends, WebSocketException, status, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

# ---------------------------- WEBSOCKET WITH TOKEN --------------------------------------
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


# ---------------------- CONNECTION MANAGER -----------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message:str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
