"""
Tic-Tac-Toe Flask server
Implements the API contract from the specification.

POST /api/move
  Request:  {"board": ".........", "agent": "random"}
  Success:  {"board": "...", "agent_move": int|null, "status": "...", "winning_line": list|null}
  Error:    {"error": "..."} with status 400
"""

from flask import Flask, request, render_template, jsonify
import random

app = Flask(__name__)

# All 8 possible winning lines (indexes 0-8)
WINNING_LINES = [
    [0, 1, 2],  # top row
    [3, 4, 5],  # middle row
    [6, 7, 8],  # bottom row
    [0, 3, 6],  # left column
    [1, 4, 7],  # middle column
    [2, 5, 8],  # right column
    [0, 4, 8],  # diagonal \
    [2, 4, 6],  # diagonal /
]


def is_valid_board(board: str) -> bool:
    """Board must be exactly 9 characters, only X, O and ."""
    if not isinstance(board, str) or len(board) != 9:
        return False
    return all(c in "XO." for c in board)


def count_marks(board: str) -> tuple[int, int]:
    """Return (number of X, number of O)."""
    return board.count("X"), board.count("O")


def get_winner(board: str) -> tuple[str | None, list[int] | None]:
    """
    Check if there is a winner.
    Returns (winner, winning_line) where winner is "X", "O" or None.
    """
    for line in WINNING_LINES:
        a, b, c = line
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a], line
    return None, None


def is_full(board: str) -> bool:
    return "." not in board


def get_empty_squares(board: str) -> list[int]:
    return [i for i, c in enumerate(board) if c == "."]


def random_agent_move(board: str) -> int | None:
    """Choose a random empty square. Returns None if board is full."""
    empty = get_empty_squares(board)
    if not empty:
        return None
    return random.choice(empty)


@app.route("/")
def index():
    """Serve the game page (client)."""
    return render_template("index.html")


@app.route("/api/move", methods=["POST"])
def api_move():
    """
    Main game endpoint.
    Receives the current board after the human's move,
    returns the agent's reply (or indicates the game already ended).
    """
    data = request.get_json(silent=True)

    # --- Validation ---
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if "board" not in data:
        return jsonify({"error": "Missing field: board"}), 400

    if "agent" not in data:
        return jsonify({"error": "Missing field: agent"}), 400

    board = data["board"]
    agent = data["agent"]

    if not is_valid_board(board):
        return jsonify({"error": "Invalid board: must be 9 characters of X, O or ."}), 400

    if agent not in ("random",):  # later: "qtable"
        return jsonify({"error": f"Unknown agent: '{agent}'"}), 400

    # --- Check if the human's move already ended the game ---
    winner, winning_line = get_winner(board)

    if winner == "O":
        return jsonify({
            "board": board,
            "agent_move": None,
            "status": "human_wins",
            "winning_line": winning_line
        })

    if winner == "X":
        # Should not normally happen (agent already won on previous turn)
        return jsonify({
            "board": board,
            "agent_move": None,
            "status": "agent_wins",
            "winning_line": winning_line
        })

    if is_full(board):
        return jsonify({
            "board": board,
            "agent_move": None,
            "status": "draw",
            "winning_line": None
        })

    # --- Agent plays ---
    if agent == "random":
        move = random_agent_move(board)
    else:
        # Placeholder for future agents
        move = random_agent_move(board)

    if move is None:
        # Board became full somehow
        return jsonify({
            "board": board,
            "agent_move": None,
            "status": "draw",
            "winning_line": None
        })

    # Apply the move
    board_list = list(board)
    board_list[move] = "X"
    new_board = "".join(board_list)

    # Check result after agent's move
    winner, winning_line = get_winner(new_board)

    if winner == "X":
        status = "agent_wins"
    elif is_full(new_board):
        status = "draw"
        winning_line = None
    else:
        status = "playing"
        winning_line = None

    return jsonify({
        "board": new_board,
        "agent_move": move,
        "status": status,
        "winning_line": winning_line
    })


if __name__ == "__main__":
    app.run(debug=True)
