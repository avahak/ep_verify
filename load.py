# TODO...
import re
# import numpy as np
from typing import Type
import classes
import random

SQL_BACKUP_DIRECTORY = R'C:/Users/mavak/Desktop/eastpool_backup_05_09_2024/'
TABLE_NAMES = ["ep_rafla", "ep_kausi", "ep_lohko", "ep_jasen", "ep_pelaaja", 
               "ep_ottelu", "ep_sarjat", "ep_peli", "ep_erat", "ep_peli_tulokset",
               "ep_ottelu_tulokset", "ep_pelaaja_tulokset", "ep_joukkue_tulokset"]

def strip_str(s: str) -> str: 
    s = s.strip()
    if s == 'NULL':
        return None
    if len(s) >= 2 and s[0] == "'":
        return s[1:-1]
    return s

def load_sql_values(file_path: str, target_class: Type) -> str:
    # Load file into string:
    with open(SQL_BACKUP_DIRECTORY + file_path, 'r') as file:
        text = file.read()

    # Extract the data as a substring within the INSERT query:
    start_index = text.index(R"` VALUES ")
    end_index = text[start_index:].index(";")
    text = text[start_index+9:start_index+end_index]

    # Split the data into rows:
    # TODO Should fix: what if a string value inside has ( or ) character?
    pattern = r'\((.*?)\)'
    rows = re.findall(pattern, text)

    # Split each row into data values:
    data = []
    for row in rows: 
        # Regex pattern to match single-quoted strings and non-quotes
        pattern = r"'(?:[^']|'')*'|[^,']+"
        matches = re.findall(pattern, row)
        values = [strip_str(match) for match in matches]
        data.append(target_class(*values))

    return data

def load_db():
    db = {}
    for table_name in TABLE_NAMES: 
        db[table_name] = load_sql_values(f'takaisku_ep_{table_name}.sql', getattr(classes, table_name))
    return db

def print_db(db):
    for key in db:
        pick = random.sample(db[key], 6)
        for p in pick:
            print(p)
        print()

if __name__ == '__main__':
    db = load_db()
    print_db(db)