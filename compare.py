"""
Compare the three versions of stats: computed stats, original results, and _tulokset tables.
"""

import loader
import results
import config
from dataclasses import fields

def verify_stats(db, table, category, heading, stats, stats_original, stats_tulokset):
    findings = f'--- {heading} ---\n\n'
    for id in db[table]:
        s = stats[category][id]
        so = stats_original[category][id]
        st = stats_tulokset[category][id]
        diff_s_so = {f.name for f in fields(s) if getattr(s, f.name) != getattr(so, f.name)}
        diff_s_st = {f.name for f in fields(s) if getattr(s, f.name) != getattr(st, f.name)}
        diff = list(diff_s_so | diff_s_st)    # union set as list
        if len(diff) > 0:
            tuple_begin = "(" if len(diff) > 1 else ""
            tuple_end = ")" if len(diff) > 1 else ""
            findings += f'{id=}: expected: {tuple_begin}' + ",".join(diff) + f"{tuple_end}={tuple_begin}" + ",".join([f'{getattr(s, field_name)}' for field_name in diff]) + tuple_end
            if s != so:
                findings += f', original: ={tuple_begin}' + ",".join([f'{getattr(so, field_name)}' for field_name in diff]) + tuple_end
            if s != st:
                findings += f', tulokset: ={tuple_begin}' + ",".join([f'{getattr(st, field_name)}' for field_name in diff]) + tuple_end
            findings += "\n"
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
        expected = { "e_era": row.v_era-row.h_era, "e_peli": row.v_peli-row.h_peli, "pelit": row.v_peli+row.h_peli }
        found = { "e_era": row.e_era, "e_peli": row.e_peli, "pelit": row.pelit }
        diff = [field_name for field_name in expected if getattr(row, field_name) != expected[field_name]]
        if len(diff) > 0:
            tuple_begin = "(" if len(diff) > 1 else ""
            tuple_end = ")" if len(diff) > 1 else ""
            findings += f'{lohko=}, joukkue={row.joukkue}, {id=}: expected: {tuple_begin}' + ",".join(diff) + f'{tuple_end}={tuple_begin}' + ",".join([f'{expected[field_name]}' for field_name in diff]) + tuple_end
            findings += f', found: {tuple_begin}' + ",".join([f'{found[field_name]}' for field_name in diff]) + tuple_end
            findings += "\n"
    return findings
            

def output_stats(db):
    stats = results.compute_stats(db)
    stats_original = results.get_stats_original(db)
    stats_tulokset = results.get_stats_tulokset(db)

    output = [
        ("ep_peli", verify_stats(db, "ep_peli", "game_stats", "game stats", stats, stats_original, stats_tulokset)), 
        ("ep_ottelu", verify_stats(db, "ep_ottelu", "match_stats", "match stats", stats, stats_original, stats_tulokset)), 
        ("ep_pelaaja", verify_stats(db, "ep_pelaaja", "player_stats", "player stats", stats, stats_original, stats_tulokset)), 
        ("ep_joukkue", verify_stats(db, "ep_joukkue", "team_stats", "team stats", stats, stats_original, stats_tulokset)), 
        ("ep_pelaaja_redundant", verify_redundant_fields_in_ep_pelaaja(db))
    ]

    for name, findings in output:
        with open(f'{config.OUTPUT_DIR}/{name}.txt', 'w') as f:
            f.write(findings)


if __name__ == '__main__':
    db = loader.load_db()
    output_stats(db)