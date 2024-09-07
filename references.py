"""
Check the referential integrity of the database for the most important tables.
NOTE: ideally this would be done in the database schema by adding foreign key constraits
to all the references.
"""
import loader
import config

def verify_reference_integrity(db, table_name, key_name, referenced_table):
    needs_output = False
    findings = f'--- {table_name}.{key_name} --\n\n'
    for id, row in db[table_name].items():
        reference_id = getattr(row, key_name)
        if reference_id not in db[referenced_table]:
            findings = findings + f'{table_name}({id=}): {key_name}={reference_id} not found in {referenced_table}\n'
            needs_output = True
    return findings + "\n\n" if needs_output else ""

def output_result(db):
    findings = ""
    references = [
        ("ep_lohko", "kausi", "ep_kausi"),
        ("ep_joukkue", "kausi", "ep_kausi"),
        ("ep_joukkue", "lohko", "ep_lohko"),
        ("ep_pelaaja", "joukkue", "ep_joukkue"),
        ("ep_ottelu", "lohko", "ep_lohko"),
        ("ep_ottelu", "koti", "ep_joukkue"),
        ("ep_ottelu", "vieras", "ep_joukkue"),
        ("ep_sarjat", "joukkue", "ep_joukkue"),
        ("ep_sarjat", "lohko", "ep_lohko"),
        ("ep_sarjat", "ottelu", "ep_ottelu"),
        ("ep_peli", "ottelu", "ep_ottelu"),
        ("ep_peli", "kp", "ep_pelaaja"),
        ("ep_peli", "vp", "ep_pelaaja"),
        ("ep_erat", "peli", "ep_peli"), 
        ("ep_peli_tulokset", "peli", "ep_peli"),
        ("ep_ottelu_tulokset", "ottelu", "ep_ottelu"),
        ("ep_pelaaja_tulokset", "pelaaja", "ep_pelaaja"),
        ("ep_joukkue_tulokset", "joukkue", "ep_joukkue")
    ]

    for table_name, key_name, referenced_table in references:
        findings = findings + verify_reference_integrity(db, table_name, key_name, referenced_table)

    with open(f'{config.OUTPUT_DIR}/referential_integrity.txt', 'w') as f:
        f.write(findings)

if __name__ == '__main__':
    db = loader.load_db()
    output_result(db)