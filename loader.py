"""
Loads all the exported database dumps into a single object containing the parsed data.
"""
import re
from typing import List, Type
import random
import os

import config
import classes

def get_files_in_directory(directory: str) -> List[str]:
    try:
        return [s for s in os.listdir(directory) if os.path.isfile(os.path.join(directory, s))]
    except Exception as e:
        print(f"An error occurred: {e}")
    return []

def strip_str(s: str) -> str: 
    s = s.strip()
    if s == 'NULL':
        return None
    if len(s) >= 2 and s[0] == "'":
        return s[1:-1]
    return s

def load_table(file_path: str, target_class: Type) -> str:
    """
    Super scuffed, use with caution!
    """
    table = {}

    # Load file into string:
    with open(f'{config.SQL_BACKUP_DIRECTORY}/{file_path}', 'r', encoding='utf-8') as file:
        all_text = file.read()

    start_indexes = [iter.start() for iter in re.finditer("` VALUES ", all_text)]

    # Go through insert queries in the file
    for start_index in start_indexes:
        # Extract the data as a substring within the INSERT query
        # TODO Should fix: sloppy, could be within a string!
        end_index = all_text[start_index:].index(");")

        text = all_text[start_index+9 : start_index+end_index+1]
        # print(f'{file_path}: [{start_index+9}, {start_index+end_index+1}]')

        # Split the data into rows:
        # TODO Should fix: what if a string value inside has ( or ) character?
        pattern = r'\((.*?)\)'
        rows = re.findall(pattern, text)

        # Split each row into data values and enter them into the given dataclass:
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
    file_names = get_files_in_directory(config.SQL_BACKUP_DIRECTORY)

    for file_name in file_names:
        # Files should have the form "dbname_tablename.sql"
        if not file_name.startswith(config.DATABASE_NAME) or not file_name.endswith(".sql"):
            continue
        table_name = file_name[len(config.DATABASE_NAME)+1:-4]
        db[table_name] = load_table(file_name, getattr(classes, table_name))
    return db

def print_db_samples(db, count: int):
    for key in db:
        table = db[key]
        ids = list(table.keys())
        pick = random.sample(ids, count)
        for id in pick:
            print(f'id {id}: {table[id]}')
        print()

if __name__ == '__main__':
    db = load_db()
    print_db_samples(db, 4)

    # print(db["ep_peli"][31203])
    # for id, row in db["ep_erat"].items():
    #     if row.peli == 31203:
    #         print(row)
    # print(db["ep_erat"])

    # team = db["ep_joukkue"][728]
    # print(team)

    # player = db["ep_pelaaja"][5167]
    # print(player)
    # team = db["ep_joukkue"][player.joukkue]
    # print(team)
