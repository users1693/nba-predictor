from typing import Dict, Optional

# Stat weights for scoring algorithm
WEIGHTS = {
    'fg_pct': 3.0,      # Field goal efficiency is critical
    'ppg': 0.5,         # Points matter but need to normalize
    'apg': 2.0,         # Ball movement/playmaking
    'rpg': 1.5,         # Rebounding/possession control
}

# Home court advantage bonus (percentage points)
HOME_COURT_ADVANTAGE = 5.0


def calculate_team_score(stats: Dict[str, float]) -> float:
    """
    Calculate a team's strength score based on their statistics.
    
    Args:
        stats: Dictionary of team statistics
        
    Returns:
        Numerical strength score
    """
    score = 0.0
    
    for stat_name, weight in WEIGHTS.items():
        stat_value = stats.get(stat_name, 0.0)
        score += stat_value * weight
    
    return score


def predict_game(home_team: Dict, away_team: Dict, 
                 use_home_advantage: bool = True) -> Dict:
    """
    Predict the winner of a game based on team statistics.
    
    Args:
        home_team: Dictionary with 'name', 'abbreviation', and 'stats'
        away_team: Dictionary with 'name', 'abbreviation', and 'stats'
        use_home_advantage: Whether to apply home court advantage
        
    Returns:
        Dictionary with prediction results
    """
    # Calculate base scores
    home_score = calculate_team_score(home_team['stats'])
    away_score = calculate_team_score(away_team['stats'])
    
    # Apply home court advantage
    if use_home_advantage:
        home_score += HOME_COURT_ADVANTAGE
    
    # Determine winner
    if home_score > away_score:
        predicted_winner = home_team['name']
        winner_abbr = home_team['abbreviation']
        score_diff = home_score - away_score
    else:
        predicted_winner = away_team['name']
        winner_abbr = away_team['abbreviation']
        score_diff = away_score - home_score
    
    # Calculate confidence (simple approach)
    # Larger score difference = higher confidence
    total_score = home_score + away_score
    confidence = min((score_diff / total_score) * 2000, 99.9) 
    
    return {
        'predicted_winner': predicted_winner,
        'winner_abbreviation': winner_abbr,
        'confidence': round(confidence, 1),
        'home_score': round(home_score, 2),
        'away_score': round(away_score, 2),
        'score_difference': round(score_diff, 2)
    }


# Test function
def main():
    """Test the prediction engine with sample data"""
    
    # Sample team data (these are realistic NBA stats)
    home_team = {
        'name': 'Cleveland Cavaliers',
        'abbreviation': 'CLE',
        'stats': {
            'fg_pct': 45.3,
            'ppg': 121.1,
            'rpg': 43.8,
            'apg': 27.6
        }
    }
    
    away_team = {
        'name': 'Milwaukee Bucks',
        'abbreviation': 'MIL',
        'stats': {
            'fg_pct': 50.2,
            'ppg': 118.4,
            'rpg': 40.2,
            'apg': 26.8
        }
    }
    
    print("="*60)
    print("PREDICTION ENGINE TEST")
    print("="*60)
    print(f"\nHome: {home_team['name']}")
    print(f"  Stats: FG%={home_team['stats']['fg_pct']}, "
          f"PPG={home_team['stats']['ppg']}, "
          f"RPG={home_team['stats']['rpg']}, "
          f"APG={home_team['stats']['apg']}")
    
    print(f"\nAway: {away_team['name']}")
    print(f"  Stats: FG%={away_team['stats']['fg_pct']}, "
          f"PPG={away_team['stats']['ppg']}, "
          f"RPG={away_team['stats']['rpg']}, "
          f"APG={away_team['stats']['apg']}")
    
    # Make prediction
    prediction = predict_game(home_team, away_team)
    
    print(f"\n{'='*60}")
    print("PREDICTION")
    print(f"{'='*60}")
    print(f"🏆 Predicted Winner: {prediction['predicted_winner']} "
          f"({prediction['winner_abbreviation']})")
    print(f"📊 Confidence: {prediction['confidence']}%")
    print(f"🏠 Home Score: {prediction['home_score']}")
    print(f"✈️  Away Score: {prediction['away_score']}")
    print(f"📈 Score Difference: {prediction['score_difference']}")


if __name__ == "__main__":
    main()