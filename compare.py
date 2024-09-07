"""
Compare the three different versions of stats.
"""

import loader
import results

def compare_stats(db):
    """
    Compare the three versions of stats: compute_stats, _tulokset tables, and old results.
    """
    stats = results.compute_stats(db)
    stats_original = results.get_stats_original(db)
    stats_tulokset = results.get_stats_tulokset(db)

    # game_stats
    for id, row in db["ep_peli"]:
        s = stats["game_stats"][id]
        so = stats_original["game_stats"][id]
        st = stats_tulokset["game_stats"][id]
        if s != so:
            log




if __name__ == '__main__':
    db = loader.load_db()
    compare_stats(db)

game_stats = stats["game_stats"]
match_stats = stats["match_stats"]
player_stats = stats["player_stats"]
team_stats = stats["team_stats"]