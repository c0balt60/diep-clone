from fastapi import FastAPI
from server.app.routers.game_router import router as game_router

app: FastAPI = FastAPI()

app.include_router(game_router, prefix="/game", tags=["game"])
