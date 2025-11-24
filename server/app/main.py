import asyncio
from contextlib import asynccontextmanager
import json
import math
import time
import uuid
from typing import Any, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app import constants as constsants
from app.services.Player import Player
from app.services.Bullet import Bullet
from app.utils.Vector2 import Vector2


# Setup lifetime
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load
    print("Starting game tick loop")
    asyncio.create_task(game_tick_loop())
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
TICK_RATE = 20  # ticks per second
DT = 1.0 / TICK_RATE

# Web sockets
connections: Dict[str, WebSocket] = {}
players: Dict[str, Player] = {}
bullets: Dict[str, Bullet] = {}


# Utility send
async def safe_send(websocket: WebSocket, data: Any) -> None:
    try:
        await websocket.send_text(json.dumps(data))
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error sending data: {e}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pid = str(uuid.uuid4())[:8]
    connections[pid] = websocket
    players[pid] = Player(pid, name=f"Player_{pid}")

    print(f"Player {pid} connected.")

    # Send id
    await safe_send(websocket, {"type": "init", "id": pid})
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # Basic message handling
            if message.get("type") == "input":
                player: Any = players.get(pid)
                if player:
                    player.inputs.append(message)
                    player.last_input_seq = message["input"]["seq"]
            elif message.get("type") == "join":
                players[pid].name = message.get("name", "Player")
            # Ignore unknown message types

    except WebSocketDisconnect:
        print(f"Player {pid} disconnected.")
        del connections[pid]
        del players[pid]
    finally:
        connections.pop(pid, None)
        players.pop(pid, None)


async def game_tick():
    last = time.time()
    while True:
        now = time.time()
        elapsed = now - last
        if elapsed < DT:
            await asyncio.sleep(DT - elapsed)
            continue

        last = time.time()
        process_inputs(DT)
        await broadcast_state()


async def game_tick_loop():
    last = time.time()
    while True:
        now = time.time()
        elapsed = now - last
        if elapsed < DT:
            await asyncio.sleep(DT - elapsed)
            continue
        last = time.time()
        process_inputs(DT)
        await broadcast_state()


def process_inputs(dt: float):
    # Apply player inputs
    for pid, p in list(players.items()):
        # default velocities
        vx = vy = 0.0
        # Process queued inputs (simple: take last)
        if p.inputs:
            # choose the last input in the queue (could process all for deterministic)
            inp = p.inputs.pop(0)
            # sample input fields; adjust for dt
            up = inp.get("up", False)
            down = inp.get("down", False)
            left = inp.get("left", False)
            right = inp.get("right", False)
            shoot = inp.get("shoot", False)
            angle = inp.get("angle", p.angle)
            p.angle = angle
            if up:
                vy -= 1
            if down:
                vy += 1
            if left:
                vx -= 1
            if right:
                vx += 1
            mag = math.hypot(vx, vy)
            if mag > 0:
                vx = vx / mag * constsants.PLAYER_SPEED
                vy = vy / mag * constsants.PLAYER_SPEED
            else:
                vx = vy = 0.0
            # movement
            p.x += vx * dt
            p.y += vy * dt
            # shooting: spawn bullet
            if shoot:
                bx = p.x + math.cos(p.angle) * 16
                by = p.y + math.sin(p.angle) * 16
                bvx = math.cos(p.angle) * constsants.BULLET_SPEED
                bvy = math.sin(p.angle) * constsants.BULLET_SPEED
                b = Bullet(owner_id=p.id, x=bx, y=by, vel=Vector2(bvx, bvy))
                bullets[b.id] = b
        # else: could apply friction or keep last velocity if desired

    # update bullets
    nowt = time.time()
    for bid in list(bullets.keys()):
        b = bullets[bid]
        b.x += b.velocity.x * dt
        b.y += b.velocity.y * dt
        if nowt - b.spawn_time > constsants.BULLET_LIFETIME:
            bullets.pop(bid, None)
        else:
            # simple collision check with players (not owner)
            for pid, p in players.items():
                if pid == b.owner:
                    continue
                dx = p.x - b.x
                dy = p.y - b.y
                if dx * dx + dy * dy < (12 * 12):  # collision radius
                    p.health -= 10
                    bullets.pop(bid, None)
                    break


async def broadcast_state():
    snapshot: Dict[str, Any] = {
        "type": "state",
        "tick": int(time.time() * 1000),
        "players": [
            {"id": p.id, "x": p.x, "y": p.y, "angle": p.angle, "health": p.health}
            for p in players.values()
        ],
        "bullets": [
            {"id": b.id, "x": b.x, "y": b.y, "vx": b.velocity.x, "vy": b.velocity.y}
            for b in bullets.values()
        ],
    }
    coros: list[Any] = []
    for _, ws in list(connections.items()):
        coros.append(safe_send(ws, snapshot))
    if coros:
        await asyncio.gather(*coros, return_exceptions=True)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
