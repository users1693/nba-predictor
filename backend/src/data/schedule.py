import requests
from typing import List, Dict, Optional
from datetime import datetime

ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

def get_todays_games() -> List[Dict]:
    """
    Fetch today's NBA games from ESPN API.
    Only returns games that haven't started yet (STATUS_SCHEDULED).
    
    Returns:
        List of game dictionaries with team info and stats
    """
    try:
        response = requests.get(ESPN_SCOREBOARD_URL, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        events = data.get('events', [])
        
        games = []
        skipped_games = []
        
        for event in events:
            # Check game status
            competition = event.get('competitions', [{}])[0]
            status = competition.get('status', {})
            status_type = status.get('type', {})
            status_name = status_type.get('name', '')
            
            game_name = event.get('name', 'Unknown Game')
            
            # Only process scheduled games
            if status_name == 'STATUS_SCHEDULED':
                game = parse_game(event)
                if game:
                    games.append(game)
            else:
                # Track skipped games for logging
                status_detail = status_type.get('detail', status_name)
                skipped_games.append({
                    'name': game_name,
                    'status': status_detail
                })
        
        # Log what we skipped
        if skipped_games:
            print(f"\nSkipped {len(skipped_games)} game(s) that already started or finished:")
            for skipped in skipped_games:
                print(f"  - {skipped['name']}: {skipped['status']}")
            print()
        
        return games
    
    except requests.RequestException as e:
        print(f"Error fetching games: {e}")
        return []


def parse_game(event: Dict) -> Optional[Dict]:
    """
    Parse a single game event into our simplified format.
    
    Args:
        event: Raw event dict from ESPN API
        
    Returns:
        Simplified game dictionary or None if parsing fails
    """
    try:
        # Get basic game info
        game_id = event.get('id')
        game_name = event.get('name')
        game_time = event.get('date')
        
        # Navigate to competitors (teams)
        competition = event.get('competitions', [{}])[0]
        competitors = competition.get('competitors', [])
        
        if len(competitors) != 2:
            print(f"Warning: Game {game_id} doesn't have 2 competitors")
            return None
        
        # Find home and away teams
        home_team_data = None
        away_team_data = None
        
        for competitor in competitors:
            if competitor.get('homeAway') == 'home':
                home_team_data = competitor
            elif competitor.get('homeAway') == 'away':
                away_team_data = competitor
        
        if not home_team_data or not away_team_data:
            print(f"Warning: Could not identify home/away teams for game {game_id}")
            return None
        
        # Parse both teams
        home_team = parse_team(home_team_data)
        away_team = parse_team(away_team_data)
        
        return {
            "game_id": game_id,
            "game_name": game_name,
            "game_time": game_time,
            "home_team": home_team,
            "away_team": away_team
        }
    
    except Exception as e:
        print(f"Error parsing game: {e}")
        return None


def parse_team(competitor: Dict) -> Dict:
    """
    Parse team information and statistics from competitor data.
    
    Args:
        competitor: Competitor dict from ESPN API
        
    Returns:
        Dictionary with team name and stats
    """
    team_info = competitor.get('team', {})
    statistics = competitor.get('statistics', [])
    
    # Extract basic team info
    team = {
        "name": team_info.get('displayName', 'Unknown'),
        "abbreviation": team_info.get('abbreviation', 'UNK'),
        "logo": team_info.get('logo', ''),
        "stats": extract_stats(statistics)
    }
    
    return team


def extract_stats(statistics: List[Dict]) -> Dict:
    """
    Extract relevant statistics from the statistics array.
    
    Args:
        statistics: List of stat dictionaries
        
    Returns:
        Dictionary with key stats (fg_pct, ppg, rpg, apg)
    """
    stats = {}
    
    # Create a mapping for easy lookup
    stat_map = {
        'fieldGoalPct': 'fg_pct',
        'threePointPct': 'three_pct',
        'freeThrowPct': 'ft_pct',
        'avgPoints': 'ppg',
        'avgRebounds': 'rpg',
        'avgAssists': 'apg'
    }
    
    for stat in statistics:
        stat_name = stat.get('name')
        if stat_name in stat_map:
            our_name = stat_map[stat_name]
            value = stat.get('displayValue', '0')
            
            try:
                stats[our_name] = float(value)
            except ValueError:
                stats[our_name] = 0.0
    
    return stats


# Test function
def main():
    """Test the schedule fetcher"""
    print("="*60)
    print("NBA GAME SCHEDULE FETCHER")
    print("="*60)
    print("\nFetching today's scheduled NBA games from ESPN...\n")
    
    games = get_todays_games()
    
    if not games:
        print("⚠️  No scheduled games found.")
        print("   (Games may have already started or there are no games today)")
        return
    
    print(f"✅ Found {len(games)} scheduled game(s):\n")
    
    for i, game in enumerate(games, 1):
        print(f"{'='*60}")
        print(f"GAME {i}: {game['game_name']}")
        print(f"{'='*60}")
        print(f"⏰ Time: {game['game_time']}")
        print(f"\n🏠 HOME: {game['home_team']['name']} ({game['home_team']['abbreviation']})")
        home_stats = game['home_team']['stats']
        print(f"   📊 FG%: {home_stats.get('fg_pct', 'N/A')}% | "
              f"PPG: {home_stats.get('ppg', 'N/A')} | "
              f"RPG: {home_stats.get('rpg', 'N/A')} | "
              f"APG: {home_stats.get('apg', 'N/A')}")
        
        print(f"\n✈️  AWAY: {game['away_team']['name']} ({game['away_team']['abbreviation']})")
        away_stats = game['away_team']['stats']
        print(f"   📊 FG%: {away_stats.get('fg_pct', 'N/A')}% | "
              f"PPG: {away_stats.get('ppg', 'N/A')} | "
              f"RPG: {away_stats.get('rpg', 'N/A')} | "
              f"APG: {away_stats.get('apg', 'N/A')}")
        print()


if __name__ == "__main__":
    main()





    