from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse
# import uvicorn

app = FastAPI()

# Configuration des en-têtes CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez spécifier les domaines autorisés
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/")
def read_api():
    return {"message": "Hello from FastAPI!"}

@app.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
