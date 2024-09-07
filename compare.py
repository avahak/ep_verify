"""
Compare the three different versions of stats.
"""

import loader
import results

def verify_stats(db, table, category, heading, stats, stats_original, stats_tulokset):
    findings = f'--- {heading} ---\n\n'
    for id in db[table]:
        s = stats[category][id]
        so = stats_original[category][id]
        st = stats_tulokset[category][id]
        if s != so:
            findings = findings + f'{id=}: ' + 'expected: ' + str(s) + ', original: ' + str(so) + '\n'
        if s != st:
            findings = findings + f'{id=}: ' + 'expected: ' + str(s) + ', tulokset: ' + str(st) + '\n'
    return findings

def verify_redundant_fields_in_ep_pelaaja(db):
    """
    Checkes e_era, e_peli, pelit in ep_pelaaja.
    NOTE: Can fix with query like:
    UPDATE ep_pelaaja p INNER JOIN ep_joukkue j ON p.joukkue=j.id SET p.e_era=p.v_era-p.h_era, p.e_peli=p.v_peli-p.h_peli, p.pelit=p.v_peli+p.h_peli WHERE j.lohko=117;
    """
    findings = f'--- ep_pelaaja: e_era, e_peli, pelit ---\n\n'
    for id, row in db["ep_pelaaja"].items():
        if row.joukkue not in db["ep_joukkue"]:
            continue    # problem with database integrity
        lohko = db["ep_joukkue"][row.joukkue].lohko
        if row.e_era != row.v_era-row.h_era:
            findings = findings + f'{lohko=}, joukkue={row.joukkue}, {id=}: expected: e_era={row.v_era-row.h_era}, found value: {row.e_era}\n'
        if row.e_peli != row.v_peli-row.h_peli:
            findings = findings + f'{lohko=}, joukkue={row.joukkue}, {id=}: expected: e_peli={row.v_peli-row.h_peli}, found value: {row.e_peli}\n'
        if row.pelit != row.v_peli+row.h_peli:
            findings = findings + f'{lohko=}, joukkue={row.joukkue}, {id=}: expected: pelit={row.v_peli+row.h_peli}, found value: {row.pelit}\n'
    return findings
            

def output_stats(db, dir):
    """
    Compare the three versions of stats: compute_stats, _tulokset tables, and old results.
    """
    stats = results.compute_stats(db)
    stats_original = results.get_stats_original(db)
    stats_tulokset = results.get_stats_tulokset(db)

    output = [
        ("game", verify_stats(db, "ep_peli", "game_stats", "game stats", stats, stats_original, stats_tulokset)), 
        ("match", verify_stats(db, "ep_ottelu", "match_stats", "match stats", stats, stats_original, stats_tulokset)), 
        ("player", verify_stats(db, "ep_pelaaja", "player_stats", "player stats", stats, stats_original, stats_tulokset)), 
        ("team", verify_stats(db, "ep_joukkue", "team_stats", "team stats", stats, stats_original, stats_tulokset)), 
        ("ep_pelaaja_redundant", verify_redundant_fields_in_ep_pelaaja(db))
    ]

    for (type, findings) in output:
        with open(f'{dir}/{type}_findings.txt', 'w') as f:
            f.write(findings)


if __name__ == '__main__':
    db = loader.load_db()
    output_stats(db, "output")