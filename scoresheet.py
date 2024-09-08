import loader
import config
from results import who_won_round

"""
Checks some aspects of the scoresheet integrity:
- only symbols "V0", "K1-K6", "V1-V6" are used in ep_erat.era[1-5]
- no non-wins before game resolution and no wins after it

TODO
- players need to belong to the correct teams
- only one player can be empty in ep_peli
- empty player has to lose all rounds
...
"""

def check_ep_erat_symbols_and_resolution():
    """
    Check that only symbols "V0", "K1-K6", "V1-V6" are used in ep_erat.era[1-5].
    Also checks that there are no non-wins before game resolution and no wins after it.
    """
    findings = "--- allowed symbols and game resolution ---\n\n"
    for id, row in db["ep_erat"].items():
        score = { "home": 0, "away": 0 }
        row_findings = []
        for k in range(5):
            symbol = getattr(row, f'era{k+1}')
            winner = who_won_round(symbol)

            # check that no invalid symbols are used
            if (winner is None) and (symbol != "V0"):
                row_findings.append(f'era{k+1} invalid value: \"{symbol}\"')
            
            # check that there are no non-wins before resolution and no wins after
            is_resolved = score["home"] >= 3 or score["away"] >= 3
            if is_resolved and winner is not None:
                row_findings.append(f'era{k+1} declares winner after game resolution')
            if not is_resolved and winner is None:
                row_findings.append(f'era{k+1} declares no winner before game resolution')

            # update score
            if winner == "home":
                score["home"] += 1
            if winner == "away":
                score["away"] += 1

        if len(row_findings) > 0:
            findings += f'{id = }: {", ".join(row_findings)}\n'
            
    return findings + "\n\n"

def check(db):
    # Track which ep_erat rows are associated with a given match
    match_id_to_round_ids = {}
    for id, row in db["ep_ottelu"].items():
        match_id_to_round_ids[id] = []
    for id, row in db["ep_erat"].items():
        game_id = row.peli
        if game_id not in db["ep_peli"]:
            continue
        match_id = db["ep_peli"][game_id].ottelu
        if match_id not in db["ep_ottelu"]:
            continue
        match_id_to_round_ids[match_id].append(id)

    # print([len(l) for l in match_id_to_round_ids.values()])
    
    findings = ""
    findings += check_ep_erat_symbols_and_resolution()

    with open(f'{config.OUTPUT_DIR}/scoresheet.txt', 'w') as f:
        f.write(findings)
    

if __name__ == '__main__':
    db = loader.load_db()
    check(db)
    print(db["ep_erat"][30447])
    print(db["ep_peli"][30447])
    print(db["ep_ottelu"][6498])