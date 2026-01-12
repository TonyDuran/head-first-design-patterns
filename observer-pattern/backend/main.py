"""
FastAPI backend for Observer Pattern Snake Game Demo
Demonstrates GOOD (WebSocket push) vs BAD (polling) patterns
"""
import asyncio
import time
import os
from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from typing import Optional
import json

from .game import GameSingleton, Direction, GameState

# Get the path to frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Global game state
game = None
game_tick_task = None
active_player = None  # Track the active player connection ID
player_lock = asyncio.Lock()
game_speed = 0.5  # Game tick interval in seconds (lower = faster)
use_push_updates = True  # Current mode: True = WebSocket (GOOD), False = Polling (BAD)
game_started = False  # Whether the game is actively running (not paused)
polling_delay = 0.1  # Artificial delay for polling endpoint in seconds


async def game_tick_loop():
    """Background task that advances game state at intervals"""
    global game, game_speed, game_started
    while True:
        try:
            if game and game_started and not game.state.game_over:
                game.tick()
            await asyncio.sleep(game_speed)
        except Exception as e:
            print(f"Error in game tick: {e}")
            await asyncio.sleep(game_speed)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global game, game_tick_task
    # Startup
    game = GameSingleton.get_instance("game.db")
    game_tick_task = asyncio.create_task(game_tick_loop())
    print("Game initialized and tick loop started")
    yield
    # Shutdown
    if game_tick_task:
        game_tick_task.cancel()
    print("Game shutdown")


app = FastAPI(lifespan=lifespan)

# Store WebSocket connections for push updates
spectator_connections: dict[int, WebSocket] = {}
connection_counter = 0


@app.get("/api/state")
async def get_state():
    """Endpoint for polling spectators (BAD approach)"""
    global polling_delay
    if not game:
        return {"error": "Game not initialized"}
    # Artificial delay to simulate bad polling
    await asyncio.sleep(polling_delay)
    state = game.get_state()
    return state.to_dict()


@app.post("/api/player/connect")
async def player_connect():
    """Player endpoint - first come, first serve"""
    global active_player, game

    player_id = id(asyncio.current_task())
    active_player = player_id

    # If no game or game is over, reset it
    if not game or game.state.game_over:
        game.reset_game()

    return {"status": "connected", "player_id": player_id}


@app.post("/api/player/disconnect")
async def player_disconnect():
    """Player disconnect - allows others to take over"""
    global active_player
    active_player = None
    return {"status": "disconnected"}


@app.post("/api/player/direction/{direction}")
async def set_direction(direction: str):
    """Set snake direction from player input"""
    global active_player
    if active_player is None:
        raise HTTPException(status_code=409, detail="No active player")

    try:
        dir_enum = Direction(direction.upper())
        game.set_direction(dir_enum)
        return {"status": "success"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid direction")


@app.post("/api/player/reset")
async def reset_game():
    """Reset game for new round"""
    global game_started
    game.reset_game()
    game_started = False  # Don't auto-start after reset
    return {"status": "game_reset"}


@app.post("/api/player/start")
async def start_game():
    """Start the game (allow ticking)"""
    global game_started
    game_started = True
    return {"status": "game_started"}


@app.post("/api/player/pause")
async def pause_game():
    """Pause the game (stop ticking)"""
    global game_started
    game_started = False
    return {"status": "game_paused"}


@app.post("/api/player/resume")
async def resume_game():
    """Resume the game (start ticking again)"""
    global game_started
    game_started = True
    return {"status": "game_resumed"}


@app.get("/api/player/spectator-count")
async def get_spectator_count():
    """Get number of connected spectators"""
    return {"spectator_count": len(spectator_connections)}


@app.post("/api/player/polling-delay/{delay_ms}")
async def set_polling_delay(delay_ms: float):
    """Set artificial delay for polling endpoint in milliseconds"""
    global polling_delay
    # Clamp between 0 and 2000ms
    polling_delay = max(0, min(2.0, delay_ms / 1000.0))
    return {"status": "delay_set", "delay_ms": polling_delay * 1000}


@app.post("/api/player/speed/{speed}")
async def set_speed(speed: float):
    """Set game speed (tick interval in seconds)"""
    global game_speed
    # Clamp between 0.1 (fast) and 2.0 (slow)
    game_speed = max(0.1, min(2.0, speed))
    return {"status": "speed_set", "speed": game_speed}


@app.post("/api/player/toggle-mode")
async def toggle_mode():
    """Toggle between GOOD (WebSocket) and BAD (Polling) modes"""
    global use_push_updates
    use_push_updates = not use_push_updates
    return {"use_push_updates": use_push_updates}


@app.get("/api/mode")
async def get_mode():
    """Get current mode setting"""
    return {"use_push_updates": use_push_updates}


@app.websocket("/ws/spectate")
async def websocket_spectate(websocket: WebSocket):
    """WebSocket endpoint for GOOD approach (push updates)"""
    global connection_counter, spectator_connections

    await websocket.accept()
    conn_id = connection_counter
    connection_counter += 1
    spectator_connections[conn_id] = websocket

    def notify_spectator(state: GameState):
        """Callback for observer pattern - runs when game state changes"""
        # This will be called from the game tick thread
        asyncio.create_task(send_update_to_spectator(conn_id, state))

    game.subscribe(notify_spectator)

    try:
        # Send initial state
        state = game.get_state()
        await websocket.send_json({
            "type": "game_state",
            "data": state.to_dict()
        })

        # Keep connection alive, listen for disconnection
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        game.unsubscribe(notify_spectator)
        if conn_id in spectator_connections:
            del spectator_connections[conn_id]


async def send_update_to_spectator(conn_id: int, state: GameState):
    """Send update to a specific spectator"""
    if conn_id in spectator_connections:
        try:
            await spectator_connections[conn_id].send_json({
                "type": "game_state",
                "data": state.to_dict(),
                "timestamp": time.time()
            })
        except Exception as e:
            print(f"Error sending to spectator {conn_id}: {e}")


@app.get("/api/health")
async def health():
    """Health check"""
    return {"status": "ok"}


@app.get("/")
async def index():
    """Serve frontend"""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/player")
async def player():
    """Serve player frontend"""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# Serve static files from frontend
try:
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")
