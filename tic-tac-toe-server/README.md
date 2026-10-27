# Tic-Tac-Toe Flask Server

Implementation of the Tic-Tac-Toe API contract from the course specification.

## API Contract

### `POST /api/move`

**Request body:**
```json
{
  "board": "O........",
  "agent": "random"
}
```

- `board`: 9-character string (positions 0–8, row by row)
  - `X` = agent, `O` = human, `.` = empty
- `agent`: currently only `"random"` ( `"qtable"` reserved for later)

**Success (200):**
```json
{
  "board": "O...X....",
  "agent_move": 4,
  "status": "playing",
  "winning_line": null
}
```

- `status`: `"playing"` | `"agent_wins"` | `"human_wins"` | `"draw"`
- `agent_move`: `0–8` or `null` (when the human's move already ended the game)
- `winning_line`: `null` or array of 3 indexes, e.g. `[2, 4, 6]`

**Error (400):**
```json
{"error": "…"}
```

Returned for: invalid board, missing field, unknown agent.

## How to run

```bash
# (optional) create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in the browser.

## Project structure

```
tic-tac-toe-server/
├── app.py                 # Flask server + /api/move
├── requirements.txt
├── templates/
│   └── index.html         # Game page
└── static/
    ├── style.css
    └── game.js            # Client logic
```

## Behavior highlights (matching the specification)

- Page starts empty – wait for **New Game**
- **Who Starts** is a toggle (Agent / Human), disabled while a game is in progress
- **Agent Type** is a dropdown (`random` available, `qtable` shown but disabled)
- Board is locked while waiting for the server ("Agent is thinking…")
- After game ends, empty squares are no longer clickable
- Server errors / unreachable server are shown in red
- Winning line is highlighted in green
