from dataclasses import dataclass
import loader
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
    if round_result in ['K1', 'K2', 'K3', 'K4', 'K5', 'K6']:
        return "home"
    if round_result in ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']:
        return "away"
    return None

def tabulate_results(db):
    """
    Recreate the _tulokset tables from scratch from round results in ep_erat.
    """
    # Count for unique round results
    round_results_counter = {}

    # Correctly counted counterparts to 
    # ep_peli_tulokset, ep_ottelu_tulokset, ep_pelaaja_tulokset, ep_joukkue_tulokset
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


    # Compute game_stats
    for id, row in db["ep_erat"].items():
        game_id = row.peli
        if game_id not in db["ep_peli"]:
            continue
        for k in range(5):
            round_result = getattr(row, f'era{k+1}')
            round_results_counter[round_result] = round_results_counter.get(round_result, 0)+1
            winner = who_won_round(round_result)
            game_stats[game_id].ktulos += 1 if winner == "home" else 0
            game_stats[game_id].vtulos += 1 if winner == "away" else 0


    print(game_stats)
    print(f'{round_results_counter = }')


if __name__ == '__main__':
    db = loader.load_db()
    tabulate_results(db)