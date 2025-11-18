"""
NBA Game Predictor - Main Script
Fetches today's scheduled games and predicts outcomes
"""

from src.data.schedule import get_todays_games
from src.predictor.engine import predict_game
from datetime import datetime


def main():
    """Main execution function"""
    
    print("=" * 80)
    print(" " * 25 + "NBA GAME PREDICTOR")
    print("=" * 80)
    print(f"\n📅 Date: {datetime.now().strftime('%B %d, %Y')}")
    print(f"⏰ Time: {datetime.now().strftime('%I:%M %p')}\n")
    
    # Step 1: Fetch today's games
    print("🔄 Fetching scheduled games from ESPN...\n")
    games = get_todays_games()
    
    if not games:
        print("❌ No scheduled games found for today.")
        print("   - Games may have already started")
        print("   - Or there might be no games scheduled")
        return
    
    print(f"✅ Found {len(games)} scheduled game(s)\n")
    print("=" * 80)
    print(" " * 30 + "PREDICTIONS")
    print("=" * 80)
    
    # Step 2: Predict each game
    for i, game in enumerate(games, 1):
        predict_and_display_game(game, i)
    
    print("\n" + "=" * 80)
    print("✅ Predictions complete!")
    print("=" * 80)


def predict_and_display_game(game: dict, game_number: int):
    """
    Predict and display results for a single game.
    
    Args:
        game: Game dictionary from schedule.py
        game_number: Game number for display
    """
    home_team = game['home_team']
    away_team = game['away_team']
    
    # Make prediction
    prediction = predict_game(home_team, away_team, use_home_advantage=True)
    
    # Display game info
    print(f"\n{'─' * 80}")
    print(f"🏀 GAME {game_number}: {game['game_name']}")
    print(f"{'─' * 80}")
    
    # Parse game time (it's in ISO format: "2025-11-18T00:00Z")
    try:
        game_time = datetime.fromisoformat(game['game_time'].replace('Z', '+00:00'))
        time_str = game_time.strftime('%I:%M %p ET')
    except:
        time_str = game['game_time']
    
    print(f"⏰ Scheduled: {time_str}\n")
    
    # Display teams and stats
    print(f"🏠 HOME: {home_team['name']} ({home_team['abbreviation']})")
    print(f"   📊 Season Stats:")
    print(f"      FG%: {home_team['stats'].get('fg_pct', 'N/A')}% | "
          f"PPG: {home_team['stats'].get('ppg', 'N/A')} | "
          f"RPG: {home_team['stats'].get('rpg', 'N/A')} | "
          f"APG: {home_team['stats'].get('apg', 'N/A')}")
    print(f"   🎯 Predictor Score: {prediction['home_score']}")
    
    print(f"\n✈️  AWAY: {away_team['name']} ({away_team['abbreviation']})")
    print(f"   📊 Season Stats:")
    print(f"      FG%: {away_team['stats'].get('fg_pct', 'N/A')}% | "
          f"PPG: {away_team['stats'].get('ppg', 'N/A')} | "
          f"RPG: {away_team['stats'].get('rpg', 'N/A')} | "
          f"APG: {away_team['stats'].get('apg', 'N/A')}")
    print(f"   🎯 Predictor Score: {prediction['away_score']}")
    
    # Display prediction
    print(f"\n{'─' * 80}")
    print(f"🏆 PREDICTION: {prediction['predicted_winner']} "
          f"({prediction['winner_abbreviation']}) wins")
    print(f"📊 Confidence: {prediction['confidence']}%")
    print(f"📈 Score Difference: {prediction['score_difference']} points")
    print(f"{'─' * 80}")


if __name__ == "__main__":
    main()