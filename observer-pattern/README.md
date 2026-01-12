# Observer Pattern: Snake Game Demo

An interactive demonstration of the **Observer Pattern** using WebSocket (push) vs HTTP polling (pull) for real-time updates.

<img width="1557" height="981" alt="image" src="https://github.com/user-attachments/assets/ac81b218-cf95-4f1e-8fdb-bc055d7a3c2f" />

1-Player with many Specatators. The player can control whether the game is in real-time or delayed for spectators. 

## The Pattern

**Observer Pattern**: Objects (subjects) notify multiple observers of state changes automatically.

### Pros
- Decouples subjects from observers (loose coupling)
- Dynamic subscription/unsubscription at runtime
- Multiple observers handle events independently
- Real-time notifications without polling

### Cons
- Memory overhead from maintaining observer lists
- Hard to debug observer notification chains
- Observer execution order is unpredictable
- Can leak memory if observers aren't unsubscribed

## GOOD vs BAD in This Demo

- **GOOD (Push)**: WebSocket connections receive instant updates via `game.subscribe()` callback
- **BAD (Pull)**: HTTP polling every 1000ms with configurable artificial delay (0-2000ms)

Spectators can toggle between modes to see the real-time difference in lag.

## How to Run

```bash
docker-compose up --build
# Open http://localhost:8000
```

Player goes to one browser tab, spectators open more tabs. Player controls the snake, spectators watch with their chosen update method.

## Code Paths

### Player Path (Push Always)
- **Connect**: `POST /api/player/connect` → [backend/main.py](backend/main.py#L90)
- **Game State**: `WebSocket /ws/spectate` → [backend/main.py](backend/main.py#L173) (instant updates via `game.subscribe()`)
- **Controls**: Arrow keys + WASD for direction input

### Spectator Path (Toggle Between Methods)
- **GOOD (Push)**: `WebSocket /ws/spectate` → [backend/main.py](backend/main.py#L173) (same as player, instant)
- **BAD (Pull)**: `GET /api/state` → [backend/main.py](backend/main.py#L65) (polls every 1000ms + artificial delay)
- **Toggle Mode**: Click button → `POST /api/player/toggle-mode` → Server switches `use_push_updates` flag
- **Spectators auto-reconnect** when player toggles mode (checks every 2s via `GET /api/mode`)

### Core Observer Logic
- **Subscribe/Unsubscribe**: [backend/game.py](backend/game.py#L42-L51)
- **Notify All Observers**: [backend/game.py](backend/game.py#L53-L61) (called on each game tick)
- **Game Tick Loop**: [backend/main.py](backend/main.py#L31-L42) (runs every 0.5s by default)

## Features

- Player-only controls (WASD/Arrow keys)
- Speed slider (0.1-2.0s per tick)
- Polling delay slider (0-2000ms in BAD mode, only visible when BAD is active)
- Live spectator count display
- Lag indicator for spectators (ms since last update)
- Start/Pause/Resume game controls
- Spectators auto-sync when mode toggles

## Note

This is **heavily vibe coded** for educational impact over production standards. Observer list cleanup on disconnect may leak references. Feel free to PR improvements!
