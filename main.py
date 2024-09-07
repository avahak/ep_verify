"""
Runs all the checks, creates output directory, and creates the output files.
"""
import references
import compare
import loader
import os

dir = "output"

if __name__ == "__main__":
    db = loader.load_db()
    os.makedirs(dir, exist_ok=True)
    compare.output_stats(db, dir)
    references.output_result(db, dir)