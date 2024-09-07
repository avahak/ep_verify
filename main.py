"""
Loads .sql files into one object, creates output directory, 
runs the checks, and creates the output files.
"""
import references
import compare
import loader
import os
import config

if __name__ == "__main__":
    db = loader.load_db()
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    compare.output_stats(db)
    references.output_result(db)