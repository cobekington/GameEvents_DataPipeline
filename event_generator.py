import json
import random
import time
from datetime import datetime  # For alternative timestamp handling

# Configuration
INACTIVITY_THRESHOLD = 60  # Seconds a player remains active without events

# Global state for tracking active players
active_players = {}

# ----------------- Event Generation Functions -----------------

def generate_player_join_event():
    """Generates a 'player_join' event with sample data."""

    with open('event_definitions.json', 'r') as f:
        event_defs = json.load(f)

    player_join_def = next(item for item in event_defs if item["eventType"] == "player_join")

    event = {}
    for field in player_join_def['fields']:
        if field['type'] == 'string':
            if field['name'] == 'timestamp':
                event[field['name']] = time.strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                event[field['name']] = generate_sample_string(field['name'])
        elif field['type'] == 'integer':
            event[field['name']] = random.randint(1, 100)  

    player_id = event['player_id']
    active_players[player_id] = {'joined_at': event['timestamp']}
    return event

def generate_sample_string(field_name):
    """Generates sample string values for various event fields."""

   if field_name == 'game_mode':
    return random.choice(['team_deathmatch', 'capture_the_flag', 'battle_royale', 'objective_based']) 
        elif field_name == 'map_name':
             return random.choice(['urban_warfare', 'ancient_temple', 'space_station', 'forest_outpost'])
                elif field_name == 'region':
             return random.choice(['NA', 'EU', 'APAC', 'LATAM'])
                elif field_name == 'team':
                return random.choice(['red', 'blue', 'green'])  
                elif field_name == 'weapon_used':
  return random.choice(['assault_rifle', 'sniper_rifle', 'shotgun', 'grenade', 'rocket_launcher'])
  elif field_name == 'item_name':
    items = ['small_health_pack', 'large_health_pack', 'ammo_crate', 'shield']
    weights = [0.6, 0.2, 0.15, 0.05]  # Adjust to control rarity
  return random.choices(items, weights)
 else: # A catch-all for other potential string fields 
  return f"sample_{field_name}" 
  
  
def generate_match_start_event():
    """Generates a 'match_start' event with sample data."""

    with open('event_definitions.json', 'r') as f:
        event_defs = json.load(f)

    event_def = next(item for item in event_defs if item["eventType"] == "match_start")

    event = {}
    for field in event_def['fields']:
        if field['type'] == 'string':
            if field['name'] == 'game_mode':
                event[field['name']] = generate_sample_string(field['name'])
            elif field['name'] == 'map_name':
                event[field['name']] = generate_sample_string(field['name'])
            # Add more elif blocks for other string fields 
        elif field['type'] == 'integer':
            if field['name'] == 'match_id':
                event[field['name']] = random.randint(1000, 9999) 
            elif field['name'] == 'player_count':
                event[field['name']] = random.randint(2, 20)  # Adjust range for your game
            # Add more elif blocks for other integer fields 
    return event
    
def generate_player_kill_event():
    """Generates a 'player_kill' event with sample data."""

    with open('event_definitions.json', 'r') as f:
        event_defs = json.load(f)

    event_def = next(item for item in event_defs if item["eventType"] == "player_kill")

    event = {}
    for field in event_def['fields']:
        if field['type'] == 'string':
            if field['name'] == 'weapon_used':
                event[field['name']] = generate_sample_string(field['name'])
        elif field['type'] == 'integer':
            # ... (Your existing killer_id and victim_id logic) ... 
        elif field['type'] == 'boolean':
            if field['name'] == 'headshot':
                event[field['name']] = random.choice([True, False]) 
        elif field['type'] == 'number':  # Assuming float for distance
            if field['name'] == 'distance':
                event[field['name']] = random.uniform(5, 50)  # Adjust range 
                
        remove_inactive_players()  
    killer_id = random.choice(list(active_players.keys()))
    victim_id = random.choice(list(active_players.keys()))
    while victim_id == killer_id:
        victim_id = random.choice(list(active_players.keys()))

    event['killer_id'] = killer_id
    event['victim_id'] = victim_id
    return event
 

def generate_match_end_event(team_red_kills, team_blue_kills, team_red_objectives, team_blue_objectives):
    """Generates a 'match_end' event with sample data, including tie-handling logic."""

    with open('event_definitions.json', 'r') as f:
        event_defs = json.load(f)

    event_def = next(item for item in event_defs if item["eventType"] == "match_end")
    
     event = {}
    for field in event_def['fields']:
        if field['type'] == 'string':
            if field['name'] == 'timestamp':
                event[field['name']] = time.strftime('%Y-%m-%dT%H:%M:%SZ')
            elif field['name'] == 'winning_team':
                if team_red_kills > team_blue_kills:
                    event['winning_team'] = 'red' 
                elif team_blue_kills > team_red_kills:
                    event['winning_team'] = 'blue' 
                else:  # Tie in kills 
                    if team_red_objectives > team_blue_objectives:
                        event['winning_team'] = 'red'
                    elif team_blue_objectives > team_red_objectives:
                        event['winning_team'] = 'blue' 
                    else:  # Tie in both kills and objectives
                        event['winning_team'] = random.choice(['red', 'blue'])  
                        elif field['type'] == 'integer':
                            if field['name'] == 'match_id':
                                event[field['name']] = random.randint(1000, 9999) 
                        elif field['type'] == 'number':
                            if field['name'] == 'match_duration':
                                event[field['name']] = random.uniform(10, 30)  # Adjust for match length
                            elif field['type'] == 'array':
                                if field['name'] == 'player_scores':
                                    event[field['name']] = generate_player_scores()  # You'll need a helper function
    return event

def generate_item_pickup_event
    """Generates an 'item_pickup' event with sample data."""

    with open('event_definitions.json', 'r') as f:
        event_defs = json.load(f)

    event_def = next(item for item in event_defs if item["eventType"] == "item_pickup")

    event = {}
    for field in event_def['fields']:
        if field['type'] == 'string':
            if field['name'] == 'timestamp':
                event[field['name']] = time.strftime('%Y-%m-%dT%H:%M:%SZ')
            elif field['name'] == 'item_name':
                event[field['name']] = generate_sample_string(field['name'])
        elif field['type'] == 'integer':
            if field['name'] == 'player_id':
                event[field['name']] = random.choice(list(active_players.keys())) 
        elif field['type'] == 'number':
            if field['name'] == 'player_health':
                base_health_gain = 10  # Example
    if event['item_name'] == 'small_health_pack':
        health_gain = base_health_gain
    elif event['item_name'] == 'large_health_pack':
        health_gain = base_health_gain * 2  # Or some other multiplier 
    # ... Consider maximum health limits ...
    event[field['name']] = random.uniform(event['player_health'] + health_gain, event['player_health'] + health_gain + 10)  # Slight Variation
    return event

# ----------------- Helper Functions -----------------

def remove_inactive_players():
    """Removes players from active_players if they exceed the inactivity threshold."""

    current_time = time.time()  
    for player_id, data in list(active_players.items()): 
        if current_time - time.mktime(time.strptime(data['joined_at'], '%Y-%m-%dT%H:%M:%SZ')) > INACTIVITY_THRESHOLD:
            del active_players[player_id] 

def generate_player_scores():
    """Generates a sample list of player scores for the 'match_end' event."""

    num_players = random.randint(5, 15)  
    scores = []

    for _ in range(num_players):
        player_id = random.choice(list(active_players.keys())) 
        score = random.randint(0, 50) 
        scores.append({'player_id': player_id, 'score': score})

    return scores

