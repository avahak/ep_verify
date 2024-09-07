"""
Compare the three different versions of stats.
"""

import loader
import results

output_file_name = "output/findings.txt"

def compare_stats(db, table, category, heading, stats, stats_original, stats_tulokset):
    findings = f'--- {heading} ---\n'
    for id, row in db[table]:
        s = stats[category][id]
        so = stats_original[category][id]
        st = stats_tulokset[category][id]
        if s != so:
            findings = findings + f'{id=}: ' + 'expected: ' + s + ', original: ' + so + '\n'
        if s != st:
            findings = findings + f'{id=}: ' + 'expected: ' + s + ', tulokset: ' + st + '\n'
    return findings

def output_stats(db):
    """
    Compare the three versions of stats: compute_stats, _tulokset tables, and old results.
    """
    stats = results.compute_stats(db)
    stats_original = results.get_stats_original(db)
    stats_tulokset = results.get_stats_tulokset(db)

    findings = ""

    findings = findings + compare_stats(db, "ep_peli", "game_stats", "game stats", stats, stats_original, stats_tulokset) + "\n\n"
    findings = findings + compare_stats(db, "ep_ottelu", "match_stats", "match stats", stats, stats_original, stats_tulokset) + "\n\n"
    findings = findings + compare_stats(db, "ep_pelaaja", "player_stats", "player stats", stats, stats_original, stats_tulokset) + "\n\n"
    findings = findings + compare_stats(db, "ep_joukkue", "team_stats", "team stats", stats, stats_original, stats_tulokset) + "\n\n"

    with open(output_file_name, 'w') as f:
        f.write(findings)


if __name__ == '__main__':
    db = loader.load_db()
    output_stats(db)