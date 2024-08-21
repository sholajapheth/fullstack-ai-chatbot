import os
from ..socket.connection import ConnectionManager
from ..socket.utils import get_token
from ..redis.config import RedisCn
from ..redis.producer import Producer
from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    WebSocket,
    Request,
    BackgroundTasks,
    HTTPException,
    WebSocketDisconnect,
)
import uuid
from ..schema.chat import Chat
from redis.commands.json.path import Path


manager = ConnectionManager()
chat = APIRouter()
redis = RedisCn()


# ==================================================================


# @route    POST /token
# @desc     Route to generate chat token
# @access   Public
@chat.post("/token")
async def token_generator(name: str, request: Request):

    if name == "":
        raise HTTPException(
            status_code=400, detail={"loc": "name", "msg": "Enter a valid name"}
        )

    token = str(uuid.uuid4())

    json_client = await redis.create_connection()

    #  create a new chat session
    chat_session = Chat(token=token, messages=[], name=name)

    print(chat_session.model_dump())

    # store chat session in redis JSON with the token as key
    json_client.json().set(str(token), Path.root_path(), chat_session.model_dump())

    # set a timeout for redis data
    json_client.expire(str(token), 3600)

    return chat_session.model_dump()


# ==================================================================


# @route   POST /refresh_token
# @desc    Route to refresh chat token
# @access  Public
@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None


# ==================================================================


# @route   Websocket /chat
# @desc    Socket for chatbot
# @access  Public
@chat.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket = WebSocket, token: str = Depends(get_token)
):
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)

    try:
        while True:
            data = await websocket.receive_text() + " (echo)"
            print(data)
            stream_data = {}
            stream_data[token] = data
            producer.add_to_stream(stream_data, "message_channel")
            await manager.send_personal_message(
                f"Response: Simulating response from the GPT service", websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client left the chat")
