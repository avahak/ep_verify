"""
Loads .sql files into one object, creates output directory, 
runs the checks, and creates the output files.
"""
import os

import config
import loader
import references
import compare
import scoresheet

if __name__ == "__main__":
    db = loader.load_db()
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    compare.output_stats(db)
    references.output_result(db)
    scoresheet.output_result(db)