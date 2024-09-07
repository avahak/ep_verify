"""
Loads all the exported database dumps into a single object containing the parsed data.
"""
import re
from typing import Type
import classes
import random

SQL_BACKUP_DIRECTORY = R'C:/Users/mavak/Desktop/ep_sql_backup_07-09-2024/'
TABLE_NAMES = ["ep_rafla", "ep_kausi", "ep_lohko", "ep_jasen", "ep_pelaaja", "ep_joukkue",
               "ep_ottelu", "ep_sarjat", "ep_peli", "ep_erat", "ep_peli_tulokset",
               "ep_ottelu_tulokset", "ep_pelaaja_tulokset", "ep_joukkue_tulokset"]

def strip_str(s: str) -> str: 
    s = s.strip()
    if s == 'NULL':
        return None
    if len(s) >= 2 and s[0] == "'":
        return s[1:-1]
    return s

def load_table(file_path: str, target_class: Type) -> str:
    """
    Super scuffed, use with caution.
    """
    table = {}

    # Load file into string:
    with open(SQL_BACKUP_DIRECTORY + file_path, 'r', encoding='utf-8') as file:
        all_text = file.read()

    # Go through insert queries in the file
    for start_index in [iter.start() for iter in re.finditer("` VALUES ", all_text)]:
        # Extract the data as a substring within the INSERT query
        end_index = all_text[start_index:].index(");")  # sloppy, could be within a string!

        text = all_text[start_index+9 : start_index+end_index+1]
        # print(f'{file_path}: [{start_index+9}, {start_index+end_index+1}]')

        # Split the data into rows:
        # TODO Should fix: what if a string value inside has ( or ) character?
        pattern = r'\((.*?)\)'
        rows = re.findall(pattern, text)
        # rows = [row.replace("\\'", '"') for row in rows]  # not needed - regex handles

        # Split each row into data values and enter them into a dict:
        for row in rows: 
            # Regex pattern to match single-quoted strings and non-quotes
            pattern = r"'(?:\\'|[^'])*'|[^,]+"
            matches = re.findall(pattern, row)
            values = [strip_str(match) for match in matches]
            obj = target_class(*values)
            table[obj.id] = obj

    return table

def load_db():
    db = {}
    for table_name in TABLE_NAMES: 
        db[table_name] = load_table(f'takaisku_ep_{table_name}.sql', getattr(classes, table_name))
    return db

def print_db_samples(db, count):
    for key in db:
        table = db[key]
        ids = list(table.keys())
        pick = random.sample(ids, count)
        for id in pick:
            print(f'id {id}: {table[id]}')
        print()

if __name__ == '__main__':
    db = load_db()
    # print_db_samples(db, 6)

    # print(db["ep_peli"][31203])
    # for id, row in db["ep_erat"].items():
    #     if row.peli == 31203:
    #         print(row)
    # print(db["ep_erat"])

    # team = db["ep_joukkue"][728]
    # print(team)

    player = db["ep_pelaaja"][5167]
    print(player)
    team = db["ep_joukkue"][player.joukkue]
    print(team)
