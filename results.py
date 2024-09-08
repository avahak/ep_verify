"""
Creates three different versions of stats from the database.
"""

from dataclasses import dataclass
# import numpy as np

@dataclass
class GameStats:
    ktulos: int
    vtulos: int

@dataclass
class MatchStats:
    ktulos: int
    vtulos: int

@dataclass
class PlayerStats:
    v_era: int
    h_era: int
    v_peli: int
    h_peli: int

@dataclass
class TeamStats:
    v_era: int
    h_era: int
    v_peli: int
    h_peli: int
    voitto: int
    tappio: int

def who_won_round(round_result):
    """
    Returns "home" if home player won, "away" if away player won, otherwise None.
    """
    if round_result in ['K1', 'K2', 'K3', 'K4', 'K5', 'K6']:
        return "home"
    if round_result in ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']:
        return "away"
    return None

def create_zero_stats(db):
    game_stats = {}
    match_stats = {}
    team_stats = {}
    player_stats = {}
    for id in db["ep_peli"].keys():
        game_stats[id] = GameStats(ktulos=0, vtulos=0)
    for id in db["ep_ottelu"].keys():
        match_stats[id] = MatchStats(ktulos=0, vtulos=0)
    for id in db["ep_pelaaja"].keys():
        player_stats[id] = PlayerStats(v_era=0, h_era=0, v_peli=0, h_peli=0)
    for id in db["ep_joukkue"].keys():
        team_stats[id] = TeamStats(v_era=0, h_era=0, v_peli=0, h_peli=0, voitto=0, tappio=0)
    return { 
        "game_stats": game_stats,      
        "match_stats": match_stats,
        "player_stats": player_stats, 
        "team_stats": team_stats
    }

def compute_stats(db):
    """
    Recreate the _tulokset tables from scratch from round results in ep_erat.
    """
    # Count for unique round results
    round_results_counter = {}

    stats = create_zero_stats(db)
    game_stats = stats["game_stats"]
    match_stats = stats["match_stats"]
    player_stats = stats["player_stats"]
    team_stats = stats["team_stats"]

    # process ep_erat
    for id, row in db["ep_erat"].items():
        game_id = row.peli
        if game_id not in db["ep_peli"]:
            continue

        match_id = db["ep_peli"][game_id].ottelu
        if match_id not in db["ep_ottelu"]:
            continue

        home_team_id = db["ep_ottelu"][match_id].koti
        away_team_id = db["ep_ottelu"][match_id].vieras
        if (home_team_id not in db["ep_joukkue"]) or (away_team_id not in db["ep_joukkue"]):
            continue

        home_player_id = db["ep_peli"][game_id].kp
        away_player_id = db["ep_peli"][game_id].vp
        if (home_player_id not in db["ep_pelaaja"]) or (away_player_id not in db["ep_pelaaja"]):
            continue

        for k in range(5):
            round_result = getattr(row, f'era{k+1}')
            round_results_counter[round_result] = round_results_counter.get(round_result, 0) + 1
            winner = who_won_round(round_result)
            game_stats[game_id].ktulos += 1 if winner == "home" else 0
            game_stats[game_id].vtulos += 1 if winner == "away" else 0

            team_stats[home_team_id].v_era += 1 if winner == "home" else 0
            team_stats[home_team_id].h_era += 1 if winner == "away" else 0
            team_stats[away_team_id].v_era += 1 if winner == "away" else 0
            team_stats[away_team_id].h_era += 1 if winner == "home" else 0

            player_stats[home_player_id].v_era += 1 if winner == "home" else 0
            player_stats[home_player_id].h_era += 1 if winner == "away" else 0
            player_stats[away_player_id].v_era += 1 if winner == "away" else 0
            player_stats[away_player_id].h_era += 1 if winner == "home" else 0

    # process ep_peli
    for id, row in game_stats.items():
        match_id = db["ep_peli"][id].ottelu
        if match_id not in db["ep_ottelu"]:
            continue 

        home_team_id = db["ep_ottelu"][match_id].koti
        away_team_id = db["ep_ottelu"][match_id].vieras
        if (home_team_id not in db["ep_joukkue"]) or (away_team_id not in db["ep_joukkue"]):
            continue

        home_player_id = db["ep_peli"][id].kp
        away_player_id = db["ep_peli"][id].vp
        if (home_player_id not in db["ep_pelaaja"]) or (away_player_id not in db["ep_pelaaja"]):
            continue

        winner = None
        if row.ktulos >= 3 and row.vtulos < row.ktulos:
            winner = "home"
        elif row.vtulos >= 3 and row.ktulos < row.vtulos:
            winner = "away"

        match_stats[match_id].ktulos += 1 if winner == "home" else 0
        match_stats[match_id].vtulos += 1 if winner == "away" else 0

        team_stats[home_team_id].v_peli += 1 if winner == "home" else 0
        team_stats[home_team_id].h_peli += 1 if winner == "away" else 0
        team_stats[away_team_id].v_peli += 1 if winner == "away" else 0
        team_stats[away_team_id].h_peli += 1 if winner == "home" else 0

        player_stats[home_player_id].v_peli += 1 if winner == "home" else 0
        player_stats[home_player_id].h_peli += 1 if winner == "away" else 0
        player_stats[away_player_id].v_peli += 1 if winner == "away" else 0
        player_stats[away_player_id].h_peli += 1 if winner == "home" else 0

    # teams: voitto, tappio
    for id, row in match_stats.items():
        winner = None
        if row.ktulos > row.vtulos:
            winner = "home"
        elif row.vtulos > row.ktulos:
            winner = "away"

        home_team_id = db["ep_ottelu"][id].koti
        away_team_id = db["ep_ottelu"][id].vieras
        if (home_team_id not in db["ep_joukkue"]) or (away_team_id not in db["ep_joukkue"]):
            continue

        team_stats[home_team_id].voitto += 1 if winner == "home" else 0
        team_stats[home_team_id].tappio += 1 if winner == "away" else 0
        team_stats[away_team_id].voitto += 1 if winner == "away" else 0
        team_stats[away_team_id].tappio += 1 if winner == "home" else 0

    return stats

def get_stats_original(db):
    """
    Returns stats object according to original stats fields.
    """
    stats = create_zero_stats(db)
    game_stats = stats["game_stats"]
    match_stats = stats["match_stats"]
    player_stats = stats["player_stats"]
    team_stats = stats["team_stats"]

    for id, row in db["ep_peli"].items():
        game_stats[id].ktulos = row.ktulos
        game_stats[id].vtulos = row.vtulos

    for id, row in db["ep_ottelu"].items():
        match_stats[id].ktulos = row.ktulos
        match_stats[id].vtulos = row.vtulos

    for id, row in db["ep_pelaaja"].items():
        player_stats[id].v_era = row.v_era
        player_stats[id].h_era = row.h_era
        player_stats[id].v_peli = row.v_peli
        player_stats[id].h_peli = row.h_peli

    for id, row in db["ep_sarjat"].items():
        team_id = row.joukkue
        if team_id not in db["ep_joukkue"]:
            continue
        team_stats[team_id].v_era = row.v_era
        team_stats[team_id].h_era = row.h_era
        team_stats[team_id].v_peli = row.v_peli
        team_stats[team_id].h_peli = row.h_peli
        team_stats[team_id].voitto = row.voitto
        team_stats[team_id].tappio = row.tappio
    return stats

def get_stats_tulokset(db):
    """
    Returns stats object according to _tulokset tables.
    """
    stats = create_zero_stats(db)
    game_stats = stats["game_stats"]
    match_stats = stats["match_stats"]
    player_stats = stats["player_stats"]
    team_stats = stats["team_stats"]

    for id, row in db["ep_peli_tulokset"].items():
        game_id = row.peli
        if game_id not in db["ep_peli"]:
            continue
        game_stats[game_id].ktulos = row.ktulos
        game_stats[game_id].vtulos = row.vtulos

    for id, row in db["ep_ottelu_tulokset"].items():
        match_id = row.ottelu
        if match_id not in db["ep_ottelu"]:
            continue
        match_stats[match_id].ktulos = row.ktulos
        match_stats[match_id].vtulos = row.vtulos

    for id, row in db["ep_pelaaja_tulokset"].items():
        player_id = row.pelaaja
        if player_id not in db["ep_pelaaja"]:
            continue
        player_stats[player_id].v_era = row.v_era
        player_stats[player_id].h_era = row.h_era
        player_stats[player_id].v_peli = row.v_peli
        player_stats[player_id].h_peli = row.h_peli

    for id, row in db["ep_joukkue_tulokset"].items():
        team_id = row.joukkue
        if team_id not in db["ep_joukkue"]:
            continue
        team_stats[team_id].v_era = row.v_era
        team_stats[team_id].h_era = row.h_era
        team_stats[team_id].v_peli = row.v_peli
        team_stats[team_id].h_peli = row.h_peli
        team_stats[team_id].voitto = row.voitto
        team_stats[team_id].tappio = row.tappio
    return stats

if __name__ == '__main__':
    pass