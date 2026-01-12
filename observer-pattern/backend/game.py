"""
Snake game logic with Observer pattern demonstration.
The GameState is a Subject that notifies Observers (spectators) of updates.
"""
import sqlite3
from enum import Enum
from typing import List, Callable, Optional
from dataclasses import dataclass, asdict
from threading import Lock
import json


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def to_dict(self):
        return {"x": self.x, "y": self.y}


@dataclass
class GameState:
    """Represents the current game state"""
    snake: List[Position]
    fruit: Position
    score: int
    game_over: bool
    direction: Direction
    high_score: int

    def to_dict(self):
        return {
            "snake": [pos.to_dict() for pos in self.snake],
            "fruit": self.fruit.to_dict(),
            "score": self.score,
            "game_over": self.game_over,
            "direction": self.direction.value,
            "high_score": self.high_score,
        }


class GameDatabase:
    """Handles all database operations for game state persistence"""

    def __init__(self, db_path: str = "game.db"):
        self.db_path = db_path
        self.lock = Lock()
        self._init_db()

    def _init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS game_state (
                    id INTEGER PRIMARY KEY,
                    snake TEXT NOT NULL,
                    fruit TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    game_over INTEGER NOT NULL,
                    direction TEXT NOT NULL,
                    high_score INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

    def save_state(self, state: GameState):
        """Write game state to database"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO game_state (snake, fruit, score, game_over, direction, high_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        json.dumps([asdict(p) for p in state.snake]),
                        json.dumps(asdict(state.fruit)),
                        state.score,
                        1 if state.game_over else 0,
                        state.direction.value,
                        state.high_score,
                    ),
                )
                conn.commit()

    def get_latest_state(self) -> Optional[GameState]:
        """Read latest game state from database"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT snake, fruit, score, game_over, direction, high_score
                    FROM game_state
                    ORDER BY id DESC
                    LIMIT 1
                """
                )
                row = cursor.fetchone()

                if not row:
                    return None

                snake_data = json.loads(row[0])
                fruit_data = json.loads(row[1])
                score = row[2]
                game_over = bool(row[3])
                direction = Direction(row[4])
                high_score = row[5]

                snake = [Position(**p) for p in snake_data]
                fruit = Position(**fruit_data)

                return GameState(
                    snake=snake,
                    fruit=fruit,
                    score=score,
                    game_over=game_over,
                    direction=direction,
                    high_score=high_score,
                )


class SnakeGame:
    """Main game logic - Subject in Observer pattern"""

    GRID_WIDTH = 20
    GRID_HEIGHT = 20

    def __init__(self, db_path: str = "game.db"):
        self.db = GameDatabase(db_path)
        self.lock = Lock()
        self.state = self._load_or_create_state()
        self.observers: List[Callable[[GameState], None]] = []

    def _load_or_create_state(self) -> GameState:
        """Load state from DB or create new game"""
        latest = self.db.get_latest_state()
        if latest and not latest.game_over:
            return latest

        # Create new game
        high_score = latest.high_score if latest else 0
        return GameState(
            snake=[Position(10, 10), Position(9, 10), Position(8, 10)],
            fruit=Position(15, 15),
            score=0,
            game_over=False,
            direction=Direction.RIGHT,
            high_score=high_score,
        )

    def subscribe(self, observer: Callable[[GameState], None]):
        """Register an observer (spectator)"""
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer: Callable[[GameState], None]):
        """Unregister an observer"""
        if observer in self.observers:
            self.observers.remove(observer)

    def _notify_observers(self):
        """Notify all observers of state change"""
        for observer in self.observers:
            try:
                observer(self.state)
            except Exception as e:
                print(f"Error notifying observer: {e}")

    def set_direction(self, direction: Direction):
        """Set the next direction for the snake"""
        with self.lock:
            # Prevent reversing into itself
            opposite = {
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP,
                Direction.LEFT: Direction.RIGHT,
                Direction.RIGHT: Direction.LEFT,
            }
            if self.state.direction != opposite[direction]:
                self.state.direction = direction

    def tick(self):
        """Advance game state by one tick"""
        with self.lock:
            if self.state.game_over:
                return

            # Calculate new head position
            head = self.state.snake[0]
            dx, dy = self._get_direction_vector(self.state.direction)
            new_head = Position(head.x + dx, head.y + dy)

            # Check collision with walls
            if (
                new_head.x < 0
                or new_head.x >= self.GRID_WIDTH
                or new_head.y < 0
                or new_head.y >= self.GRID_HEIGHT
            ):
                self.state.game_over = True
                if self.state.score > self.state.high_score:
                    self.state.high_score = self.state.score
                self.db.save_state(self.state)
                self._notify_observers()
                return

            # Check collision with self
            if new_head in self.state.snake:
                self.state.game_over = True
                if self.state.score > self.state.high_score:
                    self.state.high_score = self.state.score
                self.db.save_state(self.state)
                self._notify_observers()
                return

            # Add new head
            self.state.snake.insert(0, new_head)

            # Check fruit collision
            if new_head == self.state.fruit:
                self.state.score += 10
                self.state.fruit = self._generate_fruit()
            else:
                # Remove tail if didn't eat fruit
                self.state.snake.pop()

            # Save to database
            self.db.save_state(self.state)

            # Notify all observers
            self._notify_observers()

    def reset_game(self):
        """Reset game for new player"""
        with self.lock:
            high_score = self.state.high_score
            self.state = GameState(
                snake=[Position(10, 10), Position(9, 10), Position(8, 10)],
                fruit=Position(15, 15),
                score=0,
                game_over=False,
                direction=Direction.RIGHT,
                high_score=high_score,
            )
            self.db.save_state(self.state)
            self._notify_observers()

    def get_state(self) -> GameState:
        """Get current game state"""
        with self.lock:
            return GameState(
                snake=self.state.snake.copy(),
                fruit=self.state.fruit,
                score=self.state.score,
                game_over=self.state.game_over,
                direction=self.state.direction,
                high_score=self.state.high_score,
            )

    @staticmethod
    def _get_direction_vector(direction: Direction) -> tuple:
        """Get (dx, dy) for a direction"""
        vectors = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
        }
        return vectors[direction]

    @staticmethod
    def _generate_fruit() -> Position:
        """Generate a random fruit position"""
        import random

        return Position(
            random.randint(0, SnakeGame.GRID_WIDTH - 1),
            random.randint(0, SnakeGame.GRID_HEIGHT - 1),
        )


class GameSingleton:
    """Singleton pattern for game instance"""

    _instance: Optional[SnakeGame] = None
    _lock = Lock()

    @classmethod
    def get_instance(cls, db_path: str = "game.db") -> SnakeGame:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = SnakeGame(db_path)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """For testing purposes"""
        cls._instance = None
