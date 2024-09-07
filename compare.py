"""
Compare the three different versions of stats.
"""

import loader
import results

def compare_stats(db, table, category, heading, stats, stats_original, stats_tulokset):
    findings = f'--- {heading} ---\n\n'
    for id, row in db[table].items():
        s = stats[category][id]
        so = stats_original[category][id]
        st = stats_tulokset[category][id]
        if s != so:
            findings = findings + f'{id=}: ' + 'expected: ' + str(s) + ', original: ' + str(so) + '\n'
        if s != st:
            findings = findings + f'{id=}: ' + 'expected: ' + str(s) + ', tulokset: ' + str(st) + '\n'
    return findings

def output_stats(db):
    """
    Compare the three versions of stats: compute_stats, _tulokset tables, and old results.
    """
    stats = results.compute_stats(db)
    stats_original = results.get_stats_original(db)
    stats_tulokset = results.get_stats_tulokset(db)

    game_findings = compare_stats(db, "ep_peli", "game_stats", "game stats", stats, stats_original, stats_tulokset)
    match_findings = compare_stats(db, "ep_ottelu", "match_stats", "match stats", stats, stats_original, stats_tulokset)
    player_findings = compare_stats(db, "ep_pelaaja", "player_stats", "player stats", stats, stats_original, stats_tulokset)
    team_findings = compare_stats(db, "ep_joukkue", "team_stats", "team stats", stats, stats_original, stats_tulokset)

    for (type, findings) in [("game", game_findings), ("match", match_findings), ("player", player_findings), ("team", team_findings)]:
        with open(f'output/{type}_findings.txt', 'w') as f:
            f.write(findings)


if __name__ == '__main__':
    db = loader.load_db()
    output_stats(db)