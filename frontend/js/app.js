// API Configuration
const API_URL = "http://127.0.0.1:8000"; // Local development
// const API_URL = 'https://your-app.onrender.com';  // Production (we'll change this later)

// DOM Elements
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const errorTextEl = document.getElementById("error-text");
const noGamesEl = document.getElementById("no-games");
const predictionsContainer = document.getElementById("predictions-container");

// Load predictions on page load
document.addEventListener("DOMContentLoaded", () => {
  loadPredictions();
});

/**
 * Fetch and display predictions from the API
 */
async function loadPredictions() {
  // Show loading state
  showLoading();

  try {
    const response = await fetch(`${API_URL}/predictions`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Check if we have predictions
    if (data.games_count === 0) {
      showNoGames();
      return;
    }

    // Display predictions
    displayPredictions(data.predictions);
  } catch (error) {
    console.error("Error fetching predictions:", error);
    showError(error.message);
  }
}

/**
 * Display predictions in the UI
 */
function displayPredictions(predictions) {
  // Hide loading/error states
  hideAllStates();

  // Show predictions container
  predictionsContainer.style.display = "grid";

  // Clear existing content
  predictionsContainer.innerHTML = "";

  // Create a card for each game
  predictions.forEach((game) => {
    const card = createGameCard(game);
    predictionsContainer.appendChild(card);
  });
}

/**
 * Create a game card element
 */
function createGameCard(game) {
  const card = document.createElement("div");
  card.className = "game-card";

  // Format game time
  const gameTime = formatGameTime(game.game_time);

  // Determine which team won
  const homeWon = game.prediction.winner === game.home_team.name;

  card.innerHTML = `
        <div class="game-header">
            <div class="game-time">${gameTime}</div>
            <div class="game-title">${game.game_name}</div>
        </div>
        
        <div class="team ${homeWon ? "winner-team" : ""}">
            <img src="${game.home_team.logo}" alt="${
    game.home_team.abbreviation
  }" class="team-logo">
            <div class="team-info">
                <div class="team-name">${game.home_team.name} (Home)</div>
                <div class="team-stats">
                    <span class="stat">FG: ${
                      game.home_team.stats.fg_pct
                    }%</span>
                    <span class="stat">PPG: ${game.home_team.stats.ppg}</span>
                    <span class="stat">RPG: ${game.home_team.stats.rpg}</span>
                    <span class="stat">APG: ${game.home_team.stats.apg}</span>
                </div>
            </div>
            <div class="predictor-score">${game.home_team.predictor_score}</div>
        </div>
        
        <div class="vs-divider">
            <span class="vs-text">VS</span>
        </div>
        
        <div class="team ${!homeWon ? "winner-team" : ""}">
            <img src="${game.away_team.logo}" alt="${
    game.away_team.abbreviation
  }" class="team-logo">
            <div class="team-info">
                <div class="team-name">${game.away_team.name} (Away)</div>
                <div class="team-stats">
                    <span class="stat">FG: ${
                      game.away_team.stats.fg_pct
                    }%</span>
                    <span class="stat">PPG: ${game.away_team.stats.ppg}</span>
                    <span class="stat">RPG: ${game.away_team.stats.rpg}</span>
                    <span class="stat">APG: ${game.away_team.stats.apg}</span>
                </div>
            </div>
            <div class="predictor-score">${game.away_team.predictor_score}</div>
        </div>
        
        <div class="prediction-result">
            <div class="winner">
                <span class="winner-icon">🏆</span>
                ${game.prediction.winner}
            </div>
            <div class="confidence-label">Confidence</div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${
                  game.prediction.confidence
                }%"></div>
            </div>
            <div class="confidence-value">${game.prediction.confidence}%</div>
            <div class="score-diff">Score difference: ${
              game.prediction.score_difference
            } points</div>
        </div>
    `;

  return card;
}

/**
 * Format ISO timestamp to readable time
 */
function formatGameTime(isoString) {
  try {
    const date = new Date(isoString);
    const options = {
      weekday: "short",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
      timeZoneName: "short",
    };
    return date.toLocaleString("en-US", options);
  } catch (error) {
    return isoString;
  }
}

/**
 * UI State Management
 */
function showLoading() {
  hideAllStates();
  loadingEl.style.display = "block";
}

function showError(message) {
  hideAllStates();
  errorTextEl.textContent = message;
  errorEl.style.display = "block";
}

function showNoGames() {
  hideAllStates();
  noGamesEl.style.display = "block";
}

function hideAllStates() {
  loadingEl.style.display = "none";
  errorEl.style.display = "none";
  noGamesEl.style.display = "none";
  predictionsContainer.style.display = "none";
}
