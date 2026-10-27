/**
 * Tic-Tac-Toe client
 * Follows the behavior specification.
 */

const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const newGameBtn = document.getElementById("new-game-btn");
const whoStartsBtn = document.getElementById("who-starts-btn");
const agentTypeSelect = document.getElementById("agent-type");

let board = ".........";          // 9 characters
let gameActive = false;
let whoStarts = "Agent";         // "Agent" or "Human"
let waiting = false;

// Create the 9 squares
for (let i = 0; i < 9; i++) {
  const sq = document.createElement("button");
  sq.className = "square";
  sq.dataset.index = i;
  sq.disabled = true;
  sq.addEventListener("click", () => onSquareClick(i));
  boardEl.appendChild(sq);
}

function renderBoard(winningLine = null) {
  const squares = boardEl.querySelectorAll(".square");
  squares.forEach((sq, i) => {
    const mark = board[i];
    sq.textContent = mark === "." ? "" : mark;
    sq.classList.remove("X", "O", "win");
    if (mark === "X") sq.classList.add("X");
    if (mark === "O") sq.classList.add("O");
    if (winningLine && winningLine.includes(i)) {
      sq.classList.add("win");
    }
    // Disable when not the human's turn or game over / waiting
    sq.disabled = !gameActive || waiting || mark !== ".";
  });
}

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.classList.toggle("error", isError);
}

function updateControls() {
  // Who Starts can change only when no game is in progress
  whoStartsBtn.disabled = gameActive;
  whoStartsBtn.textContent = `Who Starts: ${whoStarts}`;

  // Agent Type can always be changed (per behavior)
  agentTypeSelect.disabled = false;
}

function startNewGame() {
  board = ".........";
  gameActive = true;
  waiting = false;
  renderBoard();
  updateControls();

  if (whoStarts === "Agent") {
    // Agent makes the first move
    setStatus("Agent is thinking…");
    waiting = true;
    renderBoard();
    callApi();
  } else {
    setStatus("Your turn");
  }
}

function onSquareClick(index) {
  if (!gameActive || waiting || board[index] !== ".") return;

  // Place human mark (O)
  const arr = board.split("");
  arr[index] = "O";
  board = arr.join("");
  renderBoard();

  setStatus("Agent is thinking…");
  waiting = true;
  renderBoard();          // lock the board
  callApi();
}

async function callApi() {
  const agent = agentTypeSelect.value;

  try {
    const res = await fetch("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board, agent })
    });

    const data = await res.json();

    if (!res.ok) {
      setStatus(data.error || "Server error", true);
      waiting = false;
      gameActive = false;
      renderBoard();
      updateControls();
      return;
    }

    // Update board with agent's reply
    board = data.board;
    waiting = false;

    if (data.status === "playing") {
      setStatus("Your turn");
      renderBoard();
    } else if (data.status === "agent_wins") {
      setStatus("Agent wins!");
      gameActive = false;
      renderBoard(data.winning_line);
    } else if (data.status === "human_wins") {
      setStatus("You win!");
      gameActive = false;
      renderBoard(data.winning_line);
    } else if (data.status === "draw") {
      setStatus("It's a draw!");
      gameActive = false;
      renderBoard();
    }

    updateControls();

  } catch (err) {
    setStatus("Cannot reach the server.", true);
    waiting = false;
    gameActive = false;
    renderBoard();
    updateControls();
  }
}

// Event listeners
newGameBtn.addEventListener("click", startNewGame);

whoStartsBtn.addEventListener("click", () => {
  if (gameActive) return;
  whoStarts = whoStarts === "Agent" ? "Human" : "Agent";
  updateControls();
});

// Initial state
renderBoard();
updateControls();
setStatus("Press New Game to start");
