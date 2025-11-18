"""
FastAPI application for NBA Game Predictor
Provides REST API endpoints for fetching predictions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import sys
from pathlib import Path

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.data.schedule import get_todays_games
from src.predictor.engine import predict_game

# Initialize FastAPI app
app = FastAPI(
    title="NBA Game Predictor API",
    description="Predict NBA game outcomes based on team statistics",
    version="1.0.0"
)

# Enable CORS so frontend can call this API
# (CORS = Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint - API info"""
    return {
        "message": "NBA Game Predictor API",
        "version": "1.0.0",
        "endpoints": {
            "/predictions": "Get today's game predictions",
            "/health": "Health check"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/predictions")
def get_predictions():
    """
    Get predictions for today's scheduled NBA games.
    
    Returns:
        List of predictions with game info and predicted winners
    """
    try:
        # Fetch today's games
        games = get_todays_games()
        
        if not games:
            return {
                "date": "today",
                "games_count": 0,
                "message": "No scheduled games found for today",
                "predictions": []
            }
        
        # Generate predictions for each game
        predictions = []
        for game in games:
            home_team = game['home_team']
            away_team = game['away_team']
            
            # Make prediction
            prediction = predict_game(home_team, away_team, use_home_advantage=True)
            
            # Combine game info with prediction
            result = {
                "game_id": game['game_id'],
                "game_name": game['game_name'],
                "game_time": game['game_time'],
                "home_team": {
                    "name": home_team['name'],
                    "abbreviation": home_team['abbreviation'],
                    "logo": home_team.get('logo', ''),
                    "stats": home_team['stats'],
                    "predictor_score": prediction['home_score']
                },
                "away_team": {
                    "name": away_team['name'],
                    "abbreviation": away_team['abbreviation'],
                    "logo": away_team.get('logo', ''),
                    "stats": away_team['stats'],
                    "predictor_score": prediction['away_score']
                },
                "prediction": {
                    "winner": prediction['predicted_winner'],
                    "winner_abbreviation": prediction['winner_abbreviation'],
                    "confidence": prediction['confidence'],
                    "score_difference": prediction['score_difference']
                }
            }
            predictions.append(result)
        
        return {
            "date": "today",
            "games_count": len(predictions),
            "predictions": predictions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating predictions: {str(e)}")


# Run with: uvicorn src.api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)